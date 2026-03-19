# synapse-git

**Automated git operations with Conventional Commits for Claude Code.**

Stage, commit, push, create PRs, and squash-merge with auto-generated Conventional Commit messages and smart diff analysis.

## Installation

```bash
# Add the Synapse marketplace
claude plugin marketplace add CHOSENX-GPU/synapse

# Install the git plugin
claude plugin install synapse@synapse-git
```

## Prerequisites

- **git**
- **gh CLI** (for PR operations)

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **git-workflow** | `/commit` `/save` `/push` `/pr` `/squash-merge` | Automated git operations with Conventional Commits |

## Commands

| Command | Description |
|---------|-------------|
| `/save` | Lightweight WIP commit (does not push) |
| `/commit [message]` | Formal commit with auto-generated Conventional Commit message + push |
| `/push` | Manual push trigger |
| `/pr [title]` | Create a Pull Request with auto-generated description |
| `/squash-merge` | Merge an approved PR and clean up |

## Quick Start

```
# Save work in progress
/save

# Formal commit (auto-generates message, auto-pushes)
/commit

# Create a PR
/pr "Add JWT authentication"

# Merge after approval
/squash-merge
```

## Conventional Commits

All commits follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

| Type | Use When |
|------|----------|
| feat | New feature or capability |
| fix | Bug fix |
| refactor | Code restructuring without behavior change |
| docs | Documentation only |
| test | Adding or updating tests |
| chore | Maintenance (deps, config, CI) |
| perf | Performance improvement |
| ci | CI/CD changes |
| build | Build system changes |

## Companion Plugins

synapse-git works standalone but integrates with the Synapse family:

| Plugin | Integration |
|--------|------------|
| [synapse-ears](../synapse-ears/) | Include EARS findings in PR descriptions |
| [synapse-review](../synapse-review/) | Auto-commit after approved code review |
| [synapse-execute](../synapse-execute/) | Auto-commit after batch execution |
| [synapse-worktree](../synapse-worktree/) | Auto-cleanup worktree on squash-merge |

## Requirements

- **Claude Code** with plugin support
- **git**
- **gh CLI** (for `/pr` and `/squash-merge`)

## License

MIT License. See [LICENSE](../LICENSE).
