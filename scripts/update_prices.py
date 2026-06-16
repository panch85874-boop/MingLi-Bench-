#!/usr/bin/env python3
"""每日抓取台股收盤價,更新 game/prices.json。

資料來源(皆為公開 OpenAPI,伺服器端抓取無 CORS 問題):
  - 上市(TWSE): https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL
  - 上櫃(TPEx): https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes

抓不到的個股會沿用既有 prices.json 的舊值,確保資料不缺漏。
僅供遊戲娛樂計算,非投資建議。
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

# 與遊戲輪盤一致的股票代號
CODES = [
    "5274", "6515", "7556", "6223", "2308", "3665", "8027", "1519", "5289",
    "2338", "6669", "2360", "3324", "6805", "2059", "2330", "4749", "5536",
    "5434", "3443", "3533", "1590", "2383", "3017", "8996", "5269", "3661",
    "2345", "6531", "8210", "3529", "7750", "6274", "7777", "8299", "5328",
    "3131", "3035", "3653",
]

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


def collect(records, code_key_opts, close_key_opts, wanted):
    out = {}
    for rec in records or []:
        code = pick(rec, *code_key_opts)
        if code is None or str(code).strip() not in wanted:
            continue
        price = to_float(pick(rec, *close_key_opts))
        if price and price > 0:
            out[str(code).strip()] = price
    return out


def main():
    wanted = set(CODES)
    prices = {}

    for label, url, code_keys, close_keys in [
        ("TWSE", TWSE_URL, ("Code",), ("ClosingPrice", "Close")),
        ("TPEx", TPEX_URL, ("SecuritiesCompanyCode", "Code"), ("Close", "ClosingPrice")),
    ]:
        try:
            data = fetch_json(url)
            got = collect(data, code_keys, close_keys, wanted)
            prices.update(got)
            print(f"{label}: 取得 {len(got)} 檔收盤價")
        except Exception as e:  # noqa: BLE001
            print(f"{label} 抓取失敗: {e}", file=sys.stderr)

    # 沿用舊值補齊缺漏的個股
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                old = json.load(f).get("prices", {})
            for c in CODES:
                if c not in prices and c in old:
                    prices[c] = old[c]
        except Exception:  # noqa: BLE001
            pass

    if not prices:
        print("沒有取得任何股價,放棄更新(保留舊檔)。", file=sys.stderr)
        sys.exit(1)

    as_of = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    payload = {"asOf": as_of, "prices": prices}
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"已更新 {len(prices)} 檔股價,日期 {as_of} → {os.path.normpath(OUT_PATH)}")


if __name__ == "__main__":
    main()
