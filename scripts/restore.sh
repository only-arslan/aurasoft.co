#!/usr/bin/env bash
#
# Restore a backup produced by scripts/backup.sh.
#
# Usage:
#   ./scripts/restore.sh                    # restore the most recent backup
#   ./scripts/restore.sh 20260808-144500    # restore a specific timestamp
#   ./scripts/restore.sh --list             # show what is available
#
# This DROPS the current database before importing. It asks first.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DEST="${WP_BACKUP_DIR:-$ROOT/backups}"

say() { printf '\n\033[1;34m==>\033[0m %s\n' "$1"; }

WP_FLAGS=()
[ "$(id -u)" -eq 0 ] && WP_FLAGS+=( --allow-root )
wp() { command wp "${WP_FLAGS[@]}" "$@"; }

[ -d "$DEST" ] || { echo "No backups directory at $DEST" >&2; exit 1; }

if [ "${1:-}" = "--list" ]; then
  echo "Available backups in $DEST:"
  ls -1t "$DEST" 2>/dev/null | sed 's/^/  /'
  exit 0
fi

STAMP="${1:-}"
if [ -z "$STAMP" ]; then
  # Newest db dump wins when no timestamp is given.
  newest="$(ls -1t "$DEST"/db-*.sql.gz 2>/dev/null | head -1 || true)"
  [ -n "$newest" ] || { echo "No database backups found in $DEST" >&2; exit 1; }
  STAMP="$(basename "$newest" | sed 's/^db-//; s/\.sql\.gz$//')"
fi

DB_FILE="$DEST/db-$STAMP.sql.gz"
UP_FILE="$DEST/uploads-$STAMP.tar.gz"
[ -f "$DB_FILE" ] || { echo "No database backup for timestamp '$STAMP'. Try --list." >&2; exit 1; }

cat <<EOF

  About to restore:  $STAMP
    database: $DB_FILE
    uploads : $([ -f "$UP_FILE" ] && echo "$UP_FILE" || echo "(none in this backup)")

  This DROPS every table in the current database and replaces it.
EOF

read -r -p "  Type 'yes' to continue: " confirm
[ "$confirm" = "yes" ] || { echo "Aborted."; exit 1; }

say "Restoring database"
# Reset rather than import over the top, so tables removed since the backup do
# not survive the restore and leave a half-old schema.
wp db reset --yes
gunzip -c "$DB_FILE" | wp db import -

if [ -f "$UP_FILE" ]; then
  say "Restoring uploads"
  mkdir -p wp-content
  tar -xzf "$UP_FILE" -C wp-content
fi

say "Restored"
wp option get home
wp option get siteurl
cat <<'EOF'

  If this dump came from a different host, the URLs above will be wrong.
  Fix them with:

    wp option update home    'https://aurasoft.co'
    wp option update siteurl 'https://aurasoft.co'
    wp search-replace 'https://old-url.example' 'https://aurasoft.co' --skip-columns=guid

EOF
