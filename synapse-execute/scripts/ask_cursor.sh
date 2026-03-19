#!/usr/bin/env bash
# Shell fallback for calling Cursor CLI when MCP is unavailable.
# Usage: ask_cursor.sh "<prompt>" [working-dir]

set -euo pipefail

PROMPT="${1:?Usage: ask_cursor.sh '<prompt>' [working-dir]}"
WORKDIR="${2:-.}"

cd "$WORKDIR"

cursor --command "$PROMPT"
