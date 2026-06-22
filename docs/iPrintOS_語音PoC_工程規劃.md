# iPrintOS 無人影印店 — 現場語音主動協助 PoC｜工程規劃文件

> 版本 v0.1（規劃稿）｜目標：**7 天內做出可測試 PoC**
> 定位：**無人自助影印店「現場操作助理」**，不是聊天客服。
> 紅線：所有模型輸出**只能進 Action Router 白名單**，不可直接操作交易、付款、退款、機台維修。

---

## 1. 一句話總結

在無人影印店機台前放一隻「語音耳朵」：聽懂客人卡在哪 → 分類成 7 種固定意圖 → 觸發 iPrintOS 既有白名單流程或轉人工，**降低現場求助電話與操作流失**，且**完全不碰錢與機台執行權**。

---

## 2. 系統架構（文字描述）

```
┌──────────────────────────── 機台端 (Kiosk / Edge) ────────────────────────────┐
│                                                                                │
│  [麥克風] → [VAD 語音活動偵測]  ──(偵測到人聲開口, 去背景噪音)──┐                │
│                                                               │                │
│                                              audio chunk (16k mono PCM)         │
│                                                               ▼                │
│                                                   [WebSocket 上行]              │
└───────────────────────────────────────────────────────────────┬──────────────┘
                                                                  │
┌──────────────────────────── 語音服務 (Voice Service) ──────────▼──────────────┐
│                                                                                │
│  [ASR Adapter]  ── faster-whisper (主力) / Nemotron (benchmark 對照)            │
│       │  text + confidence + latency                                           │
│       ▼                                                                        │
│  [Intent Classifier]  ── L1 關鍵詞規則 → L2 向量相似度 → (信心不足) unknown      │
│       │  {intent, score, slots}                                                │
│       ▼                                                                        │
│  [Action Router]  ★安全閘門★  只查白名單 intent→action 對照表                   │
│       │   ├─ 允許 → 回傳 action（切頁 / 播 TTS / 開升級單）                      │
│       │   └─ 不在白名單 / 低信心 / 客訴 → 強制走 human_help 或 complaint         │
│       ▼                                                                        │
│  ┌────────────┬───────────────┬──────────────────┐                            │
│  ▼            ▼               ▼                  ▼                            │
│ [TTS]    [Page Switch]   [Remote Escalation]  [Event Log]                      │
│ 短句語音  切 iPrintOS     通知遠端人工          記錄全鏈路                       │
│ 指引     測試頁面        (店/機台/時間/         (audio? text/intent/            │
│          (mock)         語音文字/意圖/畫面)     action/result)                  │
└────────────────────────────────────────────────────────────────────────────────┘
            │                                          │
            ▼                                          ▼
   [iPrintOS 後端規則引擎]                      [店主 / 客服 通知通道]
   (PoC 階段 = mock, 真執行權在此)              (LINE / Webhook / Dashboard)
```

**架構紅線（不可違反）**

- Action Router 是**唯一**能對外觸發動作的元件，且只走「白名單對照表」。
- ASR 與 Intent Classifier 永遠**只輸出資料**，不直接呼叫任何交易 / 機台 API。
- 任何「信心不足、未知意圖、客訴、涉及錢」→ 一律降級到 `human_help` / `complaint`，不自作主張。

---

## 3. 模組清單與責任

