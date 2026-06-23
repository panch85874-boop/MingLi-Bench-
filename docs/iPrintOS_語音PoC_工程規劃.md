# iPrintOS 無人影印店 — 現場語音主動協助 PoC｜工程規劃文件

> 版本 **v0.2**（已併入 10 項範圍決定）｜目標：**7 天內做出可測試 PoC**
> 定位：**無人自助影印店的「簡易問答型語音助理」**——功能上類似 AI 客服（回答客人簡單問題），但**封閉領域、只播固定答案、不自由閒聊、不碰交易**。
> 紅線：語音助理是一個**完全獨立的封閉問答盒**——聽 → 比對固定問答庫 → 有就播語音引導、沒有就說「資料庫沒有、無法處理」並結束。**不碰錢、不碰機台、不切畫面、不轉人工、不連 iPrintOS 後端。**

---

## 0. 範圍決定（v0.2 拍板）

| # | 主題 | 決定 |
|---|---|---|
| 1 | 部署 | 每店一台**落地 edge box**（店控主機旁） |
| 2 | 機台 | Windows + 瀏覽器（非觸控一體機）+ **外接 USB 指向性麥克風** |
| 3 | 對外動作 | **只用 TTS 語音引導**，不切畫面、不轉人工；無對應資料就停止並告知客人 |
| 4 | 語言 | **國語 + 英文**（外籍客） |
| 5 | ASR 位置 | **在地端為主**；落地主機預算受限才改雲端（ASR Adapter 可插拔切換） |
| 6 | ASR 引擎 | 第一版**只做 faster-whisper**；Nemotron 對照組延後 |
| 7 | 觸發方式 | 用**既有店內監視系統的「人員進入」訊號**觸發問候 → 開收音窗對答 |
| 8 | 後端串接 | **純獨立 FAQ**，v1 不連 iPrintOS 後端（唯讀串接留 v2） |
| 9 | 資料保存 | **只存文字 + 指標**，原始音檔即收即丟 |
| 10 | 本輪交付 | 規劃文件 + **100 句引導語庫**（見 `iPrintOS_語音引導語庫.md`） |

---

## 1. 一句話總結

監視系統偵測到客人走進無人影印店 → edge box 上的語音助理主動問候 → 聽客人講一句卡在哪 → 分類成 7 種固定意圖 → **播一段簡短的固定語音引導**；**比對不到就直說「這個我這邊沒有資料」並結束**。全程在地端、不碰錢、不碰機台、不轉人工。

---

## 2. 系統架構（文字描述）

```
┌─────────── 店內既有監視系統 (NVR / IP Cam, 從外往內照, 拍不到路人) ───────────┐
│   偵測到「有人進入」 ── ONVIF事件 / HTTP webhook / IO乾接點 / RTSP自判 ──┐      │
└──────────────────────────────────────────────────────────────────────┼──────┘
                                                                         │ presence signal
┌─────────────────────── 落地 edge box (Windows 店控主機旁) ─────────────▼──────┐
│                                                                                │
│  [M0 Presence Trigger] 收到「有人進入」→ 觸發問候                               │
│        │                                                                       │
│        ▼                                                                       │
│  [M5 TTS] 播問候語「您好，需要幫忙嗎?」（固定句庫, 在地端 piper）               │
│        │                                                                       │
│        ▼                                                                       │
│  [M1 VAD 收音窗] 開 5~10s 收音 (外接USB麥, 指向性, 去背景噪音)                  │
│        │  16k mono PCM                                                         │
│        ▼                                                                       │
│  [M2 ASR Adapter] faster-whisper (本地權重, 中/英自動偵測)                      │
│        │  text + lang + confidence + latency                                   │
│        ▼                                                                       │
│  [M3 Intent Classifier] L1 中英關鍵詞 → L2 多語句向量 → (低信心) unknown        │
│        │  {intent, score}                                                      │
│        ▼                                                                       │
│  [M4 Router] ★安全閘門★ 查問答庫白名單                                          │
│        │   ├─ 命中且有引導 → 回 guidance_id                                     │
│        │   └─ 未命中 / 低信心 / unknown → fallback「資料庫沒有, 無法處理」        │
│        ▼                                                                       │
│  ┌──────────────┬───────────────────┐                                         │
│  ▼              ▼                                                              │
│ [M5 TTS]    [M8 Event Log]                                                     │
│ 播固定引導   只存 text/intent/score/latency/guidance_id  (★不存音檔★)          │
│ 語音        SQLite (本地)                                                       │
└────────────────────────────────────────────────────────────────────────────────┘
```

