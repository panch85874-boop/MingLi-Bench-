# iPrinter.com.tw × Cloudflare 設定檢查表

> 角色分工:**老潘手動操作**(登入 / 人機驗證 / 2FA / 改 nameserver / Dashboard 設定);
> **我負責指引、檢查、記錄、驗證**。不使用、不記錄、不寫入任何帳密 / Token / API Key。

## 🔐 安全(最優先)
- [ ] **更改 Cloudflare 密碼**(先前截圖明碼外洩)
- [ ] 開啟 **2FA**

## 🔎 目前現況(由公開 DNS 查得,2026-06-16)
- `iprinter.com.tw` A → `104.21.51.148`, `172.67.181.183`(Cloudflare anycast)
- `www.iprinter.com.tw` A → 同上(Cloudflare anycast)
- IPv6 → `2606:4700:3034::…`(Cloudflare)
- 判定:**網域已掛在 Cloudflare,zone 應為 Active,apex 與 www 皆已 Proxied(橘雲)**
## 🧱 已釐清的架構(2026-06-16)
- **官網主站**:`iprinter.com.tw` / `www` → Cloudflare(橘雲)→ **DigitalOcean 新加坡 Droplet `152.42.167.42`(Nginx)**
  - 網站根目錄:`/home/ai-agent/iprint_web_project/`(`index.html`、`assets/`…)
  - SSL:**Cloudflare Origin 憑證** → Cloudflare 端應設 **Full (strict)**
- **子網域**:`gw.iprinter.com.tw` / `line.iprinter.com.tw` → **Cloudflare Tunnel → 本機**(後台 / LINE Bot)
- **Google Drive `愛印iPrint_備份/index.html`** = 備份,非線上來源
- 結論:**不是 Cloudflare Pages**,是「Cloudflare 代理 → 傳統主機(DO 新加坡 Nginx)」

## 🎮 把遊戲放上官網(iprinter.com.tw/game/)
因為是 Nginx 傳統主機,做法 = 把遊戲檔放進網站根目錄的 `game/` 夾:
1. SSH 進 DO 主機(由老潘 / 有 SSH 的代理執行)
2. 建立資料夾:`/home/ai-agent/iprint_web_project/game/`
3. 上傳遊戲 **`index.html`**(建議用「完全自包含版」)到該夾
4. 開 `https://iprinter.com.tw/game/` 驗證
> 自包含版不依賴任何外部資源(Logo 內嵌、股價烤進檔案),最適合丟上 Nginx。

## ✅ 待你在 Dashboard 確認 / 設定
1. [ ] **Overview**:zone 顯示 **Active**;記下 Cloudflare 指派的 2 組 nameserver
2. [ ] **SSL/TLS → Overview**:確認為 **Full (strict)**(已用 Cloudflare Origin 憑證)— ⚠️ 不要用 Flexible
4. [ ] **canonical(擇一,建議 apex)**:`www.iprinter.com.tw` **301 →** `https://iprinter.com.tw/`
       - Rules → **Redirect Rules** → Create:
         - When: `http.host eq "www.iprinter.com.tw"`
         - Then: Dynamic redirect, 狀態 **301**,目標 `concat("https://iprinter.com.tw", http.request.uri.path)`,**Preserve query string** 開
5. [ ] **DNS → Records**:確認 **MX / SPF(TXT)/ DKIM / DMARC / Google·Meta 驗證** 全部保留,且為 **DNS only(灰雲)**
6. [ ] 動任何 DNS 前先**截圖/匯出**整份紀錄備份

## 🧪 驗證指令(PowerShell,跑完把結果貼給我)
```
nslookup -type=ns iprinter.com.tw 1.1.1.1
nslookup iprinter.com.tw 1.1.1.1
nslookup www.iprinter.com.tw 1.1.1.1
curl.exe -I https://iprinter.com.tw/
curl.exe -I https://www.iprinter.com.tw/
curl.exe -I https://www.iprinter.com.tw/   # 應看到 301 Location: https://iprinter.com.tw/
```

## 🎯 成功標準
- [ ] apex 可開、HTTPS 無憑證錯誤
- [ ] www 可開或正確 301 → apex
- [ ] zone Active(若用 Pages,custom domain Active)
- [ ] Email DNS 未被破壞
- [ ] 首頁 / robots.txt / sitemap.xml 可開
- [ ] 無任何密碼 / Token / API Key 被寫入檔案
