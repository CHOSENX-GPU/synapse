# Synapse

**Multi-AI collaboration workflow plugin for Claude Code.**

Synapse connects Claude Code, Codex, and Cursor into a unified development workflow with adversarial plan review, orchestrated execution, cross-agent code review, git worktree management, and automated git operations — all integrated with the EARS knowledge system.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    User Layer (Human-in-the-Loop)                │
│  Plan tasks → Assign agents → Review code → Approve merges      │
└────────────┬─────────────────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────────────────┐
│                   Orchestration Layer (Synapse Skills)            │
│                                                                   │
│  /plan-review    /plan-execute    /code-review                   │
│  (adversarial)   (delegation)     (deep review)                  │
│                                                                   │
│  /worktree-manager              /git-workflow                    │
│  (create/switch/handoff/clean)  (commit/push/pr/merge)           │
│                                                                   │
│  /codex-bridge                                                    │
│  (MCP + shell fallback)                                          │
└──────────┬──────────────────┬──────────────────┬─────────────────┘
           │                  │                  │
┌──────────▼──┐  ┌───────────▼──┐  ┌────────────▼──┐
│ Claude Code │  │ Codex (MCP)  │  │  Cursor CLI   │
│ (orchestr.) │  │ (exec/review)│  │ (exec/review) │
└─────────────┘  └──────────────┘  └───────────────┘
           │                  │                  │
┌──────────▼──────────────────▼──────────────────▼─────────────────┐
│                   Knowledge Layer (EARS)                          │
│  Tier 1: traces/<task>/trace.md    (per-worktree)                │
│  Tier 2: KNOWN_ISSUES.md          (project-wide)                 │
│  Tier 3: CLAUDE.md / AGENTS.md    (project principles)           │
│  Tier 4: ~/.claude/memory/        (cross-project)                │
└──────────────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# Install the plugin
claude plugin install synapse@synapse
```

After installation, run `/setup` in Claude Code to configure global settings.

## Available Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **plan-review** | `/plan-review` | Create a technical plan, delegate adversarial review to Codex, iterate until solid |
| **plan-execute** | `/plan-execute` | Execute a reviewed plan via Codex/Cursor/Claude with batch execution and auto-review |
| **code-review** | `/code-review` | Deep code review in 3 modes: claude-only, codex-review, dual-review |
| **worktree-manager** | `/worktree` | Create, list, switch, handoff, and cleanup git worktrees |
| **git-workflow** | `/commit` `/save` `/push` `/pr` | Automated git operations with Conventional Commits |
| **codex-bridge** | (internal) | MCP and shell bridge for calling Codex/Cursor from Claude Code |
| **setup** | `/setup` | One-time environment configuration |

## Quick Start

### 1. Setup

```
/setup
```

This configures Codex MCP, updates your global CLAUDE.md, and verifies EARS compatibility.

### 2. Start a Feature Branch

```
/worktree create feature-auth --from main --agent claude-code
```

### 3. Plan and Review

```
/plan-review Implement JWT authentication module
```

Claude Code creates the plan, Codex reviews adversarially, you iterate until approved.

### 4. Execute the Plan

```
/plan-execute ./plans/plan-xxx-v2.md
```

Batched execution with automatic code review and commits.

### 5. Create a PR

```
/pr "Add JWT authentication"
```

## Usage Scenarios

### Parallel Feature Development

```
/worktree create feature-auth --agent claude-code
/worktree create feature-api --agent codex
# Work on auth in one worktree, API in another — simultaneously
```

### Agent Handoff

```
# Claude Code finished planning in feature-auth
/worktree handoff feature-auth --to cursor
# Open Cursor, point to the feature-auth worktree
# Cursor reads .worktree-spec.md and continues
```

### Full Workflow

```
/worktree create feature-auth
/plan-review Implement JWT auth with refresh tokens
/plan-execute ./plans/plan-xxx-v2.md
/code-review
/pr "feat: JWT authentication with refresh tokens"
/squash-merge
```

## Directory Conventions

### Project Structure

```
<project>/
├── CLAUDE.md              # Project principles (Tier 3)
├── KNOWN_ISSUES.md        # Cross-task patterns (Tier 2)
├── plans/                 # Plan, review, and execution files
└── traces/                # EARS Tier 1 records
    └── <task>/trace.md
```

### Worktree Structure

```
<project>-worktrees/
├── feature-auth/
│   ├── .worktree-spec.md  # Spec handoff document
│   └── traces/
│       └── feature-auth/
│           └── trace.md
└── feature-api/
    └── ...
```

## EARS Integration

Synapse is fully compatible with the EARS (Evolving Autonomous Research System) knowledge capture system. New EARS trigger points:

| Trigger | Entry Type | Location |
|---------|-----------|----------|
| Plan review round complete | Checkpoint | worktree trace.md |
| Execution batch passes | Checkpoint | worktree trace.md |
| Execution batch fails 3x | Dead End | worktree trace.md |
| Code review finds error pattern | Error | worktree trace.md |
| Worktree handoff | Checkpoint | worktree trace.md |
| Same issue appears 2+ times | Promotion | KNOWN_ISSUES.md |

## Requirements

- **Claude Code** with plugin support
- **gh CLI** (for PR operations)
- **git** 2.20+ (for worktree support)
- **Codex MCP** or **Codex CLI** (for cross-agent review/execution)
- **Cursor CLI** (optional, for Cursor integration)

## License

MIT License. See [LICENSE](LICENSE).