**架構紅線（不可違反）**

- 語音助理**不連 iPrintOS 後端、不連金流、不連機台 Driver**。它是旁掛的獨立服務。
- M4 Router 只查「固定問答庫白名單」，命不中一律走 `fallback_no_data`，**不猜、不下結論、不轉人工**。
- M8 **只存文字與指標，永不存原始音檔**。
- 監視系統影像只用來產生「有人進入」這一個布林訊號，**語音端不取畫面、不做人臉辨識、不存 frame**（店家原有的安防錄影是另一套系統，與此無關）。

---

## 3. 模組清單與責任

| # | 模組 | 責任 | PoC 實作方式 | 不負責 |
|---|---|---|---|---|
| M0 | Presence Trigger | 收店內監視系統「有人進入」訊號 → 觸發問候 | 優先 ONVIF/HTTP webhook；備援 IO 乾接點；最後備援拉 RTSP 自判 | 不存畫面、不辨識人臉 |
| M1 | VAD 收音窗 | 問候後開 5~10s 收音，切句、去背景噪音 | `silero-vad` / `webrtcvad` + 指向性 USB 麥；最短語音長度防誤觸發 | 不做喚醒詞 |
| M2 | ASR Adapter | 語音→文字（中/英自動偵測），輸出 text/lang/conf/latency；可插拔本地/雲端 | `faster-whisper`（本地 small/medium）；雲端 adapter 為預算備援 | 不做語意判斷 |
| M3 | Intent Classifier | 文字→7 類意圖之一或 `unknown` | L1 中英關鍵詞 + L2 多語句向量（`bge-m3` / multilingual）；門檻以下=unknown | 不執行動作、不下結論 |
| M4 | Router ★ | 安全閘門：查問答庫白名單 → 回 guidance_id 或 fallback | 純規則表（讀 `intents.json` + `guidance` 庫），無 LLM 決策 | **不碰金流/機台/人工** |
| M5 | TTS | 播問候語 + 固定引導語（中/英） | 在地端 `piper`（繁中+英文）；PoC 可先用預錄音檔 | 不自由生成台詞（只播固定句庫） |
| M8 | Event Log | 記錄全鏈路供 benchmark 與稽核 | SQLite（本地）；**不含音檔** | — |
| M9 | Orchestrator | 串接 M0→M1→M2→M3→M4→M5 的狀態機服務 | FastAPI + WebSocket / 本地行程 | — |

> 對比 v0.1：**移除 M6 Page Switch**（不切畫面）、**移除 M7 Remote Escalation**（不轉人工）。**新增 M0 Presence Trigger**（鏡頭觸發）。

---

## 4. Intent Schema（JSON 草案 v0.2）

動作模型簡化為：命中 → `play_guidance`（指向引導語庫的 guidance group）；未命中 → `fallback_no_data`。**已移除 `needs_human` 與所有升級動作。**

