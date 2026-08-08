#!/usr/bin/env bash
# Call a WordPress MCP tool. Usage: mcp.sh <tool> '<json args>'
set -euo pipefail
TOOL="$1"; ARGS="${2:-{\}}"
curl -sS -X POST "https://aurasoft.co/wp-json/wp/v2/wpmcp/streamable" \
  -H "Authorization: Bearer $WP_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":9,\"method\":\"tools/call\",\"params\":{\"name\":\"$TOOL\",\"arguments\":$ARGS}}"
