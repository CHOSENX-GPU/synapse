#!/usr/bin/env bash
# Shell fallback for calling Codex CLI when MCP is unavailable.
# Usage: ask_codex.sh "<prompt>" [read-only|workspace-write] [working-dir]

set -euo pipefail

PROMPT="${1:?Usage: ask_codex.sh '<prompt>' [sandbox-mode] [working-dir]}"
SANDBOX="${2:-read-only}"
WORKDIR="${3:-.}"

cd "$WORKDIR"

if [ "$SANDBOX" = "read-only" ]; then
  codex --approval-mode suggest --quiet "$PROMPT"
elif [ "$SANDBOX" = "workspace-write" ]; then
  codex --approval-mode full-auto --quiet "$PROMPT"
else
  echo "ERROR: Invalid sandbox mode '$SANDBOX'. Use 'read-only' or 'workspace-write'."
  exit 1
fi