```json
{
  "schema_version": "0.2",
  "lang": ["zh-TW", "en"],
  "intents": [
    {
      "id": "print_mobile",
      "desc": "手機 / 雲端檔案列印",
      "keywords_zh": ["手機", "LINE", "傳檔", "上傳", "雲端", "照片印", "QR", "掃碼"],
      "keywords_en": ["phone", "upload", "file", "qr", "print from phone"],
      "action": "play_guidance",
      "guidance_group": "print_mobile"
    },
    {
      "id": "copy_id",
      "desc": "身分證 / 證件影印（走 Copy via FTP 流程）",
      "keywords_zh": ["身分證", "證件", "健保卡", "駕照", "正反面", "雙面"],
      "keywords_en": ["id card", "id copy", "both sides", "passport"],
      "action": "play_guidance",
      "guidance_group": "copy_id"
    },
    {
      "id": "scan",
      "desc": "掃描到 Email / USB",
      "keywords_zh": ["掃描", "掃瞄", "信箱", "email", "USB", "隨身碟"],
      "keywords_en": ["scan", "email", "usb", "scan to"],
      "action": "play_guidance",
      "guidance_group": "scan"
    },
    {
      "id": "payment",
      "desc": "付款操作問題（不含退款爭議）",
      "keywords_zh": ["付款", "付錢", "怎麼付", "悠遊卡", "Line Pay", "掃碼付", "沒出紙"],
      "keywords_en": ["pay", "payment", "how to pay", "no print after pay"],
      "action": "play_guidance",
      "guidance_group": "payment"
    },
    {
      "id": "machine_error",
      "desc": "機台狀況（卡紙/缺紙/印壞）— 引導依螢幕自助 + 改用店內另外兩台機器",
      "keywords_zh": ["卡紙", "沒紙", "缺紙", "印壞", "空白", "當機", "壞掉"],
      "keywords_en": ["jam", "paper jam", "out of paper", "blank", "broken"],
      "action": "play_guidance",
      "guidance_group": "machine_error"
    },
    {
      "id": "human_help",
      "desc": "想找人 — v1 不轉接，語音引導操作 + 線上常見問題頁面",
      "keywords_zh": ["找人", "幫我", "有人嗎", "客服", "聯絡"],
      "keywords_en": ["help", "someone", "contact", "support"],
      "action": "play_guidance",
      "guidance_group": "human_help"
    },
    {
      "id": "complaint",
      "desc": "客訴/抱怨 — v1 固定致歉 + 引導手機操作頁面填聯絡資料自助申請退款/處理",
      "keywords_zh": ["扣錢", "退款", "退費", "賠", "客訴", "投訴", "亂扣"],
      "keywords_en": ["refund", "overcharge", "complaint", "money back"],
      "action": "play_guidance",
      "guidance_group": "complaint"
    },
    {
      "id": "unknown",
      "desc": "系統保留：低信心/無法分類/雜訊",
      "action": "fallback_no_data",
      "note": "連續 2 次 unknown → 播『您可以直接在機台螢幕操作，或參考線上常見問題頁面』後結束"
    }
  ],
  "routing": {
    "min_confidence": 0.55,
    "below_confidence_action": "fallback_no_data",
    "fallback_no_data_tts": {
      "zh": "抱歉，這個問題我這邊沒有資料；您可以直接在機台螢幕操作，或參考線上常見問題頁面。",
      "en": "Sorry, I don't have that info—you can use the on-screen menu or check our online FAQ."
    }
  }
}
```

> 註：核心原則為**無人店「自助優先、不靠真人」**。`machine_error` → 依螢幕自助 + 改用店內另外兩台機器；`complaint`/付款爭議 → 手機操作頁面填聯絡資料自助申請；`human_help` → 語音引導 + 線上常見問題頁面。唯一外部聯絡為火災/受傷等緊急 → 119/110。**全程不導真人客服電話。**

---

## 5. 事件流程範例 A：客人進門問「我要印手機檔案」

```
1. [M0] 監視系統送「有人進入」訊號 → edge box 收到
2. [M5] 播問候「您好，需要幫忙嗎?」(中) / 偵測到後續英文則切英文問候
3. [M1] 開 8s 收音窗 → 客人說「我要印手機裡的檔案」→ 切句
4. [M2] faster-whisper → text="我要印手機裡的檔案" lang=zh conf=0.92 latency=380ms
5. [M3] L1 命中「手機」→ L2 相似度 0.88 (>0.55) → intent=print_mobile
6. [M4] 查白名單 print_mobile → action=play_guidance, group="print_mobile"
        → 選該 group 的入口引導句 PM-01
7. [M5] 播 PM-01「好的，請拿手機掃描機台上的 QR Code，就能上傳檔案列印。」
8. [M8] 寫入 {ts, store_id, kiosk_id, text, intent=print_mobile, score=0.88,
        guidance_id=PM-01, asr_latency_ms=380, e2e_latency_ms=720, result=ok}
        ★不寫音檔★
9. 結束
```

端到端目標：**問候後客人講完 ≤ 1s 出聲引導（理想 ≤ 500ms 進入 intent）**。

---

## 6. 事件流程範例 B：客人說「付款了沒出紙」（v1 純 FAQ，不讀後端）

