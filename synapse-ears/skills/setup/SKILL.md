---
name: setup
description: |
  First-run setup for the synapse-ears plugin. Installs the improved EARS hook
  and verifies EARS compatibility. Use when the user says /setup, "setup ears",
  or after first installing the synapse-ears plugin.
---

# EARS Setup

One-time setup after installing the synapse-ears plugin. Installs the improved EARS hook and verifies compatibility.

## Checklist

Run through each step. Skip any that are already configured.

### 1. Check Prerequisites

```bash
# Verify git
git --version

# Verify Python (for the EARS hook)
python --version
```

### 2. Install/Upgrade EARS Hook

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

### 3. Verify EARS Compatibility

Confirm these files are intact and unmodified:

- `~/.claude/modules/ears-system.md` — EARS system description
- `~/.cursor/rules/ears-principles.mdc` — Cursor design principles (optional)
- `~/.cursor/rules/ears-knowledge-system.mdc` — Cursor EARS rules (optional)
- `~/.codex/AGENTS.md` — Codex global instructions (optional)

If any are missing, warn the user. The synapse-ears plugin complements EARS but does not replace it.

### 4. Verify Plugin Skills

List available skills to confirm synapse-ears is loaded:
```bash
claude skills list 2>/dev/null || echo "Check plugin installation"
```

Expected skills: ears-init, setup.

## Post-Setup

After setup is complete, run `/ears-init` in any project to set up project-specific EARS configuration.

## Companion Plugins

For the full Synapse workflow, consider installing these companion plugins:

| Plugin | Install Command | Adds |
|--------|----------------|------|
| synapse-review | `claude plugin install synapse@synapse-review` | `/plan-review`, `/code-review` |
| synapse-execute | `claude plugin install synapse@synapse-execute` | `/plan-execute` |
| synapse-worktree | `claude plugin install synapse@synapse-worktree` | `/worktree` commands |
| synapse-git | `claude plugin install synapse@synapse-git` | `/commit`, `/push`, `/pr` |
