# 愛印 iPrint × 黑猩猩射飛鏢 — 專案紀錄(定版 v1.0 / 2026-06-17)

> 一句話:把「黑猩猩射飛鏢選股」做成台股**前 50 高價股**轉盤小遊戲,當作 iPrint 粉專導流/品牌行銷工具。純娛樂,非投資建議。

---

## 1. 線上資訊
- **遊戲網址**:https://iprinter.com.tw/game/
- **官網**:https://iprinter.com.tw(+ www)
- **FB 粉專**:https://www.facebook.com/share/1CBgxx4Hio/
- **GitHub 原始碼**:panch85874-boop/MingLi-Bench-(分支 main;開發分支 claude/taiwan-stock-roulette-game-o8oxe8)

## 2. 架構(已查證)
- 網域 DNS:**Cloudflare**(橘雲 Proxy);Zone ID `fe7c4c5d45b027bacdcf324db8693431`;帳號 panch85874@gmail.com
- 官網主站:Cloudflare → **DigitalOcean 新加坡 Droplet `152.42.167.42`(Nginx, Ubuntu 24.04)**
  - 服務根目錄 **`/var/www/html/`**;遊戲在 **`/var/www/html/game/`**
  - SSL:Cloudflare Origin 憑證(建議 Cloudflare 端設 Full strict;origin 目前 HTTP:80)
- 子網域:`gw.` / `line.` → Cloudflare Tunnel → 本機(後台 / LINE Bot)
- 部署由「美編小潘 / OpenClaw」執行(持有 SSH 金鑰,Claude 不碰金鑰)

## 3. 部署方式(改版時才需要)
```bash
curl -L -o /var/www/html/game/index.html https://raw.githubusercontent.com/panch85874-boop/MingLi-Bench-/main/game/index.html
curl -L -o /var/www/html/game/promo-poster.png https://raw.githubusercontent.com/panch85874-boop/MingLi-Bench-/main/game/assets/promo-poster.png
curl -I https://iprinter.com.tw/game/   # 期望 200
```
- 純靜態檔,Nginx 立即生效、不需重啟。
- 已決定**不設自動同步排程**(快定版,改動少)。

## 4. 每日股價(全自動,無人工)
- **來源**:TWSE + TPEx 公開 OpenAPI(`scripts/update_prices.py`)
- **規則**:抓全市場普通股(排除 ETF/權證/特別股)→ 取**股價最高前 50 支**
- **排程**:GitHub Action `update-prices.yml`,cron `0 7 * * 1-5`(=台北 **每交易日 15:00**)→ 自動更新 `game/prices.json`
- **遊戲端**:開啟時 fetch GitHub raw `prices.json`(跨站 CORS OK),抓不到則用內建快照(自包含後備)
- 結論:**程式定版後不用再動;股價每天自動更新。**

## 5. 遊戲完整流程
1. 進場偵測:LINE→自動跳外部瀏覽器;FB/IG/WeChat/TikTok…→頂部「用瀏覽器開啟」提示(Android 一鍵 intent 跳 Chrome,iOS 引導手動)
2. 開場故事頁(馬基爾名言)→ 點畫面任一處開始
3. 選預算:**3萬 / 5萬 / 10萬**
4. 主畫面:前50高價股彩色輪盤 + 中央🐵 + 側欄(預算/已使用、TOP50按鈕、我射中了哪些股票、結束鈕、音效/分享、Logo)
5. 射飛鏢(點中央或輪盤任一處)→ 落點放大 5 秒(股名/代號/建議2~6股/最新股價×股數=金額/累計)
6. **累計 ≥ 預算 → 自動結束** → 跳「按讚送招財小卡」gate
7. 去粉專按讚 → 切回 → **全螢幕粉紅招財卡**(長按儲存/截圖,iOS 也能拿)→ 📤分享(卡圖+粉專連結)/ 🔄再玩一次

## 6. 關鍵決策
- 領卡邏輯:**先去粉專、回來才顯示卡**(卡=去粉專的獎勵,拉高點擊率)
- iOS 內建瀏覽器無法強制跳出 → 改「萬用版」:全螢幕看圖+長按/截圖(零流失)
- 招財卡:**鮮豔粉紅**主調 + 金色點綴
- 企業識別色:藍 `#3696d3`(取自 Logo)
- 分享連結用乾淨網址(站內自動處理 LINE 跳轉,不放 openExternalBrowser 參數以免觀感警戒)

## 7. 行銷素材
- **LINE 文案(22字)**:`🐵黑猩猩射飛鏢選台股!每日前50高價股,送招財小卡🧧`
- **連結**:`https://iprinter.com.tw/game/`
- FB 完整貼文 + 配圖建議:見 `game/PROMO.md`
- 宣傳海報:`game/assets/promo-poster.png`(1080×1520,含真實千金股輪盤 + 愛印 Logo)→ 已設為 og:image
- 待辦(下一步):FB 完整版發文、可規劃「按讚抽獎」(玩→按讚→截圖招財卡留言→tag好友)衝聲量

## 8. 重要檔案
| 檔案 | 用途 |
|---|---|
| `game/index.html` | 遊戲(單檔自包含,內嵌 Logo base64 + 股價快照,執行時抓最新) |
| `scripts/update_prices.py` | 每日抓全市場、取前50高價股 → prices.json |
| `.github/workflows/update-prices.yml` | 排程(台北15:00)自動更新股價 |
| `game/prices.json` | 當日前50高價股(代號/股名/收盤價) |
| `game/assets/iprint-logo.png` | 愛印 iPrint 商標 |
| `game/assets/promo-poster.png` | 宣傳海報 / og:image |
| `game/PROMO.md` | FB 宣傳貼文素材 |
| `CLOUDFLARE_SETUP.md` | Cloudflare/網域/部署檢查表 |

## 9. 限制與誠實備註
- 「按讚」無法程式驗證(信任制:只驗證「去了粉專」)。
- iOS 的 FB/IG/WeChat 內建瀏覽器**無法**強制跳外部(Apple/Meta 限制)→ 只能引導 + 萬用截圖拿卡。
- GitHub 排程若倉庫連續 60 天無任何提交會被自動暫停(偶有提交即正常;另有 workflow_dispatch 可手動觸發)。