```
1~4. 同上：收音 → ASR → text="我付款了可是沒有出紙"
5. [M3] L1 命中「付款」「沒出紙」→ intent=payment  score=0.81
6. [M4] 查白名單 payment → action=play_guidance, group="payment"
        → 命中子題 PAY-07「付款後沒出紙」
   ❗v1 不讀 iPrintOS reconciliation（8-a），所以不查真實出紙狀態、不判斷、不退款
7. [M5] 播 PAY-07（固定引導，自助優先）:
        「請先確認出紙匣並稍等約 30 秒；若仍沒出紙，您可以直接改用旁邊
          另一台機器重印，或在手機操作頁面填寫聯絡資料申請退款處理。」
8. [M8] 寫入完整鏈路 (guidance_id=PAY-07)
9. 結束
```

> 對比 v0.1：不再開升級單、不再導真人電話、不再寫真實 `screen_state`。出紙失敗 → 引導**改用店內另一台重印**或**手機操作頁面自助申請退款**；金錢爭議（退款/被扣錢）→ 落到 `complaint` group，固定致歉 + 引導手機操作頁面填聯絡資料自助申請，**不承諾任何賠償**。
> （若日後 8 改為 (b) 唯讀串接，這裡才會插入「查 reconciliation 真實出紙狀態」的步驟——列為 v2。）

---

## 7. ASR 測試計畫（Benchmark 方法）

**第一版只跑 `faster-whisper`**（small vs medium 二選一）。Nemotron 對照延後（6-c）。

| 指標 | 定義 | PoC 目標 |
|---|---|---|
| CER | 字元錯誤率（繁中用 CER） | medium ≤ 12%（乾淨）/ ≤ 20%（噪音） |
| EN WER | 英文詞錯誤率 | ≤ 20%（短句） |
| Intent Hit Rate | 100 句測試語料進對 intent 的比例 | **≥ 90%** |
| ASR Latency | 語音結束→文字 | ≤ 500ms |
| E2E Latency | 語音結束→TTS 開始 | ≤ 1s |
| False Trigger | 收音窗內無有效指令被誤判 | 量化並設門檻 |

**測試矩陣**：｛small, medium｝×｛乾淨 / 店內噪音（影印機運轉、人聲、冷氣）｝×｛100 句測試語料（中+英）｝→ 選定 PoC 主力模型。

---

## 8. 兩份語料（務必分清楚）

> **這是兩個不同的東西，別混：**

1. **100 句測試語料**（`corpus.jsonl`）：模擬**客人會講的話**，用來驗證辨識率與 intent 命中率。欄位 `text, gold_intent, lang(zh|en), style(標準|口語|台味), noise(clean|noisy)`。含 7 類各 ~13 句 + 誤觸發專組（gold=unknown）。
2. **100 句引導語庫**（`iPrintOS_語音引導語庫.md` → 之後轉 `guidance.jsonl`）：**系統要播給客人的固定回答**。依 7 意圖分群，每句有 `guidance_id, intent, trigger 範例, 中文引導(TTS), English guidance`。**本輪已產出**。

---

## 9. 第一週開發排程（7 天可測 PoC）

| Day | 產出 | 驗收 |
|---|---|---|
| D1 | repo 骨架 + `intents.json` + `guidance.jsonl`（由引導語庫轉）+ Event Log schema | schema/guidance 載入測試通過 |
| D2 | ASR Adapter（faster-whisper, 中英）+ 離線評分腳本（CER/WER/latency） | 餵 wav → 出文字+指標 |
| D3 | Intent Classifier（L1 中英關鍵詞 + L2 多語向量）+ 100 句測試語料 + Hit Rate 報表 | Intent Hit Rate ≥ 90% |
| D4 | Router（白名單 + fallback_no_data）+ 安全測試（不可碰金流/機台/人工/後端） | 紅線案例全綠 |
| D5 | Orchestrator 狀態機：Presence(先用假訊號/按鍵模擬)→問候→VAD→ASR→Intent→Router→TTS | 講一句 → 正確播引導 |
| D6 | M0 真接監視訊號（ONVIF/HTTP/IO 擇一）+ TTS piper 中英固定句庫 | 有人進入 → 自動問候 → 對答 |
| D7 | 噪音情境測試 + benchmark 報表 + Demo 腳本 + 規格建議（edge box） | 100 句 ≥ 90%、E2E ≤ 1s 抽測 |

