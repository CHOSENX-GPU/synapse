---
name: git-workflow
description: |
  Automated git operations: stage, commit with Conventional Commits, push, create PRs.
  Use when the user says /commit, /save, /push, /pr, /squash-merge,
  "commit code", "save progress", "create pull request", or "merge PR".
---

# Git Workflow

Automate git operations with Conventional Commits, auto-push, and PR creation.

## Core Principles

- **One commit per logical unit**: don't mix unrelated changes in one commit
- **Conventional Commits format**: `type(scope): description`
- **Auto-push after commit**: push to remote by default (configurable)
- **Safety first**: check for unresolved conflicts before push

## Commands

### /save

Lightweight WIP commit for in-progress work. Does not push.

1. `git add -A`
2. Analyze the diff to generate a short description
3. `git commit -m "wip: {auto-generated description}"`
4. Do NOT push (WIP commits stay local)

### /commit [message]

Formal commit after completing a logical unit of work.

1. `git add -A`
2. Analyze `git diff --staged`:
   - Run the generate-commit-msg.sh script from the plugin's scripts/ directory to get structured diff info
   - Or directly analyze `git diff --staged --stat` and `git diff --staged`
3. Determine Conventional Commit components:
   - **type**: feat | fix | refactor | docs | test | chore | perf | ci | build
   - **scope**: infer from changed file paths (e.g., `auth`, `api`, `ui`)
   - **description**: concise summary of the change
4. If user provided a message, use it as the commit body
5. Format: `git commit -m "{type}({scope}): {description}" -m "{body}"`
   - Body includes a change summary
6. Auto-push: `git push origin {current-branch}`
7. If push fails (remote has new commits): `git pull --rebase` then retry push

### /push

Manual push trigger (when auto-push is disabled).

1. Check for uncommitted changes → prompt user to `/commit` first
2. `git push origin {current-branch}`
3. If new branch, auto-add `--set-upstream`
4. If remote conflicts, inform user and suggest resolution

### /pr [title]

Create a Pull Request.

1. Ensure all local commits are pushed (run `/push` if needed)
2. Collect all commit messages on this branch relative to base
3. Generate PR description:
   - Change summary (from commits)
   - Reference to plan file (if in `./plans/`)
   - EARS key findings (if in `traces/`)
4. Run: `gh pr create --title "{title}" --body "{description}"`
   - If no title provided, generate from branch name
5. If vibe-kanban task exists, add reference in PR description

### /squash-merge

Merge an approved PR and clean up.

1. `gh pr merge --squash`
2. Run `/worktree cleanup` for the corresponding worktree (if applicable)
3. Check if any EARS entries from this branch should be promoted to KNOWN_ISSUES.md

## Conventional Commits Reference

| Type     | Use When                                      |
|----------|-----------------------------------------------|
| feat     | New feature or capability                     |
| fix      | Bug fix                                       |
| refactor | Code restructuring without behavior change    |
| docs     | Documentation only                            |
| test     | Adding or updating tests                      |
| chore    | Maintenance (deps, config, CI)                |
| perf     | Performance improvement                       |
| ci       | CI/CD changes                                 |
| build    | Build system changes                          |

## Auto-Commit Triggers (from orchestration layer)

The following scenarios trigger automatic `/commit`:
- plan-execute completes a batch and passes code-review
- plan-review completes a revision round
- worktree handoff (before handoff)

## EARS Integration

- After important commits, write an EARS Checkpoint if warranted
- The EARS PostToolUse hook (ears-trace.py) continues to work independently
- On `/squash-merge`, check traces/ for patterns worth promoting to KNOWN_ISSUES.md

## PostToolUse Hook Coordination

git-workflow works alongside the EARS ears-trace.py hook:
- ears-trace.py detects errors in Bash output → triggers EARS Error prompt
- At important EARS Checkpoints, consider auto-running `/save`
