---
name: worktree-manager
description: |
  Manage git worktree lifecycle: create, list, switch, handoff, and cleanup.
  Use when the user says /worktree, "create worktree", "new branch workspace",
  "switch worktree", "handoff to agent", or needs to manage parallel branches.
---

# Worktree Manager

Manage git worktrees for parallel multi-agent development. Each worktree gets its own working directory, spec document, and EARS trace.

## Directory Convention

```
<project-root>/                    # Main worktree (main branch), shared config
├── .git/                          # Single git database
├── CLAUDE.md                      # Tier 3 project principles (shared)
├── KNOWN_ISSUES.md                # Tier 2 cross-task patterns
└── plans/                         # Plan files

<project-root>-worktrees/          # All worktrees live here (sibling of project root)
├── feature-auth/                  # worktree: feature/auth branch
│   ├── .worktree-spec.md          # Spec handoff document
│   └── traces/
│       └── feature-auth/
│           └── trace.md           # EARS Tier 1
└── bugfix-memory-leak/
    └── ...
```

## Commands

### /worktree create <branch-name> [--from <base-branch>] [--agent <agent-name>]

1. Determine the worktree parent directory: `<project-root>-worktrees/`
   - If the parent dir doesn't exist, create it
2. Run: `git worktree add ../<project>-worktrees/<branch-name> -b <branch-name> <base-branch>`
   - Default base-branch is `main` if not specified
3. Copy the worktree-spec.md template into the new worktree as `.worktree-spec.md`
   - Fill in `{branch-name}`, `{timestamp}` (ISO 8601), `{agent}` (default: "Claude Code")
4. Create `traces/<branch-name>/trace.md` in the new worktree with header:
   ```
   # EARS Trace: <branch-name>
   ```
5. If vibe-kanban is running (check `curl -s http://127.0.0.1:50556/api/health`), create a task card

### /worktree list

1. Run `git worktree list` to get all worktrees
2. For each worktree, read `.worktree-spec.md` and extract Status and Current Agent
3. Display as a table:
   ```
   | Branch | Status | Agent | Path | Last Activity |
   |--------|--------|-------|------|---------------|
   ```

### /worktree switch <branch-name> [--to-agent <agent-name>]

1. If current worktree has uncommitted changes, run `/save` (from git-workflow skill)
2. Update current worktree's `.worktree-spec.md` handoff notes
3. Change working directory to the target worktree
4. Read target worktree's `.worktree-spec.md` to restore context
5. Read target worktree's `traces/<branch>/trace.md` for recent EARS entries
6. If `--to-agent` specified, update the spec's Current Agent field
7. Report context summary to user

### /worktree handoff <branch-name> --to <agent-name>

1. Generate a summary of current work state from `.worktree-spec.md`
2. Extract key EARS entries from `traces/<branch>/trace.md`
3. Update `.worktree-spec.md`:
   - Set Current Agent to the target agent
   - Fill in Handoff Notes with completed work, encountered issues, recommendations
   - Update EARS Summary section
4. Auto-commit the spec update: `git add .worktree-spec.md && git commit -m "chore: handoff to <agent-name>"`
5. Output a handoff instruction block the user can paste into the target agent:
   ```
   ## Handoff: <branch-name> → <agent-name>
   Working directory: <worktree-path>
   Read .worktree-spec.md for full context.
   Pending tasks: <list>
   Key EARS findings: <summary>
   ```

### /worktree cleanup <branch-name>

1. Check if the branch has been merged to main: `git branch --merged main | grep <branch-name>`
2. If merged:
   - Archive `.worktree-spec.md` and `traces/` to a timestamped backup if desired
   - Run `git worktree remove <worktree-path>`
   - Run `git branch -d <branch-name>`
   - If vibe-kanban is running, move the task card to Done
3. If NOT merged:
   - Warn the user: "Branch <branch-name> has not been merged to main. Are you sure?"
   - Only proceed if user confirms

## EARS Integration

- `/worktree create` writes an EARS Checkpoint to the new worktree's trace.md
- `/worktree handoff` writes an EARS Checkpoint before handoff
- Knowledge files (KNOWN_ISSUES.md, CLAUDE.md) live in the main worktree; changes must be committed to main first, then rebased/merged into feature worktrees

## Vibe-Kanban Integration

Before any operation, check if vibe-kanban is running:
```bash
VK_HEALTH=$(curl -s "http://127.0.0.1:50556/api/health" 2>/dev/null)
```
If available, sync worktree operations to kanban board:
- create → new task card
- status change → update card status
- cleanup → archive card