| # | 模組 | 責任 | PoC 實作方式 | 不負責 |
|---|---|---|---|---|
| M1 | Mic + VAD | 偵測開口、切句、過濾背景噪音與靜音 | `webrtcvad` 或 `silero-vad`；能量門檻 + 最短語音長度防誤觸發 | 不做喚醒詞、不做聲紋 |
| M2 | ASR Adapter | 語音→文字，輸出 text/confidence/latency；可切換引擎 | `faster-whisper`（主力，small/medium）；`nemotron` adapter 僅供 benchmark | 不做語意判斷 |
| M3 | Intent Classifier | 文字→7 類意圖之一或 `unknown` | L1 關鍵詞規則 + L2 句向量相似度（`bge-small-zh` / `text2vec`）；門檻以下 = unknown | 不執行動作、不下結論 |
| M4 | Action Router ★ | 安全閘門：查白名單、決定 action、強制降級 | 純規則表（JSON / dict），無 LLM 參與決策 | **不接付款 / 退款 / 機台維修** |
| M5 | TTS | 把固定指引語句轉語音播放 | 邊緣 `piper`（繁中）或雲端 TTS；PoC 可先用預錄音檔 | 不生成自由台詞（只播固定句庫） |
| M6 | Page Switch | 切 iPrintOS 測試頁（手機列印 / 證件 / 掃描教學頁） | PoC = 切換本地 mock 頁面（URL/route 事件） | 不操作正式機台 UI |
| M7 | Remote Escalation | 產生人工升級事件並送出 | Webhook / LINE Notify；含完整現場快照欄位 | 不替人工回覆、不關單 |
| M8 | Event Log | 記錄全鏈路供 benchmark 與稽核 | SQLite（PoC）→ 後續換 D1 / Postgres | — |
| M9 | Orchestrator | 串接 M1–M8 的 WebSocket 服務 + 狀態機 | FastAPI + websockets | — |

---

## 4. Intent Schema（JSON 草案）

```json
{
  "schema_version": "0.1",
  "intents": [
    {
      "id": "print_mobile",
      "desc": "手機 / 雲端檔案列印",
      "examples": ["我要印手機裡的檔案", "LINE 的檔案怎麼印", "手機可以列印嗎", "我要傳檔案來印"],
      "keywords": ["手機", "LINE", "傳檔", "上傳", "雲端", "照片印"],
      "action": "show_page_mobile_print",
      "needs_human": false
    },
    {
      "id": "copy_id",
      "desc": "身分證 / 證件影印",
      "examples": ["我要印身分證", "證件正反面怎麼印", "健保卡可以印嗎", "雙面證件影印"],
      "keywords": ["身分證", "證件", "健保卡", "正反面", "雙面印"],
      "action": "show_page_id_copy",
      "needs_human": false
    },
    {
      "id": "scan",
      "desc": "掃描到 Email / USB",
      "examples": ["我要掃描到信箱", "我要掃描文件", "可以掃到 USB 嗎", "掃描怎麼用"],
      "keywords": ["掃描", "掃瞄", "信箱", "email", "USB", "隨身碟"],
      "action": "show_page_scan",
      "needs_human": false
    },
    {
      "id": "payment",
      "desc": "付款問題（操作層級，不含退款）",
      "examples": ["怎麼付款", "我付款了沒出紙", "可以用悠遊卡嗎", "投幣在哪裡"],
      "keywords": ["付款", "付錢", "投幣", "悠遊卡", "扣款", "沒出紙"],
      "action": "show_page_payment_help",
      "needs_human": false,
      "note": "若同時偵測到『扣錢/退款/賠』等字 → 由 Router 升級為 complaint"
    },
    {
      "id": "machine_error",
      "desc": "機台故障（卡紙 / 缺紙 / 印壞）",
      "examples": ["卡紙了", "沒紙了", "印出來是空白的", "機器當機了"],
      "keywords": ["卡紙", "沒紙", "缺紙", "印壞", "空白", "當機", "壞掉"],
      "action": "notify_store_owner",
      "needs_human": true
    },
    {
      "id": "human_help",
      "desc": "主動找人工",
      "examples": ["我要找人", "可以幫我嗎", "有沒有人", "請問怎麼用"],
      "keywords": ["找人", "幫我", "有人嗎", "客服", "怎麼用"],
      "action": "escalate_human",
      "needs_human": true
    },
    {
      "id": "complaint",
      "desc": "客訴 / 抱怨 / 涉及金錢爭議",
      "examples": ["我被扣錢", "我要退款", "這台不能用", "我要客訴"],
      "keywords": ["扣錢", "退款", "退費", "賠", "客訴", "投訴", "亂扣"],
      "action": "escalate_human_priority",
      "needs_human": true
    },
    {
      "id": "unknown",
      "desc": "系統保留：低信心 / 無法分類 / 雜訊",
      "examples": [],
      "keywords": [],
      "action": "ask_repeat_then_escalate",
      "needs_human": false,
      "note": "連續 2 次 unknown → 自動降級 human_help"
    }
  ],
  "routing": {
    "min_confidence": 0.55,
    "below_confidence_action": "ask_repeat_then_escalate",
    "money_dispute_keywords": ["退款", "退費", "扣錢", "賠", "亂扣"],
    "money_dispute_override": "complaint"
  }
}
```

