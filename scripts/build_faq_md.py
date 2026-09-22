#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
從 data/faq_content.json 生成 Obsidian 友善的四語對照筆記
    docs/iPrintOS_FAQ_四語對照.md
與 build_faq.py 同一資料來源；改完 JSON 後一起重跑即可保持同步。
用法：python3 scripts/build_faq_md.py [更新日期 YYYY-MM-DD]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "faq_content.json")
OUT  = os.path.join(ROOT, "docs", "iPrintOS_FAQ_四語對照.md")

LANG_LABEL = {"zh": "🇹🇼 中文", "en": "🇬🇧 EN", "vi": "🇻🇳 VI", "id": "🇮🇩 ID"}

def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "（生成時填）"
    d = json.load(open(DATA, encoding="utf-8"))
    codes = [l["code"] for l in d["langs"]]
    n = sum(len(s["items"]) for s in d["sections"])

    def line(field):
        out = []
        for c in codes:
            v = (field.get(c) or field.get("en") or field.get("zh") or "").strip()
            out.append(f"  - **{LANG_LABEL.get(c, c)}**：{v}")
        return "\n".join(out)

    L = []
    L.append("---")
    L.append("title: iPrintOS 四語 FAQ 對照")
    L.append("aliases: [iPrintOS FAQ, FAQ四語對照, FAQ]")
    L.append("tags: [iPrintOS, FAQ, 多語, 語音PoC, 客服]")
    L.append(f"languages: [{', '.join(codes)}]")
    L.append("source: data/faq_content.json")
    L.append("generators: [scripts/build_faq.py, scripts/build_faq_md.py]")
    L.append(f"sections: {len(d['sections'])}")
    L.append(f"items: {n}")
    L.append(f"updated: {date}")
    L.append("---")
    L.append("")
    L.append("# iPrintOS 四語 FAQ 對照（中 / 英 / 越 / 印）")
    L.append("")
    L.append(f"> **單一資料來源**：`data/faq_content.json`（共 {len(d['sections'])} 區、{n} 題、{len(codes)} 語）。")
    L.append("> 改內容：改 JSON → 跑 `python3 scripts/build_faq.py`（產網頁）與 `python3 scripts/build_faq_md.py`（產本筆記）。")
    L.append("> 線上網頁：https://iprinter.com.tw/faq.html")
    L.append("")
    # 目錄
    L.append("## 目錄")
    for s in d["sections"]:
        anchor = f"{s['icon']} {s['title']['zh']}".strip()
        L.append(f"- [[#{anchor}]]（{len(s['items'])} 題）")
    L.append("")

    for s in d["sections"]:
        L.append(f"## {s['icon']} {s['title']['zh']}".rstrip())
        sub = " / ".join(filter(None, [s["title"].get(c, "") for c in codes if c != "zh"]))
        if sub:
            L.append(f"*{sub}*")
        L.append("")
        for it in s["items"]:
            L.append(f"### {it['q']['zh']}")
            L.append("**Q**")
            L.append(line(it["q"]))
            L.append("")
            L.append("**A**")
            L.append(line(it["a"]))
            L.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print(f"已生成 {OUT}：{len(d['sections'])} 區、{n} 題、{len(codes)} 語")

if __name__ == "__main__":
    main()
