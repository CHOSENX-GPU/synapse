#!/usr/bin/env bash
# Analyze staged diff and output structured info for commit message generation.
# Called by Claude Code during /commit to provide diff context.

set -euo pipefail

STAGED_FILES=$(git diff --cached --name-only)

if [ -z "$STAGED_FILES" ]; then
  echo "ERROR: No staged files"
  exit 1
fi

echo "=== STAGED FILES ==="
echo "$STAGED_FILES"
echo ""
echo "=== DIFF STAT ==="
git diff --cached --stat
echo ""
echo "=== DIFF CONTENT (first 200 lines) ==="
git diff --cached | head -200
