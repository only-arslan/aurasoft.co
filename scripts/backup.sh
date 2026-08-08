#!/usr/bin/env bash
#
# Back up the two things git does not track: the database and wp-content/uploads.
#
# The repository holds WordPress core and the theme, but everything you build in
# the admin — The7's theme options, page layouts, menus, widgets, posts, users —
# lives in the database. Media lives in uploads/. Without both, a repo checkout
# restores the code and none of the site.
#
# Usage:
#   ./scripts/backup.sh              # database + uploads
#   ./scripts/backup.sh --db-only    # database only (fast, for quick snapshots)
#
# Output lands in backups/ (gitignored) as a timestamped pair.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DEST="${WP_BACKUP_DIR:-$ROOT/backups}"
KEEP="${WP_BACKUP_KEEP:-10}"
STAMP="$(date +%Y%m%d-%H%M%S)"
DB_ONLY=0
[ "${1:-}" = "--db-only" ] && DB_ONLY=1

say() { printf '\n\033[1;34m==>\033[0m %s\n' "$1"; }

WP_FLAGS=()
[ "$(id -u)" -eq 0 ] && WP_FLAGS+=( --allow-root )
wp() { command wp "${WP_FLAGS[@]}" "$@"; }

command -v wp >/dev/null 2>&1 || {
  echo "WP-CLI not found. Install it: https://wp-cli.org/#installing" >&2
  exit 1
}
[ -f wp-config.php ] || { echo "No wp-config.php in $ROOT — is this a WordPress root?" >&2; exit 1; }

mkdir -p "$DEST"

say "Backing up database"
# wp db export reads credentials from wp-config.php, so this works unchanged on
# the dev container and on the production host.
wp db export "$DEST/db-$STAMP.sql" --add-drop-table
gzip -f "$DEST/db-$STAMP.sql"
echo "$DEST/db-$STAMP.sql.gz ($(du -h "$DEST/db-$STAMP.sql.gz" | cut -f1))"

if [ "$DB_ONLY" -eq 0 ]; then
  say "Backing up uploads"
  if [ -d wp-content/uploads ]; then
    tar -czf "$DEST/uploads-$STAMP.tar.gz" -C wp-content uploads
    echo "$DEST/uploads-$STAMP.tar.gz ($(du -h "$DEST/uploads-$STAMP.tar.gz" | cut -f1))"
  else
    echo "no wp-content/uploads yet — skipping"
  fi
fi

# Keep the most recent $KEEP of each kind; old backups are the ones that fill a
# disk, and a full disk is its own outage.
say "Pruning to the last $KEEP of each kind"
for prefix in db uploads; do
  find "$DEST" -maxdepth 1 -name "$prefix-*.gz" -printf '%T@ %p\n' 2>/dev/null \
    | sort -rn | tail -n "+$((KEEP+1))" | cut -d' ' -f2- \
    | while read -r old; do echo "removing $(basename "$old")"; rm -f "$old"; done
done

say "Done"
ls -1t "$DEST" | head -6
cat <<EOF

  Restore with:  ./scripts/restore.sh $STAMP

  These files are gitignored on purpose — a database dump contains user emails
  and password hashes, and does not belong in version control. Copy them off
  this machine (that is the whole point of a backup).

EOF
