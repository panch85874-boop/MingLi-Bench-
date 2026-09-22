#!/usr/bin/env bash
# iPrintOS FAQ 一鍵更新
# 用法：
#   bash scripts/update_faq.sh            # 只重新生成網頁與 Obsidian 筆記
#   bash scripts/update_faq.sh --deploy   # 生成後，再上傳到官網主機（需本機有 SSH 金鑰）
#
# 流程：改 data/faq_content.json → 跑本腳本 → 網頁(docs/faq.html)與筆記同步更新
set -euo pipefail

# 切到專案根目錄（不論從哪裡執行）
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
TODAY="$(date +%F)"

# 部署參數（如主機/路徑有變，改這裡即可）
SSH_KEY="${IPRINT_SSH_KEY:-/home/ai-agent/.ssh/id_rsa_do}"
SSH_HOST="${IPRINT_SSH_HOST:-root@152.42.167.42}"
REMOTE_PATH="${IPRINT_REMOTE_PATH:-/var/www/html/faq.html}"
FAQ_URL="https://iprinter.com.tw/faq.html"

echo "==> 1/2 生成網頁 docs/faq.html"
python3 scripts/build_faq.py

echo "==> 2/2 生成 Obsidian 筆記 docs/iPrintOS_FAQ_四語對照.md"
python3 scripts/build_faq_md.py "$TODAY"

echo "✅ 本機檔案已更新："
echo "   - docs/faq.html"
echo "   - docs/iPrintOS_FAQ_四語對照.md"

if [ "${1:-}" = "--deploy" ]; then
  echo
  echo "==> 上傳官網主機 ($SSH_HOST:$REMOTE_PATH)"
  if [ ! -f "$SSH_KEY" ]; then
    echo "❌ 找不到 SSH 金鑰：$SSH_KEY"
    echo "   （請在本機執行，或用 IPRINT_SSH_KEY 指定金鑰路徑）"
    exit 1
  fi
  scp -i "$SSH_KEY" docs/faq.html "$SSH_HOST:$REMOTE_PATH"
  echo "==> 驗證（期望 200）"
  curl -I "$FAQ_URL" 2>/dev/null | head -1 || true
  echo "✅ 已上線：$FAQ_URL"
else
  echo
  echo "👉 只更新了本機檔案。要同步上官網，請在本機執行："
  echo "   bash scripts/update_faq.sh --deploy"
  echo "   （或把改動 git push 後，由有金鑰的本機跑上面指令）"
fi
