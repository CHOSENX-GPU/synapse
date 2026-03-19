# Project: <project-name>

## Overview
<!-- Brief description of the project's goal and core functionality -->

## Design Principles
<!-- Project-specific design principles. Some universal ones to consider:
- Design for what you don't know — plans should handle unforeseen scenarios
- Principles over procedures — write instructions as principles, not rigid steps
- Defer abstraction until 3+ uses — copy-and-modify beats premature generalization
- Fail fast — crash with full stack traces for immediate debugging
- Code should be self-explanatory — comments explain "Why", not "What"
- Never copy params blindly — understand every parameter's purpose
- Consider resource costs — estimate before executing
- Review before implementing — plan first for complex tasks
- Update refs in same commit — keep code and documentation in sync
-->

## Architecture
<!-- Core modules, data flow, key dependencies, directory structure -->

## Build & Test
<!-- Build commands, test commands, environment setup -->

## EARS — Experience And Reasoning System

A PostToolUse hook automatically monitors your work and sends `[EARS]` prompts.
**When you receive an `[EARS]` message, respond to it before continuing.**

### Why This Exists

Debugging insights, surprising discoveries, and design trade-offs are the most
valuable outputs of development work — but they evaporate unless captured in the
moment. EARS ensures this knowledge accumulates in `trace.md` files, where future
sessions (yours or other agents') can learn from it.

### How to Respond

**On error prompt** — You just hit an error and fixed it. Append:

```
### EARS — Error (YYYY-MM-DD HH:MM)
- Problem: what failed — include the error message
- Diagnosis: how you identified the root cause
- Fix: what you changed and why it works
- Lesson: what would prevent this in the future
```

**On checkpoint prompt** — Reflect on recent work. Append whichever apply:

```
### EARS — Checkpoint (YYYY-MM-DD HH:MM)
- Problem solved: what broke, how you debugged it, what fixed it
- Discovery: something non-obvious you learned
- Decision: a design choice and its trade-off
- Dead end: an approach you tried and why it didn't work
```

If nothing notable happened, write: `No notable events.`

**On dead end** — When you abandon an approach:

```
### EARS — Dead End (YYYY-MM-DD HH:MM)
- Approach: what was attempted
- Why it failed: the specific reason
- Alternative: what to try instead
```

### Where to Write

Append to the nearest `trace.md` found by walking up from the file you're
editing. If none exists, create one: `# Trace: <directory-name>`

### Four-Tier Knowledge Architecture

Knowledge flows strictly upward; each tier reduces detail and increases persistence.

- **Tier 1** `traces/<task>/trace.md` — per-task raw records (errors, params, context)
- **Tier 2** `KNOWN_ISSUES.md` — cross-task patterns (Symptom/Context/Cause/Resolution/Scope). Promote when the same issue appears 2+ times in trace.md
- **Tier 3** This file (`CLAUDE.md`) — project-level principles. Promote when a KNOWN_ISSUES pattern has project-wide impact
- **Tier 4** `~/.claude/memory/pitfalls.md` — cross-project universal lessons. Promote when a lesson applies across projects

Do not promote prematurely — wait for patterns to emerge naturally. Check the upper tier for duplicates before adding.

### Lessons-Learned Pattern

When an insight is general (understood, applies broadly, has a natural home in
a shared artifact), transfer it there — KNOWN_ISSUES.md, this file, code, or
tests — wherever future work would look for it.

## Learning & Experiments

- Maintain `LEARNING.md` per project: tech decisions, new concepts, mistakes, lessons
- For research projects: use `experiments/` with `INDEX.md`, `active/`, `failed/` subdirectories
- EARS trace.md = "what happened" (raw data). LEARNING.md = "what was learned" (synthesis). They complement, not duplicate.
- Failed experiments are valuable — record why they failed and what was learned

## Key Decisions
<!-- Important technical decisions and rationale, promoted from KNOWN_ISSUES -->
