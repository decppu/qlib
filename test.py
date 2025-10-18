import requests

def _get_eastmoney():
    pn = 1
    _symbols = []
    while True:
        url = f"http://4.push2delay.eastmoney.com/api/qt/clist/get?pn={pn}&pz=100&fs=m:105,m:106,m:107&fields=f12"
        if pn % 5 == 0:
            print(f"fetching page {pn}...")
        resp = requests.get(url, timeout=None)
        if resp.status_code != 200:
            raise ValueError("request error")
        if not resp.json()["data"]:
            break

        try:
            _symbols.extend([_v["f12"].replace("_", "-P") for _v in resp.json()["data"]["diff"].values()])
        except Exception as e:
            print(f"request error: {e}")
            raise
        pn += 1

    if len(_symbols) < 8000:
        raise ValueError("request error: symbols num < 8000")

    return _symbols

# with open("eastmoney_symbols.txt", "w") as f:
#     symbols = _get_eastmoney()
#     for symbol in symbols:
#         f.write(symbol + "\n")

from yahooquery import Ticker
start = "2019-12-31 21:00:00-08:00"
end = "2020-12-30 21:00:00-08:00"

symbol = "AAAA"
interval = "1d"
_resp = Ticker(symbol, asynchronous=False).history(interval=interval, start=start, end=end)
print(_resp)