#!/usr/bin/env bash
#
# Bootstrap a local WordPress dev environment for aurasoft.co.
#
# Brings up MariaDB, creates the database, writes wp-config.php (which is
# gitignored), and runs the WordPress install. Safe to re-run — each step
# is skipped if it is already done.
#
# Usage:  ./scripts/dev-setup.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DB_NAME="${WP_DB_NAME:-aurasoft_wp}"
DB_USER="${WP_DB_USER:-wp}"
DB_PASS="${WP_DB_PASS:-wp_local_dev}"
SITE_URL="${WP_SITE_URL:-http://localhost:8080}"
SITE_TITLE="${WP_SITE_TITLE:-Aurasoft}"
ADMIN_USER="${WP_ADMIN_USER:-admin}"
ADMIN_PASS="${WP_ADMIN_PASS:-admin_dev_pw}"
ADMIN_EMAIL="${WP_ADMIN_EMAIL:-only.arslan1@gmail.com}"

say() { printf '\n\033[1;34m==>\033[0m %s\n' "$1"; }

# The dev container runs as root, which WP-CLI refuses without an explicit
# opt-in. Add the flag only when we actually are root.
WP_FLAGS=()
[ "$(id -u)" -eq 0 ] && WP_FLAGS+=( --allow-root )
wp() { command wp "${WP_FLAGS[@]}" "$@"; }

# --- MariaDB ---------------------------------------------------------------
# There is no systemd in the dev container, so the daemon is started directly.
say "Starting MariaDB"
if mariadb -u root -e "SELECT 1" >/dev/null 2>&1; then
  echo "already running"
else
  mkdir -p /var/run/mysqld
  chown mysql:mysql /var/run/mysqld
  nohup mariadbd-safe --skip-syslog >/tmp/mariadb.log 2>&1 &
  for _ in $(seq 1 20); do
    sleep 1
    mariadb -u root -e "SELECT 1" >/dev/null 2>&1 && break
  done
  mariadb -u root -e "SELECT 1" >/dev/null 2>&1 \
    || { echo "MariaDB failed to start; see /tmp/mariadb.log" >&2; exit 1; }
  echo "started"
fi

say "Creating database '$DB_NAME'"
mariadb -u root <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL

# --- WordPress -------------------------------------------------------------
say "Writing wp-config.php"
if [ -f wp-config.php ]; then
  echo "already exists (delete it to regenerate)"
else
  wp config create \
    --dbname="$DB_NAME" --dbuser="$DB_USER" --dbpass="$DB_PASS" \
    --dbhost=localhost --dbcharset=utf8mb4 --dbcollate=utf8mb4_unicode_ci \
    --extra-php <<'PHP'
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
define( 'SCRIPT_DEBUG', true );
define( 'DISALLOW_FILE_EDIT', true );
PHP
fi

say "Installing WordPress"
if wp core is-installed 2>/dev/null; then
  echo "already installed"
else
  wp core install \
    --url="$SITE_URL" --title="$SITE_TITLE" \
    --admin_user="$ADMIN_USER" --admin_password="$ADMIN_PASS" \
    --admin_email="$ADMIN_EMAIL" --skip-email
fi

say "Ready"
wp core version --extra
cat <<EOF

  Site:   $SITE_URL
  Admin:  $SITE_URL/wp-admin  ($ADMIN_USER / $ADMIN_PASS)

  Start the server with:  ./scripts/dev-server.sh

EOF
