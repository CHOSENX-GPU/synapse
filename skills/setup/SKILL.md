---
name: setup
description: |
  First-run setup for the Synapse plugin. Configures Codex MCP, updates global
  CLAUDE.md and settings.json, installs improved EARS hook, verifies compatibility.
  Use when the user says /setup, "setup synapse", "configure synapse",
  or after first installing the synapse plugin.
---

# Synapse Setup

One-time setup after installing the Synapse plugin. Configures the environment for multi-AI collaboration.

## Checklist

Run through each step. Skip any that are already configured.

### 1. Check Prerequisites

```bash
# Verify gh CLI
gh --version

# Verify git
git --version

# Check if Codex CLI is available
codex --version 2>/dev/null || echo "Codex CLI not found (optional — MCP is preferred)"

# Check if Cursor CLI is available
cursor --version 2>/dev/null || echo "Cursor CLI not found (optional)"
```

### 2. Install Codex MCP (if not already configured)

Check current MCP servers:
```bash
claude mcp list
```

If `codex` is not listed, install it:
```bash
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

Verify:
```bash
claude mcp list | grep codex
```

### 3. Update ~/.claude/CLAUDE.md

Append the following block to `~/.claude/CLAUDE.md` (preserve existing content):

```markdown

## Multi-AI Collaboration & Git Workflow Protocol (Synapse)

### Agent Roles
- **Claude Code**: orchestrator — planning, review adjudication, git operations, EARS management
- **Codex** (via MCP): executor/reviewer — code generation and adversarial review
- **Cursor** (via CLI or standalone): alternative executor — works in worktrees with spec documents

### Core Collaboration Rules
1. Non-trivial tasks: `/plan-review` first, then `/plan-execute`
2. Codex review stage must use read-only sandbox
3. All plans, reviews, execution records persist to `./plans/`
4. Key milestones auto-write EARS entries
5. One logical unit per commit, Conventional Commits format
6. Worktree switches require `.worktree-spec.md` update

### Codex MCP Call Convention
Tool: mcp__codex__codex | Required: PROMPT, cd | Review: sandbox="read-only" | Execute: sandbox="workspace-write"

### Available Synapse Skills
- `/plan-review` — create plan + adversarial review + iterative revision
- `/plan-execute` — delegate reviewed plan to executor agent
- `/code-review` — deep code review (supports cross-agent review)
- `/worktree create/list/switch/handoff/cleanup` — worktree lifecycle management
- `/commit` `/save` `/push` `/pr` `/squash-merge` — automated git operations
- `/ears-init` — project-aware EARS initialization
```

### 4. Update ~/.claude/settings.json

Merge `"mcp__codex__codex"` into the `allowedTools` array:

```json
{
  "allowedTools": [
    "mcp__codex__codex"
  ]
}
```

If `allowedTools` doesn't exist yet, create it. If it exists, append to the array.

### 5. Install/Upgrade EARS Hook (optional)

Check if the current EARS hook supports trace.md auto-discovery:
- Read `~/.claude/scripts/ears-trace.py`
- Look for the `find_trace_context` function

If the hook is missing or outdated (lacks auto-discovery):
1. Copy the improved hook from this plugin's `hooks/ears-trace.py` to `~/.claude/scripts/ears-trace.py`
2. Verify `~/.claude/settings.json` PostToolUse hook points to:
   ```json
   {
     "hooks": {
       "PostToolUse": [{
         "matcher": "Write|Edit|Bash",
         "hooks": [{
           "type": "command",
           "command": "python ~/.claude/scripts/ears-trace.py",
           "timeout": 10
         }]
       }]
     }
   }
   ```

The improved hook adds:
- **trace.md auto-discovery**: walks up the directory tree from the edited file to find the nearest trace.md
- **Context naming**: uses the directory name as context for rate limiting and prompts
- **Missing trace.md reminder**: prompts to create trace.md if none exists (5min cooldown)
- **Project-specific error patterns**: loads custom patterns from `ears-config.json` in the project root
- **Better file skipping**: ignores .claude/, .git/, __pycache__, node_modules/, trace.md itself

If the user prefers to keep their current hook, that's fine.

### 6. Verify EARS Compatibility

Confirm these files are intact and unmodified:

- `~/.claude/modules/ears-system.md` — EARS system description
- `~/.cursor/rules/ears-principles.mdc` — Cursor design principles
- `~/.cursor/rules/ears-knowledge-system.mdc` — Cursor EARS rules
- `~/.codex/AGENTS.md` — Codex global instructions

If any are missing, warn the user. Synapse skills complement EARS but do not replace it.

### 7. Verify Plugin Skills

List available skills to confirm Synapse is loaded:
```bash
claude skills list 2>/dev/null || echo "Check plugin installation"
```

Expected skills: plan-review, plan-execute, code-review, worktree-manager, git-workflow, codex-bridge, ears-init, setup.

## Post-Setup

After setup is complete, you can:
- Use `/ears-init` to set up EARS for the current project (recommended first step)
- Use `/worktree create feature-xxx` to start a new feature branch
- Use `/plan-review <task description>` to create and review a plan
- Use `/commit` to make Conventional Commits automatically
