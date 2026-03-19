# synapse-execute

**Orchestrated plan execution via Codex, Cursor, or Claude sub-agents.**

Execute reviewed and approved plans by delegating implementation to an executor agent, with Claude Code orchestrating quality control through batch execution, intermediate code review, and fix loops. Includes the Codex Bridge for MCP and shell-based agent communication.

## Installation

```bash
# Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# Install the execute plugin
claude plugin install synapse@synapse-execute
```

## Prerequisites

- **Codex MCP** (preferred) or **Codex CLI** for execution delegation
- **Cursor CLI** (optional, for Cursor-based execution)

Install Codex MCP (one-time):
```bash
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **plan-execute** | `/plan-execute` | Execute a reviewed plan via Codex/Cursor/Claude with batch review |
| **codex-bridge** | (internal) | MCP and shell bridge for calling Codex/Cursor |

## Quick Start

```
/plan-execute ./plans/plan-xxx-v2.md
```

## Executor Selection

Before starting, choose an executor:
- **codex-mcp** (default) -- MCP call to Codex, supports multi-round fix conversations
- **codex-cli** -- Shell script direct Codex invocation
- **cursor-cli** -- Via Cursor CLI
- **claude-sonnet** -- Claude Code's own sub-agent

## Execution Flow

```
Load Plan -> Decompose into Batches -> For each batch:
  -> Delegate to Executor
  -> Immediate Code Review (Claude Code)
  -> Fix Loop (if needed, max 3 rounds)
  -> Commit on pass
-> Run tests -> Push
```

- Each batch: 3-5 files maximum
- Infrastructure/foundation first, features later
- Maximum 3 fix rounds per batch before marking NEEDS_MANUAL_FIX

## Companion Plugins

synapse-execute works standalone but integrates with the Synapse family:

| Plugin | Integration |
|--------|------------|
| [synapse-review](../synapse-review/) | Review plans before execution |
| [synapse-ears](../synapse-ears/) | Auto-write EARS checkpoints per batch |
| [synapse-worktree](../synapse-worktree/) | Track progress in `.worktree-spec.md` |
| [synapse-git](../synapse-git/) | Auto-commit with Conventional Commits |

## Requirements

- **Claude Code** with plugin support
- **Codex MCP** or **Codex CLI** (for execution delegation)
- **Cursor CLI** (optional)

## License

MIT License. See [LICENSE](../LICENSE).
