# Synapse

**Modular multi-AI collaboration plugins for Claude Code.**

Synapse is a family of 5 independent plugins that connect Claude Code, Codex, and Cursor into a unified development workflow. Install all of them for the full experience, or pick only what you need.

## Architecture

```
+-----------------------------------------------------------------------+
|                    User Layer (Human-in-the-Loop)                      |
|  Plan tasks -> Assign agents -> Review code -> Approve merges          |
+----+------------------------------------------------------------------+
     |
+----v------------------------------------------------------------------+
|                   Plugin Layer (5 Independent Plugins)                  |
|                                                                        |
|  synapse-review       synapse-execute       synapse-ears               |
|  /plan-review         /plan-execute         /ears-init                 |
|  /code-review         (delegation)          (knowledge capture)        |
|  (adversarial)                                                         |
|                                                                        |
|  synapse-worktree                  synapse-git                         |
|  /worktree create/switch/          /commit /save /push                 |
|  handoff/cleanup                   /pr /squash-merge                   |
+----+------------------+------------------+----------------------------+
     |                  |                  |
+----v------+  +--------v-----+  +--------v-------+
| Claude    |  | Codex (MCP)  |  | Cursor (CLI)   |
| Code      |  | exec/review  |  | exec/review    |
+-----------+  +--------------+  +----------------+
```

## Plugins

| Plugin | Skills | Triggers | Install |
|--------|--------|----------|---------|
| **synapse-ears** | ears-init, setup | `/ears-init`, `/setup` | `claude plugin install synapse@synapse-ears` |
| **synapse-review** | plan-review, code-review, codex-bridge | `/plan-review`, `/code-review` | `claude plugin install synapse@synapse-review` |
| **synapse-execute** | plan-execute, codex-bridge | `/plan-execute` | `claude plugin install synapse@synapse-execute` |
| **synapse-worktree** | worktree-manager | `/worktree` | `claude plugin install synapse@synapse-worktree` |
| **synapse-git** | git-workflow | `/commit`, `/save`, `/push`, `/pr`, `/squash-merge` | `claude plugin install synapse@synapse-git` |

## Install All

```bash
# 1. Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# 2. Install all plugins
claude plugin install synapse@synapse-ears
claude plugin install synapse@synapse-review
claude plugin install synapse@synapse-execute
claude plugin install synapse@synapse-worktree
claude plugin install synapse@synapse-git
```

## Install Individually

Each plugin works standalone. Install only what you need:

```bash
# Just EARS knowledge capture
claude plugin install synapse@synapse-ears

# Just automated git
claude plugin install synapse@synapse-git

# Review + Execute (for full plan workflow)
claude plugin install synapse@synapse-review
claude plugin install synapse@synapse-execute
```

## Companion Matrix

Plugins enhance each other when installed together:

| Plugin | Enhanced by |
|--------|-----------|
| synapse-review | + synapse-ears (EARS checkpoints per review round) |
|                | + synapse-worktree (update .worktree-spec.md) |
|                | + synapse-git (auto-commit after approval) |
| synapse-execute | + synapse-ears (EARS checkpoints per batch) |
|                 | + synapse-worktree (track progress in spec) |
|                 | + synapse-git (auto-commit with Conventional Commits) |
| synapse-worktree | + synapse-ears (auto-create trace.md in worktrees) |
|                  | + synapse-git (auto-save before switching) |
| synapse-git | + synapse-ears (EARS findings in PR descriptions) |
|             | + synapse-worktree (auto-cleanup on squash-merge) |
| synapse-ears | standalone (no dependencies) |

## Quick Start

### Full Workflow

```
/ears-init                                    # Set up EARS for your project
/worktree create feature-auth                 # Create a feature branch
/plan-review Implement JWT auth               # Plan + adversarial review
/plan-execute ./plans/plan-xxx-v2.md          # Execute the plan
/code-review                                  # Deep code review
/pr "feat: JWT authentication"                # Create PR
/squash-merge                                 # Merge and clean up
```

### Minimal Workflow (just git + EARS)

```
/ears-init        # Set up knowledge capture
/commit           # Auto-commit with Conventional Commits
/push             # Push to remote
```

## Requirements

- **Claude Code** with plugin support
- **Python 3.8+** (for EARS hook)
- **git** 2.20+ (for worktree support)
- **gh CLI** (for PR operations)
- **Codex MCP** or **Codex CLI** (for cross-agent review/execution)
- **Cursor CLI** (optional)

## Documentation

Each plugin has its own detailed README:

- [synapse-ears](synapse-ears/README.md) -- EARS knowledge capture
- [synapse-review](synapse-review/README.md) -- Plan and code review
- [synapse-execute](synapse-execute/README.md) -- Plan execution
- [synapse-worktree](synapse-worktree/README.md) -- Worktree management
- [synapse-git](synapse-git/README.md) -- Git automation

## Acknowledgments

The EARS (Evolving Autonomous Research System) integrated in synapse-ears is based on the work of **Tianhan Zhang** ([EARS-deploy](https://github.com/TianhanZhang68/EARS-deploy)). His structured knowledge capture methodology -- four-tier architecture, trace.md auto-discovery, and PostToolUse hook design -- forms the foundation of the EARS plugin.

## License

MIT License. See [LICENSE](LICENSE).
