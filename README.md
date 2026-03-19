# Synapse

**Multi-AI collaboration workflow plugin for Claude Code.**

Synapse connects Claude Code, Codex, and Cursor into a unified development workflow with adversarial plan review, orchestrated execution, cross-agent code review, git worktree management, automated git operations, and **project-aware EARS knowledge capture** — all working together.

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
│  /ears-init        /codex-bridge                                 │
│  (project setup)   (MCP + shell fallback)                        │
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
| **ears-init** | `/ears-init` | Scan project, detect tech stack, generate customized EARS config |
| **plan-review** | `/plan-review` | Create a technical plan, delegate adversarial review to Codex |
| **plan-execute** | `/plan-execute` | Execute a reviewed plan via Codex/Cursor/Claude with batch review |
| **code-review** | `/code-review` | Deep code review in 3 modes: claude-only, codex-review, dual-review |
| **worktree-manager** | `/worktree` | Create, list, switch, handoff, and cleanup git worktrees |
| **git-workflow** | `/commit` `/save` `/push` `/pr` | Automated git operations with Conventional Commits |
| **codex-bridge** | (internal) | MCP and shell bridge for calling Codex/Cursor from Claude Code |
| **setup** | `/setup` | One-time environment configuration and hook installation |

## Quick Start

### 1. Setup (once)

```
/setup
```

Configures Codex MCP, updates global CLAUDE.md, and optionally installs the improved EARS hook.

### 2. Initialize EARS for Your Project

```
/ears-init
```

Scans your project, detects the tech stack, and generates:
- Customized `CLAUDE.md` with EARS section
- `traces/` directory and initial `trace.md`
- `KNOWN_ISSUES.md` and `LEARNING.md`
- `ears-config.json` with tech-stack-specific error patterns
- Optional: Cursor rules (`.cursor/rules/ears-project.mdc`) and Codex `AGENTS.md`

### 3. Start a Feature Branch

```
/worktree create feature-auth --from main --agent claude-code
```

### 4. Plan and Review

```
/plan-review Implement JWT authentication module
```

### 5. Execute the Plan

```
/plan-execute ./plans/plan-xxx-v2.md
```

### 6. Create a PR

```
/pr "Add JWT authentication"
```

## Project-Aware EARS

### How `/ears-init` Works

When you run `/ears-init`, Claude Code:

1. **Scans your project** — detects language (Python, Node.js, Rust, Go, etc.), framework, build/test commands, and directory structure
2. **Generates CLAUDE.md** — fills in project overview, architecture, commands, and a full EARS section with "how to respond" guidance
3. **Creates EARS skeleton** — `traces/`, `KNOWN_ISSUES.md`, `LEARNING.md`
4. **Generates `ears-config.json`** — project-specific error patterns so the hook catches the right errors for your tech stack
5. **Multi-tool setup** — optionally generates Cursor rules and Codex AGENTS.md

### `ears-config.json`

Each project gets its own `ears-config.json` at the project root. The improved EARS hook reads this file to customize its behavior:

```json
{
  "error_patterns": ["Traceback", "SyntaxError:", "TypeError:", ...],
  "checkpoint_interval": 10,
  "error_cooldown_seconds": 120,
  "checkpoint_cooldown_seconds": 600,
  "ignore_paths": [".git/", "__pycache__/", ".venv/"]
}
```

For a **Python** project, `ears-init` generates Python-specific patterns. For **Node.js**, it generates JavaScript/TypeScript patterns. For **Rust**, Go, Java, etc., it generates appropriate patterns. Mixed-language projects get combined patterns.

### Improved EARS Hook

The Synapse plugin includes an improved `ears-trace.py` hook (installed via `/setup`) that adds:

| Feature | Old Hook | Improved Hook |
|---------|----------|---------------|
| trace.md auto-discovery | No (generic path) | Walks up directory tree to find nearest trace.md |
| Context naming | Global state | Per-context (directory-based) naming and rate limiting |
| Missing trace.md reminder | No | Prompts to create one (5min cooldown) |
| Project-specific patterns | Hardcoded | Loads from `ears-config.json` |
| File skipping | Partial | Full (.git, __pycache__, node_modules, trace.md itself) |

### Example: Python Project

```
$ /ears-init

EARS initialized for my-python-app:
  - CLAUDE.md: created (Python/FastAPI detected)
  - traces/initial-setup/trace.md: created
  - KNOWN_ISSUES.md: created
  - LEARNING.md: created
  - ears-config.json: created (Python patterns)
  - Cursor rules: created (.cursor/rules/ears-project.mdc)
  - Hook: upgraded (auto-discovery enabled)
```

### Example: Node.js Project

```
$ /ears-init

EARS initialized for my-react-app:
  - CLAUDE.md: created (TypeScript/React detected)
  - traces/initial-setup/trace.md: created
  - KNOWN_ISSUES.md: created
  - LEARNING.md: created
  - ears-config.json: created (Node.js/TypeScript patterns)
  - Codex AGENTS.md: created
  - Hook: current (already up to date)
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
/ears-init
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
├── CLAUDE.md              # Project principles + EARS (Tier 3)
├── AGENTS.md              # Codex instructions (optional)
├── KNOWN_ISSUES.md        # Cross-task patterns (Tier 2)
├── LEARNING.md            # Synthesized lessons
├── ears-config.json       # Project-specific EARS hook config
├── plans/                 # Plan, review, and execution files
├── traces/                # EARS Tier 1 records
│   └── <task>/trace.md
└── .cursor/rules/
    └── ears-project.mdc   # Cursor EARS rules (optional)
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

Synapse is fully compatible with the EARS (Evolving Autonomous Research System) knowledge capture system. EARS trigger points:

| Trigger | Entry Type | Location |
|---------|-----------|----------|
| Plan review round complete | Checkpoint | worktree trace.md |
| Execution batch passes | Checkpoint | worktree trace.md |
| Execution batch fails 3x | Dead End | worktree trace.md |
| Code review finds error pattern | Error | worktree trace.md |
| Worktree handoff | Checkpoint | worktree trace.md |
| Same issue appears 2+ times | Promotion | KNOWN_ISSUES.md |
| Hook detects Bash error | Error prompt | nearest trace.md |
| Hook periodic checkpoint | Checkpoint prompt | nearest trace.md |
| Hook finds no trace.md | Reminder | create trace.md |

## Requirements

- **Claude Code** with plugin support
- **gh CLI** (for PR operations)
- **git** 2.20+ (for worktree support)
- **Python 3.8+** (for the EARS hook)
- **Codex MCP** or **Codex CLI** (for cross-agent review/execution)
- **Cursor CLI** (optional, for Cursor integration)

## License

MIT License. See [LICENSE](LICENSE).
