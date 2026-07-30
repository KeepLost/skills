#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/notifier.env" <<'EOF'
NOTIFIER_URL=http://notifier.test
NOTIFIER_ADMIN_TOKEN=admin-test
NOTIFIER_NOTIFY_TOKEN=notify-test
EOF

cat > "$TMP_DIR/jq" <<'EOF'
#!/usr/bin/env bash
if [[ -n "${NOTIFIER_ADMIN_TOKEN:-}" ]]; then
  echo "admin token leaked to jq" >&2
  exit 90
fi
printf '"message"\n'
EOF

cat > "$TMP_DIR/curl" <<'EOF'
#!/usr/bin/env bash
if [[ -n "${NOTIFIER_ADMIN_TOKEN:-}" ]]; then
  echo "admin token leaked to curl" >&2
  exit 91
fi
case "$*" in
  *"Authorization: Bearer notify-test"*) ;;
  *)
    echo "notify token missing from request" >&2
    exit 92
    ;;
esac
printf '{}\n'
EOF

chmod +x "$TMP_DIR/jq" "$TMP_DIR/curl"

OUTPUT=$(env -i \
  PATH="$TMP_DIR:$PATH" \
  PROJECT_WORKFLOW_NOTIFIER_CONFIG="$TMP_DIR/notifier.env" \
  NOTIFIER_ADMIN_TOKEN="parent" \
  bash "$SCRIPT_DIR/notifier-send.sh" "sid-test" "message-test")

[[ "$OUTPUT" == "OK: Notification sent" ]]
