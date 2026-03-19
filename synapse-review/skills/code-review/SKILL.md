---
name: code-review
description: |
  Deep code review with cross-agent support. Supports claude-only, codex-review,
  and dual-review modes. Use when the user says /code-review, "review code",
  "代码审查", or when code needs quality verification after implementation.
---

# Code-Review: Deep Code Review

Multi-mode code review supporting single-agent and cross-agent review patterns. Integrates with EARS for knowledge capture.

## Review Scope Detection

1. User specifies files → review those files
2. Called from plan-execute → review that batch's changes
3. Neither specified → use `git diff` to find recent changes

## Review Modes

### claude-only
Fast single-perspective review by Claude Code. Best for small, low-risk changes.

### codex-review (default)
Codex performs the review, Claude adjudicates findings.

Via MCP:
- `PROMPT`: files to review + review instructions (see dimensions below)
- `cd`: current working directory
- `sandbox`: `"read-only"`
- `return_all_messages`: `true`

Via Shell fallback:
```bash
bash <plugin-scripts-dir>/ask_codex.sh "<review-prompt>" read-only "<working-dir>"
```

### dual-review
Both Claude and Codex review independently, then cross-compare findings. Most thorough, best for critical changes.

1. Claude reviews first, documents findings
2. Codex reviews independently (don't share Claude's findings)
3. Compare and synthesize — agreements strengthen confidence, disagreements need resolution

## Review Dimensions

Every review evaluates these 5 dimensions. Each issue gets a severity tag.

| Dimension      | What to Check                                              |
|----------------|-----------------------------------------------------------|
| Correctness    | Logic errors, off-by-one, null handling, race conditions   |
| Security       | Injection, auth bypass, secrets exposure, input validation |
| Performance    | O(n²) loops, memory leaks, unnecessary allocations        |
| Readability    | Naming, structure, complexity, documentation               |
| Test Coverage  | Missing tests, edge cases, assertion quality               |

Severity levels: **CRITICAL** / **HIGH** / **MEDIUM** / **LOW**

## Review Report

Write to `./plans/code-review-{timestamp}.md`:

```
## Code Review Report
**Reviewer**: Claude Code | Codex | Dual
**Verdict**: APPROVED | NEEDS_FIX | NEEDS_MAJOR_REWORK
**Files Reviewed**: N files
**Issues Found**: X critical, Y high, Z medium, W low

### Issues

#### [CRITICAL] Issue title
- **File**: path/to/file.py:42
- **Dimension**: Correctness
- **Description**: ...
- **Suggested Fix**: ...

#### [HIGH] Issue title
...
```

## Handling Results

### APPROVED
- If synapse-git is installed, auto-run `/commit` + `/push`; otherwise `git add -A && git commit && git push` manually
- Notify user of approval

### NEEDS_FIX
- Send fix instructions to the executor (same SESSION_ID if available)
- Maximum 3 fix rounds
- After fixes, re-review the changed files only

### NEEDS_MAJOR_REWORK
- Recommend going back to `/plan-review`
- Write EARS Dead End entry with findings
- Do NOT auto-commit

## EARS Integration (requires synapse-ears)

If synapse-ears is installed:
- Review findings that reveal error patterns → write EARS Error entry
- If the same type of issue appears across 2+ reviews → promote to KNOWN_ISSUES.md
- Review completion → write EARS Checkpoint
- Major rework decision → write EARS Dead End

If synapse-ears is NOT installed, skip EARS entries.
