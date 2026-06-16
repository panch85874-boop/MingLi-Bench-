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
- 未能從外部判定項目:實際部署(Pages / 傳統主機)、SSL 模式、www→apex 轉址、MX/SPF 等(需 Dashboard)

## ✅ 待你在 Dashboard 確認 / 設定
1. [ ] **Overview**:zone 顯示 **Active**;記下 Cloudflare 指派的 2 組 nameserver
2. [ ] **Workers & Pages**:是否有官網的 **Pages 專案**?
       - 有 → 這是 Pages 站;到該專案 **Custom domains** 確認 `iprinter.com.tw` 與 `www.iprinter.com.tw` 皆 **Active**
       - 沒有 → 官網是「Proxied 到傳統主機/其他服務」
3. [ ] **SSL/TLS → Overview**:設為 **Full (strict)**(origin 有有效憑證時;Pages 為自動)
       - ⚠️ 不要用 Flexible
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