**砍裁原則**：M0 真接訊號（D6）若卡關，先用「按鍵/假訊號」模擬觸發，保住「有人→問候→講一句→正確引導」主幹；TTS 先用預錄音檔。

---

## 10. 風險清單與解法

| # | 風險 | 解法 |
|---|---|---|
| R1 | 監視系統不支援 ONVIF/RTSP/IO，訊號接不出來 | D6 前先驗證；接不出來就退用「機台旁按鍵」觸發；最後備援拉 RTSP 自判 |
| R2 | 收音窗內店內噪音誤辨 | 指向性 USB 麥 + VAD 能量門檻 + 最短語音長度 + 低信心走 fallback |
| R3 | 落地主機算力不足達不到 500ms | 用 faster-whisper small + 收窗式（非串流）；規格不足時 ASR 改雲端備援(5) |
| R4 | 模型越權碰金流/機台 | 架構上**根本不連** iPrintOS 後端/金流/Driver；D4 紅線測試 |
| R5 | 客人講真問題卻被「無資料」擋掉不滿 | 引導語庫盡量覆蓋常見問題（100 句）；machine_error → 改用另一台/螢幕自助；complaint → 手機操作頁面自助申請 |
| R9 | **語音導向的出口（退款入口、線上FAQ）尚未建置**，客人照講卻找不到地方去 | 見下方〈待開發相依清單〉；退款入口列 **P0**；FAQ 頁已由本 100 句語庫產出草稿（`docs/faq.html`）。**決策 1B：入口上線前退款類只導「改用另一台重印、不扣款」、不承諾現場退款**；扣款爭議致歉＋請客人保留交易紀錄 |
| R6 | 連續 unknown 造成鬼打牆 | 連 2 次 unknown → 播「建議改用機台螢幕操作或參考線上常見問題頁面」後結束收音窗 |
| R7 | TTS 自由生成不當內容 | 只播固定句庫，模型不生成台詞 |
| R8 | 鏡頭/音訊隱私疑慮 | 影像只取布林訊號不存 frame；音訊只存文字不存音檔；現場貼告示 |

**已確認的運作事實（決定引導語走向）**：
- F1：出紙失敗/印壞 **v1 無自動退款或重印機制** → 引導改用另一台重印，或手機操作頁面填聯絡資料自助申請退款。
- F2：缺紙/卡紙 **客人可依機台螢幕指示自行排除/加紙**。
- F3：退款/扣款爭議走 **iPrintOS 手機操作頁面填聯絡資料自助申請**（非真人）。⚠️ **此入口目前尚未建置，列為待開發（見下）。**
- F4：需要更多協助 → **線上常見問題頁面**（佔位 `〔線上FAQ〕`）；不導真人客服電話。⚠️ **此頁面目前尚未建置，列為待開發（見下）。**

### 待開發相依清單（語音引導語生效的前置條件）

> 引導語庫已寫成「目標狀態」措辭；下列兩項出口需建好，語音講出來才有對應落點。

| # | 項目 | 優先 | 說明 / 最小規格 | 負責 | 過渡方案（入口上線前） |
|---|---|---|---|---|---|
| D-A | **退款/聯絡自助入口**（iPrintOS 手機操作頁面內） | **P0** | 客人掃 QR 進入操作頁 → 「申請退款 / 回報問題」按鈕 → 表單欄位：訂單/交易時間、機台編號、問題類型（沒出紙/印壞/重複扣款）、聯絡方式（手機或 Email）、選填說明 → 送出後產生工單給店家核帳。對應語句：PAY-07/08/12/14、CMP-01/02/04/05/06/07/08 | iPrintOS 後端團隊 | **決策 1B：過渡期只導「改用旁邊另一台重印、不扣款」，不承諾現場退款**；扣款爭議致歉＋請客人保留交易紀錄＋告知線上申請即將開放 |
| D-B | **線上常見問題（FAQ）頁面** | P1 | 一頁式對外網頁，內容＝本 100 句語庫的問題與自助步驟，附 QR 貼在機台。對應語句：HLP-02/04/07/08、SYS-03/04、R6 | **我可直接由語庫產出 HTML/Markdown 草稿** | 未上線前 HLP 類以「**我語音引導操作 + 機台螢幕**」為主，FAQ 連結暫不播 |

