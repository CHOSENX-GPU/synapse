# synapse-worktree

**Git worktree lifecycle management for parallel multi-agent development.**

Create, list, switch, handoff, and cleanup git worktrees with structured spec documents for seamless context transfer between AI agents.

## Installation

```bash
# Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# Install the worktree plugin
claude plugin install synapse@synapse-worktree
```

## Prerequisites

- **git** 2.20+ (for worktree support)

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **worktree-manager** | `/worktree` | Create, list, switch, handoff, and cleanup git worktrees |

## Commands

| Command | Description |
|---------|-------------|
| `/worktree create <branch> [--from <base>] [--agent <name>]` | Create a new worktree with spec document |
| `/worktree list` | List all worktrees with status and agent info |
| `/worktree switch <branch> [--to-agent <name>]` | Switch to another worktree, preserving context |
| `/worktree handoff <branch> --to <agent>` | Hand off a worktree to another agent |
| `/worktree cleanup <branch>` | Remove a merged worktree and its branch |

## Quick Start

### Create a Feature Branch

```
/worktree create feature-auth --from main --agent claude-code
```

### Parallel Development

```
/worktree create feature-auth --agent claude-code
/worktree create feature-api --agent codex
```

### Agent Handoff

```
/worktree handoff feature-auth --to cursor
```

Generates a structured handoff block with context summary, pending tasks, and key findings.

## Directory Convention

```
<project>/                         # Main worktree (main branch)
+-- .git/                          # Single git database
+-- CLAUDE.md                      # Project principles (shared)
+-- plans/                         # Plan files

<project>-worktrees/               # All worktrees (sibling of project root)
+-- feature-auth/                  # worktree: feature/auth branch
|   +-- .worktree-spec.md          # Spec handoff document
|   +-- traces/                    # EARS trace (if synapse-ears installed)
+-- bugfix-memory-leak/
    +-- ...
```

## Companion Plugins

synapse-worktree works standalone but integrates with the Synapse family:

| Plugin | Integration |
|--------|------------|
| [synapse-ears](../synapse-ears/) | Auto-create trace.md in new worktrees |
| [synapse-git](../synapse-git/) | Auto-save before switching worktrees |
| [synapse-review](../synapse-review/) | Review updates `.worktree-spec.md` |
| [synapse-execute](../synapse-execute/) | Execution tracks progress in spec |

## Requirements

- **Claude Code** with plugin support
- **git** 2.20+ (for worktree support)

## License

MIT License. See [LICENSE](../LICENSE).
