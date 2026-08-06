#!/usr/bin/env bash
#
# Serve the site locally with PHP's built-in web server.
#
# Usage:  ./scripts/dev-server.sh [port]
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PORT="${1:-8080}"

if [ ! -f wp-config.php ]; then
  echo "wp-config.php is missing — run ./scripts/dev-setup.sh first." >&2
  exit 1
fi

echo "Serving http://127.0.0.1:$PORT  (Ctrl-C to stop)"
exec php -S "127.0.0.1:$PORT"
