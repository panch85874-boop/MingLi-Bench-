---
title: iPrintOS 專案現況
aliases: [專案現況, iPrintOS 現況, 工作紀錄]
tags: [iPrintOS, 專案現況, FAQ, 多語, 語音PoC, 部署]
status: FAQ 多語系統已完成、已上線
languages: [zh, en, vi, id]
branch: claude/iprintos-voice-poc-acn2c4
updated: 2026-06-29
---

# iPrintOS 專案現況

> iPrintOS 無人影印店「現場語音主動協助」PoC。本頁＝**給下次接手的記憶**，與根目錄 `CLAUDE.md` 的「專案現況」同步。
> 開發分支：`claude/iprintos-voice-poc-acn2c4`（所有變更推到此分支）。

## ✅ 已完成：FAQ 多語系統
- **單一資料來源**：[[#資料與生成]] `data/faq_content.json`（14 區、217 題，每題 zh/en/vi/id）。改內容只改這份。
- **四語**：中文 / English / Tiếng Việt（越南文）/ Bahasa Indonesia（印尼文）。
- **線上網址**：https://iprinter.com.tw/faq.html （已上線）。
- **語音語庫**：[[iPrintOS_語音引導語庫]] 升 v0.5，237 句補上越南文/印尼文兩欄（169 句沿用 FAQ 翻譯、68 句另翻）。

## 資料與生成
```
data/faq_content.json          ← 唯一資料源（四語）
  ├─ scripts/build_faq.py      → docs/faq.html（客人掃的網頁）
  └─ scripts/build_faq_md.py   → docs/iPrintOS_FAQ_四語對照.md（Obsidian 筆記）
scripts/update_faq.sh          ← 一鍵：重生成（加 --deploy 上官網）
```
- **改內容流程**：改 `faq_content.json` → `bash scripts/update_faq.sh --deploy`。
- **新增語言**：`faq_content.json` 的 `langs` 加一筆 + 各題補欄位即可，免改 HTML；未填欄位自動遞補英文。

## 部署
- 官網架構：Cloudflare →（橘雲）→ DO 新加坡 Nginx；檔案放 `/var/www/html/`。
- `faq.html` 上線路徑：`/var/www/html/faq.html`。
- **雲端 session 連不到主機（SSH 22 被擋）**，只能交付指令；需由**本機（有 `id_rsa_do` 金鑰）**執行上傳。**金鑰絕不進公開 repo。**
- 一鍵上傳（本機）：`bash scripts/update_faq.sh --deploy`。

## 店內宣導物（可列印）
- `docs/qr_sign.html` — 「掃我看 FAQ」門口/機台掃碼貼紙（A4）。
- `docs/poster_coupon.html` — 優惠碼三步驟告示（A4）。
- `docs/faq_qr.svg` / `docs/faq_qr.png` — FAQ QR（指向線上網址）。
- 對應 PDF：`docs/qr_sign.pdf`、`docs/poster_coupon.pdf`。

## 關聯筆記
- [[iPrintOS_FAQ_四語對照]] — 217 題四語對照
- [[iPrintOS_語音引導語庫]] — 語音答案側（v0.5 四語）
- [[iPrintOS_語音PoC_工程規劃]] — 工程規劃
- [[iPrintOS_比對模擬]] — 比對乾跑

## 📋 待辦
- `config/guidance.jsonl` 補 `tts_vi` / `tts_id`（語音實作用）。
- 退款自助入口 D-A（P0 待開發）。
- 考慮把專案搬到本機跑（可直接由本機上官網，免人工貼指令）。
- 視需要再加語言（如泰文）。
