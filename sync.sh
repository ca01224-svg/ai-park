#!/bin/bash
# ============================================
# AIパク 2台同期スクリプト
# Usage: ./sync.sh [pull|push|status]
# ============================================

set -euo pipefail
cd "$(dirname "$0")"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

case "${1:-status}" in

  pull)
    echo -e "${GREEN}⬇ pull: リモートから最新を取得${NC}"
    git pull origin main --rebase
    echo -e "${GREEN}✅ 同期完了${NC}"
    ;;

  push)
    echo -e "${GREEN}⬆ push: 変更をリモートに反映${NC}"

    # 変更チェック
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
      echo -e "${YELLOW}変更なし。pushするものがないよ${NC}"
      exit 0
    fi

    # 差分表示
    echo ""
    echo "--- 変更ファイル ---"
    git status --short
    echo ""

    # 自動コミット＆プッシュ
    git add -A
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    git commit -m "sync: ${TIMESTAMP}"
    git push origin main
    echo -e "${GREEN}✅ push完了${NC}"
    ;;

  status)
    echo -e "${YELLOW}📋 現在の状態${NC}"
    echo ""

    # ローカル変更
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
      echo -e "ローカル: ${GREEN}クリーン（変更なし）${NC}"
    else
      echo -e "ローカル: ${RED}未コミットの変更あり${NC}"
      git status --short
    fi

    # リモートとの差分
    git fetch origin --quiet
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)

    if [ "$LOCAL" = "$REMOTE" ]; then
      echo -e "リモート: ${GREEN}同期済み${NC}"
    else
      BEHIND=$(git rev-list HEAD..origin/main --count)
      AHEAD=$(git rev-list origin/main..HEAD --count)
      [ "$BEHIND" -gt 0 ] && echo -e "リモート: ${YELLOW}${BEHIND}件の未取得コミットあり → ./sync.sh pull${NC}"
      [ "$AHEAD" -gt 0 ] && echo -e "リモート: ${YELLOW}${AHEAD}件の未pushコミットあり → ./sync.sh push${NC}"
    fi
    ;;

  *)
    echo "Usage: ./sync.sh [pull|push|status]"
    echo ""
    echo "  pull    リモートから最新取得"
    echo "  push    変更をコミット＆プッシュ"
    echo "  status  同期状態を確認（デフォルト）"
    ;;
esac
