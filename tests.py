#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch

import speedtest_wrapper


# 20220921 return
MOCK_SPEEDTEST_JSON = {
    "type": "result",
    "timestamp": "2022-09-22T04:29:10Z",
    "ping": {"jitter": 4.077, "latency": 13.814, "low": 9.838, "high": 17.448},
    "download": {
        "bandwidth": 73593870,
        "bytes": 561306538,
        "elapsed": 7814,
        "latency": {"iqm": 49.645, "low": 12.847, "high": 81.176, "jitter": 11.933},
    },
    "upload": {
        "bandwidth": 4550470,
        "bytes": 27235440,
        "elapsed": 5903,
        "latency": {"iqm": 13.94, "low": 10.793, "high": 140.264, "jitter": 4.597},
    },
    "packetLoss": 0,
    "isp": "Spectrum",
    "interface": {
        "internalIp": "172.17.0.2",
        "name": "eth0",
        "macAddr": "02:42:AC:11:00:02",
        "isVpn": False,
        "externalIp": "47.33.15.75",
    },
    "server": {
        "id": 2408,
        "host": "spt01renonv.reno.nv.charter.com",
        "port": 8080,
        "name": "Spectrum",
        "location": "Reno, NV",
        "country": "United States",
        "ip": "24.205.192.190",
    },
    "result": {
        "id": "00420ff7-e453-44d9-8caa-b018cf72105e",
        "url": "https://www.speedtest.net/result/c/00420ff7-e453-44d9-8caa-b018cf72105e",
        "persisted": True,
    },
}


# Shitty tests just to ensure file has valid syntax and imports
class TestSpeedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.stc = speedtest_wrapper.SpeedtestCollector(debug=False)

    def test_stc_valid(self) -> None:
        self.assertTrue(self.stc)

    @patch(
        "speedtest_wrapper.SpeedtestCollector.run_speedtest",
        return_value=MOCK_SPEEDTEST_JSON,
    )
    def test_collect(self, mock_run_speedtest: Mock) -> None:
        guages = []
        for guage in self.stc.collect():
            guages.append(guage)
        self.assertEqual("spt01renonv.reno.nv.charter.com", self.stc.speedtest_host)
        self.assertEqual(19, len(guages))


if __name__ == "__main__":
    unittest.main()