> 註：原始需求列 7 類，這裡額外加 `unknown` 作為**系統保留意圖**，是誤觸發控制與安全降級的關鍵，不算對外功能。

---

## 5. 事件流程範例 A：客人說「我要印手機檔案」

```
1. VAD 偵測開口 → 錄到 1.4s 語音 chunk → WS 上行
2. ASR(faster-whisper) → text="我要印手機裡的檔案"  conf=0.92  latency=380ms
3. Intent Classifier:
     L1 關鍵詞命中 "手機" → candidate=print_mobile
     L2 向量相似度=0.88 (> 0.55) → intent=print_mobile  score=0.88
4. Action Router:
     查白名單 print_mobile → action="show_page_mobile_print", needs_human=false → 允許
5. 並行執行:
     [Page Switch] 切到 mock 頁 /demo/mobile-print
     [TTS] 播 "好的，請依畫面用手機掃 QR Code 上傳檔案"
6. Event Log 寫入:
     {ts, store_id, kiosk_id, text, intent=print_mobile, score=0.88,
      action=show_page_mobile_print, asr_latency_ms=380, e2e_latency_ms=720,
      result=ok, escalated=false}
7. 結束（無人工介入）
```

端到端目標：**≤ 1s（理想 ≤ 500ms 進入 intent）**。

---

## 6. 事件流程範例 B：客人說「付款了沒出紙」

```
1. VAD → 語音 chunk → WS 上行
2. ASR → text="我付款了可是沒有出紙"  conf=0.85
3. Intent Classifier:
     L1 命中 "付款"+"沒出紙" → candidate=payment  score=0.81
4. Action Router（★安全降級判斷★）:
     a. payment.needs_human=false，但
     b. 偵測語句涉及「已付款但無產出」= 可能金錢損失情境
     c. routing 規則：payment + 出紙失敗語境 → 不自行判定，動作 = 同時
        - action="show_page_payment_help"（先給自助排查指引）
        - 並開 [Remote Escalation] 低優先升級單（讓店主可追）
     ❗不做：不退款、不承諾賠償、不判定機台故障原因
5. [TTS] 播 "我幫你通知店家確認這筆交易，請稍候；同時你可依畫面檢查出紙匣"
6. [Remote Escalation] 送出升級事件（見下方欄位）
7. Event Log 寫入完整鏈路，escalated=true, priority=low
```

**人工升級事件必含欄位（需求硬性要求）**

```json
{
  "event_id": "evt_20260622_1530_kiosk07",
  "store_id": "taipei_zhongshan_01",
  "kiosk_id": "kiosk07",
  "ts": "2026-06-22T15:30:12+08:00",
  "asr_text": "我付款了可是沒有出紙",
  "intent": "payment",
  "intent_score": 0.81,
  "screen_state": "page=payment, last_job=printing, paper_out=unknown",
  "action_taken": "show_page_payment_help + escalate_low",
  "priority": "low",
  "needs_human": true
}
```

---

## 7. ASR 測試計畫（Benchmark 方法）

**比較組**：`faster-whisper-small` / `faster-whisper-medium` / `Nemotron(對照)`
（Nemotron 系列對繁中台灣口音支援待驗證，列為對照而非主力。）

**評估指標**

| 指標 | 定義 | PoC 目標 |
|---|---|---|
| CER | 字元錯誤率（繁中用 CER 不用 WER） | medium ≤ 12%（乾淨）/ ≤ 20%（噪音） |
| Intent Hit Rate | 100 句進正確 intent 的比例 | **≥ 90%** |
| ASR Latency | 語音結束→文字 | ≤ 500ms（GPU medium）|
| E2E Latency | 語音結束→TTS 開始 | ≤ 1s |
| False Trigger Rate | 無人/背景音被當成指令 | 量化並設門檻，越低越好 |

