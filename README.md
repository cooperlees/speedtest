# speedtest

Docker Container with latest Official Speedtest CLI wrapped into a prometheus exporter.

Seems to outperform all the native python alternatives out there.

## speedtest-wrapper

Python code using `prometheus_client` to run a small webserver to run a speedtest using the offical CLIs

We only support latest version of python as we're predominately a `Docker` deployed wrapper.

### Develop

- venv to run tests

```console
python3.10 -m venv --upgrade-deps /tmp/ts
/tmp/ts/bin/pip install black coverage
/tmp/ts/bin/coverage run tests.py
/tmp/ts/bin/coverage report -m
```

### Docker Build + run

- `docker build -t cooperlees/speedtest-wrapper .`
- `docker run --network host --rm --name speedtest_dev cooperlees/speedtest-wrapper`

To see stats:

- `curl -v http://localhost:6970/metrics`
  - Does not work on MacOS tho ... didn't debug / workout options

### Keys

All are prefixed with `speedtest_`

- `sppedtest_*_bytes` - Seems to be kilobytes
  - To get megabit per second: `speedtest_*_bytes / speedtest_*_elapsed * 8 / 1024`
