# speedtest
Docker Container with latest Official Speedtest Docker

## speedtest-wrapper

Python code using `prometheus_client` to run a small webserver to run a speedtest using the offical CLIs

### Keys

All are prefixed with `speedtest_`

- `sppedtest_*_bytes` - Seems to be kilobytes
  - To get megabit per second: `speedtest_*_bytes / speedtest_*_elapsed * 8 / 1024`
