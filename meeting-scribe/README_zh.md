<div align="center">

# Meeting Scribe

**本地優先的錄音、會議記錄與知識庫整理工具。**

[English](./README.md) | 中文

</div>

---

## 這是什麼

一套 CLI 工具鏈，把「開會」到「找得到之前開會講過什麼」這整個流程串起來：

```
錄音 / 匯入音檔
     │
     ▼
語音轉文字（本地 faster-whisper 或雲端 Whisper API）
     │
     ▼
說話人辨識（選用，pyannote.audio）
     │
     ▼
AI 摘要：重點 / 決議 / 待辦事項（可換任何 LLM）
     │
     ▼
SQLite 儲存 + 全文檢索（含中文，逐字稿與摘要都可搜）
```

每個環節都是可替換的模組——STT 引擎、摘要用的 LLM、是否要分角色，全部由 `.env` 設定決定，不綁死特定供應商。

這是 [MingLi-Bench-](../) 儲存庫裡的一個獨立子目錄——有自己的依賴、測試與 `.env`，跟 `mingli_bench/` 完全沒有共用程式碼。

## 安裝

```bash
git clone https://github.com/panch85874-boop/MingLi-Bench-.git
cd MingLi-Bench-/meeting-scribe
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 編輯 .env：至少設定摘要用的 LLM API 金鑰（建議用 OPENROUTER_API_KEY，一組金鑰可用大多數模型）
```

語音轉文字預設用本地 `faster-whisper`（不需要 API 金鑰，也不需要網路），第一次執行時會下載模型檔。若要改用雲端 Whisper API，在 `.env` 設 `STT_ENGINE=api` 並填 `OPENAI_API_KEY`。

說話人辨識是選用功能：

```bash
pip install -r requirements-diarize.txt
```

並在 [huggingface.co/pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) 接受模型授權條款，把 token 填進 `.env` 的 `HUGGINGFACE_TOKEN`。

## 快速開始

```bash
# 1. 錄音（Ctrl+C 停止），或直接用手邊已有的錄音檔
python -m meeting_scribe.cli record -o data/audio/weekly.wav

# 2. 一次完成：轉文字 + AI 摘要 + 待辦事項擷取
python -m meeting_scribe.cli process data/audio/weekly.wav \
    --title "週會 2026-07-13" --diarize

# 3. 查看整理好的紀錄
python -m meeting_scribe.cli show 1

# 4. 之後想找「上次誰負責預算」
python -m meeting_scribe.cli search 預算
```

也可以分開跑：

```bash
python -m meeting_scribe.cli transcribe data/audio/weekly.wav --title "週會" --diarize
python -m meeting_scribe.cli summarize 1 --model anthropic/claude-sonnet-5
```

## CLI 指令

| 指令 | 說明 |
|---|---|
| `record` | 從預設麥克風錄音，Ctrl+C 或 `--duration` 停止 |
| `transcribe AUDIO` | 轉文字並建立一筆會議紀錄，`--diarize` 加上說話人分角色 |
| `summarize MEETING_ID` | 用 LLM 產生摘要、重點、決議、待辦事項 |
| `process AUDIO` | `transcribe` + `summarize` 一次完成 |
| `list` | 列出最近的會議 |
| `show MEETING_ID` | 顯示摘要／待辦／逐字稿（`--transcript` 顯示逐字稿）|
| `search QUERY` | 全文檢索所有會議的逐字稿與摘要 |
| `actions list` / `actions done ID` | 管理待辦事項 |
| `export MEETING_ID --format md\|json` | 匯出會議紀錄 |
| `stats` | 資料庫統計 |

每個指令都吃 `--env-file` 參數，可以指向不同的設定檔（例如給不同專案用不同的模型/資料庫）。

## 設定摘要用的模型

`SUMMARY_MODEL` 支援兩種寫法：

- `provider/model` 形式（例如 `anthropic/claude-sonnet-5`、`openai/gpt-4o`）→ 走 OpenRouter，一把金鑰用大多數模型
- 原生模型名稱（`claude-*` → Anthropic、`deepseek-*` → DeepSeek、`gpt-*` → OpenAI）→ 走對應的原生 API
- 其他名稱（例如自架 Ollama 的 `qwen2.5`、`llama3`）→ 走本地 `OLLAMA_BASE_URL`，不需要金鑰，完全離線

## 資料存在哪裡

所有會議、逐字稿、摘要、待辦事項都存在單一 SQLite 檔案（預設 `data/meetings.db`），並建立全文檢索索引（使用 FTS5 trigram tokenizer，對中文等無空格語言也能做子字串搜尋）。沒有外部資料庫、沒有雲端依賴——整套工具可以完全離線在自己的主機上跑。

## 開發

```bash
pip install -r requirements-dev.txt
pytest
```

## 授權

[MIT License](./LICENSE)
