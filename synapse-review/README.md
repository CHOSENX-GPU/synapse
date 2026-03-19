# synapse-review

**Adversarial plan review and deep code review via Claude Code, Codex, and Cursor.**

Create technical plans and get them critically reviewed by a second AI agent. Run deep code reviews in three modes: Claude-only, Codex-review, or dual-review. Includes the Codex Bridge for MCP and shell-based agent communication.

## Installation

```bash
# Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# Install the review plugin
claude plugin install synapse@synapse-review
```

## Prerequisites

- **Codex MCP** (preferred) or **Codex CLI** for cross-agent review
- **Cursor CLI** (optional, for Cursor-based review)

Install Codex MCP (one-time):
```bash
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **plan-review** | `/plan-review` | Create a technical plan, delegate adversarial review to Codex |
| **code-review** | `/code-review` | Deep code review: claude-only, codex-review, or dual-review |
| **codex-bridge** | (internal) | MCP and shell bridge for calling Codex/Cursor |

## Quick Start

### Plan Review

```
/plan-review Implement JWT authentication with refresh tokens
```

Workflow:
1. Claude Code creates an initial plan
2. Codex reviews it adversarially across 5 dimensions
3. Claude evaluates feedback and revises
4. Iterate until approved (max 5 rounds)

### Code Review

```
/code-review
```

Three modes:
- **claude-only** -- fast single-perspective review
- **codex-review** (default) -- Codex reviews, Claude adjudicates
- **dual-review** -- both review independently, then cross-compare

## Review Dimensions

| Dimension | What to Check |
|-----------|--------------|
| Correctness | Logic errors, off-by-one, null handling, race conditions |
| Security | Injection, auth bypass, secrets exposure, input validation |
| Performance | O(n^2) loops, memory leaks, unnecessary allocations |
| Readability | Naming, structure, complexity, documentation |
| Test Coverage | Missing tests, edge cases, assertion quality |

Severity levels: **CRITICAL** / **HIGH** / **MEDIUM** / **LOW**

## Companion Plugins

synapse-review works standalone but integrates with the Synapse family:

| Plugin | Integration |
|--------|------------|
| [synapse-ears](../synapse-ears/) | Review rounds auto-write EARS checkpoints |
| [synapse-execute](../synapse-execute/) | Execute approved plans |
| [synapse-worktree](../synapse-worktree/) | Update `.worktree-spec.md` after review |
| [synapse-git](../synapse-git/) | Auto-commit after approved code review |

## Requirements

- **Claude Code** with plugin support
- **Codex MCP** or **Codex CLI** (for cross-agent review)
- **Cursor CLI** (optional)

## License

MIT License. See [LICENSE](../LICENSE).
