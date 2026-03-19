# synapse-ears

**EARS (Evolving Autonomous Research System) -- project-aware knowledge capture for Claude Code.**

Automatically captures errors, decisions, and discoveries during development sessions. Includes a PostToolUse hook with trace.md auto-discovery and a `/ears-init` skill that generates tech-stack-specific EARS configuration.

## Installation

```bash
# Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# Install the EARS plugin
claude plugin install synapse@synapse-ears
```

After installation, run `/setup` to install the improved EARS hook.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **ears-init** | `/ears-init` | Scan project, detect tech stack, generate customized EARS config |
| **setup** | `/setup` | Install EARS hook and verify compatibility |

## Quick Start

```
# 1. Install the hook (once)
/setup

# 2. Initialize EARS for your project
/ears-init
```

`/ears-init` scans your project and generates:
- Customized `CLAUDE.md` with EARS section
- `traces/` directory and initial `trace.md`
- `KNOWN_ISSUES.md` and `LEARNING.md`
- `ears-config.json` with tech-stack-specific error patterns
- Optional: Cursor rules (`.cursor/rules/ears-project.mdc`) and Codex `AGENTS.md`

## `ears-config.json`

Each project gets its own `ears-config.json` at the project root. The EARS hook reads this file to customize its behavior:

```json
{
  "error_patterns": ["Traceback", "SyntaxError:", "TypeError:"],
  "checkpoint_interval": 10,
  "error_cooldown_seconds": 120,
  "checkpoint_cooldown_seconds": 600,
  "ignore_paths": [".git/", "__pycache__/", ".venv/"]
}
```

`/ears-init` generates patterns for: Python, Node.js/TypeScript, Rust, Go, Java, C#, and polyglot projects.

## Four-Tier Knowledge Architecture

```
Tier 1: traces/<task>/trace.md     (per-task raw records)
Tier 2: KNOWN_ISSUES.md            (cross-task patterns)
Tier 3: CLAUDE.md / AGENTS.md      (project-level principles)
Tier 4: ~/.claude/memory/          (cross-project lessons)
```

Knowledge flows upward. Promote when patterns emerge (2+ occurrences).

## Improved EARS Hook

The included `hooks/ears-trace.py` improves on the default hook:

| Feature | Default Hook | Improved Hook |
|---------|-------------|---------------|
| trace.md auto-discovery | No (generic path) | Walks up directory tree to find nearest trace.md |
| Context naming | Global state | Per-context (directory-based) naming and rate limiting |
| Missing trace.md reminder | No | Prompts to create one (5min cooldown) |
| Project-specific patterns | Hardcoded | Loads from `ears-config.json` |
| File skipping | Partial | Full (.git, __pycache__, node_modules, trace.md itself) |

## Companion Plugins

synapse-ears works standalone but integrates with the Synapse family:

| Plugin | What it adds |
|--------|-------------|
| [synapse-review](../synapse-review/) | Adversarial plan review and cross-agent code review |
| [synapse-execute](../synapse-execute/) | Orchestrated plan execution via Codex/Cursor |
| [synapse-worktree](../synapse-worktree/) | Git worktree lifecycle management |
| [synapse-git](../synapse-git/) | Automated git with Conventional Commits |

## Requirements

- **Claude Code** with plugin support
- **Python 3.8+** (for the EARS hook)
- **git** (for project root detection)

## License

MIT License. See [LICENSE](../LICENSE).
