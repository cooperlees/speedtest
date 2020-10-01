#!/usr/bin/env python3

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# coding=utf8

import argparse
import json
import logging
import sys
import time
from socket import getfqdn
from subprocess import CompletedProcess, PIPE, run
from typing import Dict, Generator, Union

from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server


DEFAULT_PORT = 6970
HOSTNAME = getfqdn()
LOG = logging.getLogger(__name__)


class SpeedtestCollector:
    IGNORE_CATEGORIES = ("interface", "server", "result")
    key_prefix = "speedtest"
    labels = ["hostname", "speedtest_host"]

    def _handle_counter(self, category: str, value: float) -> GaugeMetricFamily:
        normalized_category = category.replace(" ", "_")
        key = f"{self.key_prefix}_{normalized_category}"
        g = GaugeMetricFamily(key, "Speedtest Metric", labels=self.labels)
        g.add_metric([HOSTNAME, self.speedtest_host], value)
        return g

    def collect(self) -> Generator[GaugeMetricFamily, None, None]:
        start_time = time.time()
        LOG.info("Collection started")

        speedtest_data = self.run_speedtest()
        if isinstance(speedtest_data, CompletedProcess):
            LOG.error(
                f"Speedtest failed: {speedtest_data.stderr.decode('utf8')} "
                + f"(returned {speedtest_data.returncode})"
            )
            return
        elif not speedtest_data:
            return

        self.speedtest_host = speedtest_data["server"]["host"]
        for category, value in speedtest_data.items():
            if isinstance(value, (float, int)):
                yield self._handle_counter(category, float(value))
            elif category not in self.IGNORE_CATEGORIES and isinstance(value, dict):
                for subcategory, subvalue in value.items():
                    combined_category = f"{category}_{subcategory}"
                    yield self._handle_counter(combined_category, float(subvalue))

        run_time = time.time() - start_time
        LOG.info(f"Collection finished in {run_time}s")

    def run_speedtest(self) -> Union[Dict, CompletedProcess]:
        cmd = ["speedtest", "--accept-license", "-f", "json", "-u", "bps"]
        cp = run(cmd, stderr=PIPE, stdout=PIPE)
        if cp.returncode:
            return cp
        return json.loads(cp.stdout)


def _handle_debug(debug: bool) -> None:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Speedtest Wrapper")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run webserver on [Default = {DEFAULT_PORT}]",
    )
    args = parser.parse_args()
    _handle_debug(args.debug)

    LOG.info(f"Starting {sys.argv[0]}")
    start_http_server(args.port)
    REGISTRY.register(SpeedtestCollector())
    LOG.info(f"Speedtest Prometheus Exporter - listening on {args.port}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info("Shutting down ...")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
