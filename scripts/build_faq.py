#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
從 data/faq_content.json 生成 docs/faq.html（多語）。
加語言：在 faq_content.json 的 "langs" 加一個 {code,label}，並把各題的該語言欄位填好，再跑：
    python3 scripts/build_faq.py
未填寫的語言欄位會自動以英文（再不行則中文）遞補，頁面永遠不會出現空白。
"""
import json, html, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "faq_content.json")
OUT  = os.path.join(ROOT, "docs", "faq.html")

def esc(s): return html.escape(s, quote=True)

def main():
    d = json.load(open(DATA, encoding="utf-8"))
    langs = d["langs"]
    codes = [l["code"] for l in langs]
    default = codes[0]

    def pick(field, code):
        """取某語言文字，空則以 en→zh 遞補"""
        v = (field or {}).get(code, "")
        if v.strip(): return v
        for fb in ("en", "zh"):
            if (field or {}).get(fb, "").strip(): return field[fb]
        return ""

    def ml(field, tag="span"):
        """產生多語 span：<span class="ml zh">..</span>..."""
        parts = []
        for c in codes:
            parts.append(f'<{tag} class="ml {c}">{esc(pick(field, c))}</{tag}>')
        return "".join(parts)

    # ---- 語言切換 CSS（只顯示目前語言）----
    show = ", ".join(f"body.lang-{c} .ml.{c}" for c in codes)
    css = f"""
  :root{{--bg:#f6f7f9;--card:#fff;--ink:#1c2430;--sub:#5b6675;--brand:#1664d8;--line:#e6e9ee}}
  *{{box-sizing:border-box}}
  body{{margin:0;font-family:-apple-system,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;-webkit-text-size-adjust:100%}}
  .ml{{display:none}} {show}{{display:inline}}
  header{{background:var(--brand);color:#fff;padding:20px 16px}}
  .wrap{{max-width:720px;margin:0 auto;padding:0 16px}}
  .topbar{{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}}
  .htext{{flex:1;min-width:0}}
  header h1{{margin:0 0 6px;font-size:22px;line-height:1.3}}
  header p{{margin:0;opacity:.9;font-size:14px}}
  .langsel{{flex:none;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.7);color:#fff;border-radius:20px;padding:7px 14px;font-size:14px;cursor:pointer}}
  .langsel option{{color:#1c2430}}
  .search{{margin:16px 0 8px}}
  .search input{{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:10px;font-size:16px}}
  .nav{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}}
  .chip{{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:18px;padding:6px 12px;font-size:13px;color:var(--brand);text-decoration:none}}
  .chip:active{{background:#eef4ff}}
  .note{{background:#fff7e6;border:1px solid #ffe1a8;border-radius:10px;padding:12px 14px;margin:14px 0;font-size:14px;color:#7a5a00}}
  .facts{{background:#eef4ff;border:1px solid #cfe0ff;border-radius:10px;padding:12px 14px;margin:12px 0;font-size:14px}}
  .steps{{background:#fff;border:2px solid var(--brand);border-radius:12px;padding:14px 16px;margin:10px 0 16px}}
  .steps .sh{{font-weight:700;color:var(--brand);font-size:16px;margin-bottom:8px}}
  .steps ol{{margin:0;padding-left:22px}}
  .steps li{{margin:6px 0;font-size:15px}}
  .steps .tip{{margin:10px 0 0;background:#fff7e6;border:1px solid #ffe1a8;border-radius:8px;padding:8px 12px;font-size:14px;color:#7a5a00;font-weight:600}}
  h2{{font-size:17px;margin:26px 0 10px;padding-left:10px;border-left:4px solid var(--brand);scroll-margin-top:12px}}
  details{{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:8px 0;overflow:hidden}}
  summary{{cursor:pointer;padding:13px 15px;font-weight:600;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:10px}}
  summary::-webkit-details-marker{{display:none}}
  .qtext{{flex:1}}
  summary::after{{content:"＋";color:var(--brand);font-weight:700;flex:none}}
  details[open] summary::after{{content:"－"}}
  .ans{{padding:0 15px 14px;color:var(--sub);font-size:15px}}
  footer{{color:var(--sub);font-size:13px;text-align:center;padding:30px 16px}}
  .qr{{text-align:center;margin:18px 0}}
  .qr .box{{display:inline-block;border:1px dashed var(--line);border-radius:10px;padding:24px 40px;color:var(--sub);font-size:13px;background:#fff}}
  mark{{background:#fff3b0}}
"""

    # ---- 語言下拉 ----
    opts = "".join(f'<option value="{l["code"]}">{esc(l["label"])}</option>' for l in langs)

    # ---- 導覽 chips ----
    nav = " ".join(
        f'<a href="#sec-{s["id"]}" class="chip">{ml({c: (s["icon"]+" "+pick(s["title"],c)).strip() for c in codes})}</a>'
        for s in d["sections"]
    )

    # ---- 三步驟 ----
    steps_li = "".join(f'    <li>{ml(st)}</li>\n' for st in d["ui"]["steps"])

    # ---- 區塊與題目 ----
    body = []
    for s in d["sections"]:
        body.append(f'  <h2 id="sec-{s["id"]}">{ml({c:(s["icon"]+" "+pick(s["title"],c)).strip() for c in codes})}</h2>')
        for it in s["items"]:
            body.append(
                f'  <details><summary><span class="qtext">{ml(it["q"])}</span></summary>'
                f'<div class="ans">{ml(it["a"])}</div></details>'
            )
        if s["id"] == "PRO":
            steps_block = (
                '  <div class="steps">\n'
                f'    <div class="sh">{ml(d["ui"]["steps_title"])}</div>\n'
                f'    <ol>\n{steps_li}    </ol>\n'
                f'    <p class="tip">{ml(d["ui"]["steps_tip"])}</p>\n'
                '  </div>'
            )
            # 把三步驟插在 PRO 標題後
            body.insert(len(body) - len(s["items"]), steps_block)
    body_html = "\n".join(body)

    page = f"""<!DOCTYPE html>
<html lang="{default}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>iPrintOS 自助列印 常見問題 FAQ</title>
<style>{css}</style>
</head>
<body class="lang-{default}">
<header><div class="wrap topbar">
  <div class="htext">
    <h1>{ml(d["ui"]["title"], "span")}</h1>
    <p>{ml(d["ui"]["subtitle"], "span")}</p>
  </div>
  <select class="langsel" onchange="setLang(this.value)">{opts}</select>
</div></header>

<div class="wrap">

  <div class="search"><input id="q" type="search" placeholder="{esc(pick(d["ui"]["search"], default))}" oninput="filterFAQ()"></div>

  <div class="nav">{nav}</div>

  <div class="note">{ml(d["ui"]["note"])}</div>

  <div class="facts">{ml(d["ui"]["facts"])}</div>

{body_html}

  <div class="qr"><div class="box">{ml(d["ui"]["qr_caption"])}</div></div>

</div>

<footer>{ml(d["ui"]["footer"])}</footer>

<script>
function setLang(c){{
  document.body.className = 'lang-'+c;
  document.documentElement.lang = c;
  try{{localStorage.setItem('faqLang', c);}}catch(e){{}}
  var sel=document.querySelector('.langsel'); if(sel) sel.value=c;
  window.scrollTo(0,0);
}}
(function(){{
  var c='{default}';
  try{{ c = localStorage.getItem('faqLang') || c; }}catch(e){{}}
  setLang(c);
}})();
function filterFAQ(){{
  var k=(document.getElementById('q').value||'').trim().toLowerCase();
  document.querySelectorAll('details').forEach(function(d){{
    var t=d.textContent.toLowerCase();
    d.style.display = (!k || t.indexOf(k)>=0) ? '' : 'none';
  }});
}}
</script>
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(page)
    n = sum(len(s["items"]) for s in d["sections"])
    print(f"已生成 {OUT}：{len(d['sections'])} 區塊、{n} 題、{len(codes)} 語（{','.join(codes)}）")

if __name__ == "__main__":
    main()