**測試矩陣**：｛3 模型｝×｛乾淨 / 店內噪音（影印機運轉、人聲、冷氣）｝×｛100 句語料｝。
**流程**：固定語料 → 三模型各跑一輪 → 寫入 Event Log → 用同一支評分腳本算 CER/Intent Hit/Latency → 出對照表，選定 PoC 主力引擎。

---

## 8. 100 句測試語料分類方式

- **每類 ~13–15 句**，7 類共 ~100 句，覆蓋：標準說法 / 口語省略 / 台灣慣用詞 / 同義替換。
- 標註欄位：`text, gold_intent, style(標準|口語|台味), noise(clean|noisy), source(自錄|TTS合成)`。
- 三段難度：
  - **Easy**：含明確關鍵詞（「我要印身分證」）
  - **Medium**：口語/省略（「那個證件兩面的怎用」）
  - **Hard**：含干擾或情緒（「啊這個我剛剛付了錢欸怎麼沒東西」）
- **誤觸發專組（額外 ~20 句，不計入 100）**：純背景噪音、旁人閒聊、與影印無關的話 → gold=`unknown`，驗證 false trigger 控制。
- 儲存格式：`data/voice_poc/corpus.jsonl`，方便評分腳本直接讀。

---

## 9. 第一週開發排程（7 天可測 PoC）

| Day | 產出 | 驗收 |
|---|---|---|
| D1 | repo 骨架 + intent schema JSON + 100 句語料初稿 + Event Log（SQLite）schema | `pytest` 跑通 schema 載入；語料可讀 |
| D2 | ASR Adapter（faster-whisper）+ 離線評分腳本（CER/latency） | 餵 wav → 出文字 + 指標 |
| D3 | Intent Classifier（L1 關鍵詞 + L2 向量）+ 對 100 句出 Hit Rate | Intent Hit Rate 報表 |
| D4 | Action Router（白名單表 + 安全降級規則）+ 單元測試（含 complaint/money override） | 紅線案例全綠（不可觸發交易） |
| D5 | Orchestrator（FastAPI + WebSocket）串 VAD→ASR→Intent→Router；TTS 先用預錄音檔 | 麥克風講話 → 切 mock 頁 + 播音 |
| D6 | Remote Escalation（Webhook/LINE）+ mock iPrintOS 測試頁（手機列印/證件/掃描）| 升級事件含完整欄位送達 |
| D7 | 噪音情境測試 + Nemotron 對照跑分 + 出 benchmark 報表 + Demo 腳本 | 100 句 ≥ 90% intent、E2E ≤ 1s 抽測 |

**砍裁原則**：D1–D6 任何延遲，先砍 Nemotron 對照（移到後續）、TTS 先用預錄音檔，保住「能現場講一句→正確切頁/升級」這條主幹。

---

## 10. 風險清單與解法

| # | 風險 | 影響 | 解法 |
|---|---|---|---|
| R1 | Nemotron 繁中台灣口音支援弱 | 主力選錯、CER 高 | 主力用 faster-whisper，Nemotron 僅對照；D2 早驗證 |
| R2 | 店內噪音（影印機/人聲）誤觸發 | 客人沒講話卻動作 | VAD 能量門檻 + 最短語音長度 + unknown 降級 + false trigger 專組測試 |
| R3 | 邊緣機算力不足達不到 500ms | 體驗差 | PoC 先在 GPU 開發機 / 每店一台小推論盒；CPU 退而求其次用 small + 串流 |
| R4 | LLM/模型越權操作交易 | **致命合規風險** | 架構紅線：只走 Action Router 白名單，模型不持有任何執行 API；D4 紅線測試 |
| R5 | 付款爭議被自動判定 | 賠償/客訴風險 | payment 涉錢語境一律不下結論，走升級 + 自助指引雙軌 |
| R6 | 客人隱私（錄音含個資） | 法遵風險 | PoC 預設只存文字+指標，不存原始音檔（或存後限時刪）；現場告示告知 |
| R7 | 7 類涵蓋不足 | 大量 unknown | 連續 2 次 unknown 自動轉人工；蒐集 unknown 語料迭代 |
| R8 | TTS 自由生成不當內容 | 亂承諾 | 只播固定句庫，不讓模型自由生成台詞 |

