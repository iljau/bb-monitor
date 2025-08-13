"""
Script makes a GET request to specified url and outputs following data in one line:
[response_code] [result] [response_time_in_ms]

Example:
$ python bb_monitor.py https://google.com
200 OK 2296

In case result was successful, exit code is 0. In other cases (unsuccessful check,
exception while executing code), it's not.

It's also possible to get results as json and set approximate timeout for request.
$ python bb_monitor.py https://google.com --json
{"url": "https://google.com", "response_code": 200, "result": "OK", "respose_time_ms": 932.5250999536365}

$ python bb_monitor.py https://google.com --json --timeout 0.1
{"url": "https://google.com", "response_code": null, "result": "NOK", "respose_time_ms": 767.2840999439359}
"""

import argparse
import dataclasses
import json
import sys
import timeit

import requests

@dataclasses.dataclass
class MonitoringOutput:
    url: str
    response_code: int
    result: str
    respose_time_ms: float

@dataclasses.dataclass
class RequestResult:
    url: str
    response_code: int
    respose_time_ms: float

    def is_ok(self) -> bool:
        return self.response_code == 200

    def _as_output_dc(self) -> MonitoringOutput:
        return MonitoringOutput(
            url=self.url,
            response_code=self.response_code,
            result="OK" if self.is_ok() else "NOK",
            respose_time_ms=self.respose_time_ms,
        )

    def as_str(self) -> str:
        res = self._as_output_dc()
        return "%s %s %.0f" % (res.response_code, res.result, res.respose_time_ms)

    def as_json(self) -> str:
        res = dataclasses.asdict(self._as_output_dc())
        return json.dumps(res)

def fetch_url_with_stats(url: str, timeout: float=None) -> RequestResult:
    start = timeit.default_timer()

    try:
        r = requests.get(url, timeout=timeout)
        response_code = r.status_code
    except requests.exceptions.ConnectionError as e:
        # no network
        response_code = None
    except requests.exceptions.Timeout as e:
        response_code = None
    except Exception as e:
        # re-raise exception, exit_code not used
        raise e

    diff = timeit.default_timer() - start
    diff_ms = diff * 1000

    res = RequestResult(
        url=url,
        response_code=response_code,
        respose_time_ms=diff_ms,
    )

    return res

def fetch_url_and_output(url: str, json_output: bool, timeout: float) -> None:
    res: RequestResult = fetch_url_with_stats(url, timeout=timeout)
    if json_output:
        print(res.as_json())
    else:
        print(res.as_str())

    # 0 in case of success, 1 in case errors
    if res.is_ok():
        sys.exit(0)
    else:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to check")
    parser.add_argument("--json", action='store_true', help="Output JSON output")
    parser.add_argument("--timeout", type=float, help="Request timeout in seconds")
    args = parser.parse_args()

    fetch_url_and_output(url=args.url, json_output=args.json, timeout=args.timeout)

if __name__ == "__main__":
    main()