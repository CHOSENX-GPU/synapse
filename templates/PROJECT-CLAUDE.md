# Project: <project-name>

## Overview
<!-- Brief description of the project's goal and core functionality -->

## Design Principles
<!-- Project-specific design principles, supplementing global principles.md -->

## Architecture
<!-- Core modules, data flow, key dependencies -->

## Build & Test
<!-- Build commands, test commands, environment setup -->

## EARS System
- trace.md location: `traces/<task-name>/trace.md`
- Knowledge promotion: trace → KNOWN_ISSUES → this file → ~/.claude/memory/pitfalls.md

## Multi-AI Collaboration

### Agent Roles
- **Claude Code**: orchestrator — planning, review adjudication, git operations, EARS management
- **Codex** (via MCP): executor/reviewer — code generation, adversarial review
- **Cursor** (via CLI or standalone): alternative executor — works in worktrees independently

### Collaboration Rules
1. Non-trivial tasks: `/plan-review` first, then `/plan-execute`
2. Codex review stage: read-only sandbox
3. All plans, reviews, execution records persist to `./plans/`
4. Key milestones auto-write EARS entries
5. One logical unit per commit, Conventional Commits format
6. Worktree switches require `.worktree-spec.md` update

## Key Decisions
<!-- Important technical decisions and rationale, promoted from KNOWN_ISSUES -->