---

## 11. 第一版「不做」事項（明確劃線）

- ❌ 不接正式付款、不處理金流
- ❌ 不決定退款 / 退費 / 賠償
- ❌ 不承諾任何補償
- ❌ 不改動正式機台流程、不操作正式機台 UI
- ❌ 不讓 LLM 自由操作機台或自由生成回覆台詞
- ❌ 不讓模型判斷維修結論（卡紙原因、是否故障由人工/後端規則定）
- ❌ 不做喚醒詞、聲紋辨識、多輪自由對話、閒聊
- ❌ 不串接真實 iPrintOS 後端交易 API（PoC 用 mock）

---

## 12. 下一步若要實作：先建立的檔案與 API

**建議目錄結構（新獨立模組，與既有 benchmark 隔離）**

```
iprintos_voice/
├── README.md
├── requirements.txt              # faster-whisper, webrtcvad/silero, fastapi, websockets, sentence-transformers
├── config/
│   └── intents.json              # §4 intent schema（單一事實來源）
├── data/
│   └── voice_poc/
│       ├── corpus.jsonl          # §8 100 句語料 + 誤觸發專組
│       └── audio/                # 測試 wav（git-ignored）
├── src/iprintos_voice/
│   ├── vad.py                    # M1 切句 + 噪音門檻
│   ├── asr/
│   │   ├── base.py               # ASRAdapter 介面: transcribe(audio)->{text,conf,latency}
│   │   ├── whisper_adapter.py    # 主力
│   │   └── nemotron_adapter.py   # 對照
│   ├── intent.py                 # M3 L1+L2 分類器
│   ├── router.py                 # M4 ★安全閘門★ 白名單 + 降級規則
│   ├── tts.py                    # M5 固定句庫播放
│   ├── escalation.py             # M7 升級事件
│   ├── event_log.py              # M8 SQLite
│   └── server.py                 # M9 FastAPI + WebSocket 狀態機
├── mock_iprintos/                # M6 假測試頁: mobile-print / id-copy / scan
└── tests/
    ├── test_intent.py            # 100 句 Hit Rate
    ├── test_router_safety.py     # 紅線: 任何輸入都不可觸發交易/退款
    └── benchmark_asr.py          # §7 三模型對照
```

**第一版 API（PoC）**

| 方法 | 路徑 | 用途 |
|---|---|---|
| `WS` | `/ws/audio?store_id=&kiosk_id=` | 上行音訊 chunk；下行 `{action, tts_text, page}` |
| `POST` | `/v1/intent` | 文字→意圖（離線評分/測試用）`{text}→{intent,score}` |
| `POST` | `/v1/route` | 意圖→動作（測 Router 白名單）`{intent,context}→{action,needs_human}` |
| `POST` | `/v1/escalate` | 產生人工升級事件（§6 欄位） |
| `GET` | `/v1/events` | 查 Event Log（稽核/benchmark） |
| `GET` | `/healthz` | 健康檢查 |

**最先動工的 3 個檔案（決定成敗）**

1. `config/intents.json` — 唯一事實來源，schema/keywords/白名單/降級規則都在這。
2. `src/iprintos_voice/router.py` — 安全紅線，先寫 `test_router_safety.py` 再寫實作（TDD）。
3. `tests/benchmark_asr.py` + `data/voice_poc/corpus.jsonl` — 沒有語料與評分，benchmark 與 90% 目標無從談起。

---

### 給工程師的一句話

> 先把「**講一句話 → VAD 切句 → ASR → intent → Router 白名單 → 切 mock 頁 / 開升級單 → 寫 log**」這條最短主幹打通（D5 前），再談模型對照與噪音優化。**Router 的紅線測試先寫**，這是整個 PoC 唯一不能妥協的地方。
