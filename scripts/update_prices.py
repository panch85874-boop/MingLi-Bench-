#!/usr/bin/env python3
"""每日抓取台股「全部上市櫃股票」收盤價,取「股價最高的前 N 支」,
更新 game/prices.json(含代號、股名、收盤價)。

資料來源(皆為公開 OpenAPI,伺服器端抓取無 CORS 問題):
  - 上市(TWSE): https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL
  - 上櫃(TPEx): https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes

只收錄「普通股」(4 位數字代號、非 0 開頭的 ETF),自動排除 ETF/權證/特別股。
抓不到任何資料時保留舊檔。僅供遊戲娛樂計算,非投資建議。
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

TOP_N = 50   # 取股價最高的前 N 支

TWSE_URL = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
TPEX_URL = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "game", "prices.json")


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_float(v):
    try:
        return round(float(str(v).replace(",", "").strip()), 2)
    except (ValueError, AttributeError):
        return None


def pick(rec, *keys):
    for k in keys:
        if k in rec and rec[k] not in (None, "", "--"):
            return rec[k]
    return None


def is_common_stock(code):
    """普通股:4 位數字,且非 0 開頭(排除 0050 等 ETF)。"""
    return code.isdigit() and len(code) == 4 and code[0] != "0"


def collect(records, code_keys, name_keys, close_keys, out):
    for rec in records or []:
        code = pick(rec, *code_keys)
        if code is None:
            continue
        code = str(code).strip()
        if not is_common_stock(code):
            continue
        price = to_float(pick(rec, *close_keys))
        if not price or price <= 0:
            continue
        name = pick(rec, *name_keys)
        out[code] = {"code": code, "name": (str(name).strip() if name else code), "price": price}


def main():
    found = {}

    for label, url, code_keys, name_keys, close_keys in [
        ("TWSE", TWSE_URL, ("Code",), ("Name",),
         ("ClosingPrice", "Close")),
        ("TPEx", TPEX_URL, ("SecuritiesCompanyCode", "Code"),
         ("CompanyName", "SecuritiesCompanyName", "Name"), ("Close", "ClosingPrice")),
    ]:
        try:
            data = fetch_json(url)
            before = len(found)
            collect(data, code_keys, name_keys, close_keys, found)
            print(f"{label}: 取得 {len(found) - before} 檔普通股報價")
        except Exception as e:  # noqa: BLE001
            print(f"{label} 抓取失敗: {e}", file=sys.stderr)

    if not found:
        print("沒有取得任何股價,放棄更新(保留舊檔)。", file=sys.stderr)
        sys.exit(1)

    # 取股價最高的前 N 支
    stocks = sorted(found.values(), key=lambda s: -s["price"])[:TOP_N]
    prices = {s["code"]: s["price"] for s in stocks}  # 向後相容

    as_of = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    payload = {"asOf": as_of, "topN": TOP_N, "stocks": stocks, "prices": prices}
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    lo = stocks[-1]["price"] if stocks else 0
    print(f"已收錄股價最高前 {len(stocks)} 支(最低 {lo}),日期 {as_of}")


if __name__ == "__main__":
    main()

