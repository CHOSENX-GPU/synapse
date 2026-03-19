---
name: codex-bridge
description: |
  Bridge for calling Codex and Cursor from Claude Code. Provides MCP call format
  and shell fallbacks. Use when you need to delegate work to Codex or Cursor,
  or when plan-review/plan-execute/code-review need to invoke external agents.
---

# Codex Bridge

Provides two methods for Claude Code to call Codex and Cursor: MCP (preferred) and Shell fallback.

## Method 1: Codex MCP (Preferred)

Use the `codex` MCP tool with these parameters:

| Parameter            | Required | Description                                          |
|---------------------|----------|------------------------------------------------------|
| `PROMPT`            | Yes      | The instruction/prompt to send to Codex              |
| `cd`                | Yes      | Working directory for Codex to operate in            |
| `sandbox`           | No       | `"read-only"` for review, `"workspace-write"` for execution |
| `return_all_messages` | No     | `true` to get full conversation history              |
| `SESSION_ID`        | No       | Reuse to continue a previous conversation            |

### Example: Review call
```
Tool: mcp__codex__codex
PROMPT: "Review this code for security issues..."
cd: "/path/to/project"
sandbox: "read-only"
return_all_messages: true
```

### Example: Execution call
```
Tool: mcp__codex__codex
PROMPT: "Implement the authentication module as specified..."
cd: "/path/to/project"
sandbox: "workspace-write"
return_all_messages: true
```

### Multi-round conversations
Save the `SESSION_ID` from the first response. Pass it in subsequent calls to continue the conversation (e.g., for fix instructions after a failed review).

## Method 2: Shell Fallback

When MCP is unavailable, use the shell scripts in this plugin's `scripts/` directory.

### Codex CLI

```bash
bash <plugin-scripts-dir>/ask_codex.sh "<prompt>" <sandbox-mode> "<working-dir>"
```

Arguments:
1. `prompt` (required): The instruction to send
2. `sandbox-mode` (optional): `read-only` or `workspace-write` (default: `read-only`)
3. `working-dir` (optional): Directory to run in (default: current directory)

### Cursor CLI

```bash
bash <plugin-scripts-dir>/ask_cursor.sh "<prompt>" "<working-dir>"
```

Arguments:
1. `prompt` (required): The instruction to send
2. `working-dir` (optional): Directory to run in (default: current directory)

## Detecting MCP Availability

Before calling MCP, you can check availability:
```bash
claude mcp list 2>/dev/null | grep codex
```
If the codex MCP is not listed, fall back to shell scripts.

## Agent Roles

| Agent       | Role in Synapse Workflow                          |
|-------------|--------------------------------------------------|
| Claude Code | Orchestrator — plans, reviews, adjudicates, commits |
| Codex       | Executor/Reviewer — generates code, adversarial review |
| Cursor      | Alternative executor — works in worktrees independently |

## Setup

To install Codex MCP (one-time):
```bash
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

To verify:
```bash
claude mcp list
```
