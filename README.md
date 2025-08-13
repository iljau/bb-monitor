### bb_monitor.py

```
Task:
Create simple Python script to monitor external endpoints.
a. Input will be a URL (for example: https://www.delfi.ee/)
b. Outputs are:
i. Response code
ii. Result (if code 200 then OK, else NOK)
iii. Response time in ms.
```

```bash
# create virtual env
python -m venv .venv

# activate on linux
. venv/bin/activate
# activate on windows
.venv\Scripts\activate

# install dependendencies
pip install -r requirements.txt
```

```bash
# show help
python bb_monitor.py --help
# check url, output as a string
python bb_monitor.py https://google.com
# check url, output as a json
python bb_monitor.py https://google.com --json

# check url, timeout
python bb_monitor.py https://httpbin.org/delay/10 --json --timeout 2

# invalid parameter (python exception)
python bb_monitor.py google.com
python bb_monitor.py google.com --json --timeout 2
```