> 佔位符 `〔線上FAQ〕` 待 D-B 上線後填入實際網址/QR。在 D-A、D-B 上線前，可在 `config/guidance.jsonl` 用旗標切換「過渡措辭／目標措辭」，避免語音導向不存在的頁面。
- A2：一店三台機器、**每台間隔約 1 公尺**（緊鄰），**不細分熱區**——監視系統偵測到有人進門即播問候，不分客人要用哪一台。**因機器緊鄰，「改用旁邊另一台機器」是硬體問題（卡紙/當機/印壞）的首選自助解法，客人移動成本極低。**

---

## 11. 第一版「不做」事項（明確劃線）

- ❌ 不切任何畫面（不推客人手機 session、不設輔助螢幕）
- ❌ 不轉人工、不開升級單（無資料就停止並告知）
- ❌ 不連 iPrintOS 後端（不讀付款/出紙/機台狀態）
- ❌ 不接金流、不決定退款、不承諾賠償
- ❌ 不操作機台、不碰 Fuji Driver / SNMP
- ❌ 不讓 LLM 自由操作或自由生成台詞（只播固定句庫）
- ❌ 不存原始音檔、不做人臉辨識、不存監視 frame
- ❌ 不做 Nemotron 對照（延後）、不做台語、不做多輪自由對話

---

## 12. 下一步若要實作：先建立的檔案與 API

```
iprintos_voice/
├── README.md
├── requirements.txt              # faster-whisper, silero-vad, fastapi, sentence-transformers, piper-tts, onvif-zeep(選)
├── config/
│   ├── intents.json              # §4 意圖 schema（白名單單一事實來源）
│   └── guidance.jsonl            # 由 iPrintOS_語音引導語庫.md 轉出（100 句）
├── data/voice_poc/
│   ├── corpus.jsonl              # §8 100 句『測試語料』（客人會講的話）
│   └── audio/                    # 測試 wav（git-ignored）
├── src/iprintos_voice/
│   ├── presence.py               # M0 收監視訊號（ONVIF/HTTP/IO/RTSP）
│   ├── vad.py                    # M1 收音窗
│   ├── asr/{base,whisper_adapter,cloud_adapter}.py   # M2 可插拔
│   ├── intent.py                 # M3 中英 L1+L2
│   ├── router.py                 # M4 ★白名單 + fallback_no_data★
│   ├── tts.py                    # M5 piper 固定句庫
│   ├── event_log.py              # M8 SQLite（不存音檔）
│   └── server.py                 # M9 狀態機
└── tests/
    ├── test_intent.py            # 100 句測試語料 Hit Rate
    ├── test_router_safety.py     # 紅線：任何輸入都不可碰金流/機台/人工/後端
    └── benchmark_asr.py          # §7 small vs medium
```

**第一版 API（本地）**

| 方法 | 路徑 | 用途 |
|---|---|---|
| `POST` | `/v1/presence` | 監視系統 webhook：`{store_id,kiosk_id,event:"person_in"}` → 觸發問候 |
| `WS` | `/ws/session?store_id=&kiosk_id=` | 問候後收音窗：上行音訊、下行 `{tts_text, guidance_id}` |
| `POST` | `/v1/intent` | 文字→意圖（離線測試）`{text}→{intent,score}` |
| `POST` | `/v1/route` | 意圖→引導（測白名單）`{intent}→{action,guidance_id}` |
| `GET` | `/v1/events` | 查 Event Log |
| `GET` | `/healthz` | 健康檢查 |

**最先動工的 3 個檔案（決定成敗）**
1. `config/intents.json` + `config/guidance.jsonl` — 白名單與 100 句引導語，唯一事實來源。
2. `src/iprintos_voice/router.py` — 安全紅線，先寫 `test_router_safety.py` 再寫實作（TDD）。
3. `tests/benchmark_asr.py` + `data/voice_poc/corpus.jsonl` — 沒語料與評分，90% 目標無從驗證。

---

### 給工程師的一句話

> 先把「**假裝有人進入 → 問候 → 講一句 → VAD → ASR → intent → Router 白名單 → 命中播引導 / 未命中播『無資料』 → 寫 log**」這條最短主幹打通（D5 前），D6 才接真實監視訊號。**Router 紅線測試先寫**：這套東西的唯一鐵則是——它連碰錢和機台的能力都沒有。
