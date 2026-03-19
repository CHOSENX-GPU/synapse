# Global Instructions — <project-name>

## Project Overview
<!-- Brief description of the project -->

## Design Principles

1. **Design for what you don't know** — principles handle the unexpected
2. **Principles over procedures** — prefer principles over rigid step-by-step procedures
3. **Defer abstraction until 3+ uses** — avoid premature abstraction
4. **Fail Fast** — crash with full stack traces for immediate debugging
5. **Code should be self-explanatory** — comments explain "Why", not "What"
6. **Never copy params blindly** — understand every parameter
7. **Consider resource costs** — estimate before executing
8. **Review before implementing** — plan first for complex tasks
9. **Update refs in same commit** — keep code and documentation in sync

## Build & Test
<!-- Build commands, test commands, environment setup -->

## Architecture
<!-- Core modules, data flow, key dependencies -->

## EARS — Evolving Autonomous Research System

Structured knowledge capture that survives across sessions.

### When to Write EARS Entries

Follow these rules during every task:

- **Error**: When you encounter an error, exception, or unexpected failure — after fixing it, append an EARS Error entry to the project's `traces/<task>/trace.md`
- **Checkpoint**: After completing a significant milestone or making an important decision — append an EARS Checkpoint entry
- **Dead End**: When an approach fails and you switch strategies — append an EARS Dead End entry

Create `traces/<task>/trace.md` if it doesn't exist.

### Entry Formats

```
### EARS — Error (YYYY-MM-DD HH:MM)
- Problem: what failed and the error message
- Diagnosis: how you identified the root cause
- Fix: what you changed and why it works
- Lesson: what would prevent this in the future

### EARS — Checkpoint (YYYY-MM-DD HH:MM)
- Discovery: key findings or decisions since last checkpoint
- Decision: choices made and their rationale
- Status: current progress and next steps

### EARS — Dead End (YYYY-MM-DD HH:MM)
- Approach: what was attempted
- Why it failed: reason
- Alternative: what to try instead
```

### Four-Tier Knowledge Architecture

Knowledge flows strictly upward; each tier reduces detail and increases persistence.

- **Tier 1** `traces/<task>/trace.md` — per-task raw records
- **Tier 2** `KNOWN_ISSUES.md` — cross-task patterns. Promote when same issue appears 2+ times
- **Tier 3** `AGENTS.md` (this file) — project-level principles. Promote when pattern has project-wide impact
- **Tier 4** `~/.codex/AGENTS.md` — cross-project lessons. Promote when lesson applies across projects

Do not promote prematurely — wait for patterns to emerge naturally.

## Learning & Experiments

- Maintain `LEARNING.md` per project: tech decisions, new concepts, mistakes, lessons
- EARS trace.md = "what happened" (raw data). LEARNING.md = "what was learned" (synthesis)
- Failed experiments are valuable — record why they failed
