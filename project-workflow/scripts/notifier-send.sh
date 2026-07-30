#!/usr/bin/env bash
# notifier-send.sh — 通过 notifier 推送进度消息
# Usage: notifier-send.sh <sid> <message>

set -euo pipefail

CONFIG_FILE="${PROJECT_WORKFLOW_NOTIFIER_CONFIG:-/root/.openclaw/skills/code/opencode/scripts/notifier-config.env}"
if [[ -r "$CONFIG_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      NOTIFIER_URL)
        [[ -n "${NOTIFIER_URL:-}" ]] || NOTIFIER_URL="$value"
        ;;
      NOTIFIER_NOTIFY_TOKEN)
        [[ -n "${NOTIFIER_NOTIFY_TOKEN:-}" ]] || NOTIFIER_NOTIFY_TOKEN="$value"
        ;;
    esac
  done < "$CONFIG_FILE"
fi

# This helper only needs the least-privilege notify token. Do not let a
# higher-privilege token inherited from the caller reach jq or curl.
unset NOTIFIER_ADMIN_TOKEN

: "${NOTIFIER_URL:?Set NOTIFIER_URL or provide a readable notifier config file}"
: "${NOTIFIER_NOTIFY_TOKEN:?Set NOTIFIER_NOTIFY_TOKEN or provide a readable notifier config file}"

SID="${1:?Usage: notifier-send.sh <sid> <message>}"
MESSAGE="${2:?Missing: message}"

JSON_MSG=$(printf '%s' "$MESSAGE" | jq -Rs .)

RESP=$(curl -sf -X POST "${NOTIFIER_URL}/notify" \
  -H "Authorization: Bearer ${NOTIFIER_NOTIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"sid\":\"${SID}\",\"message\":${JSON_MSG}}" 2>&1) || {
    echo "WARN: notification send failed: $RESP" >&2
    exit 2
  }

echo "OK: Notification sent"
