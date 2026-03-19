---
name: plan-execute
description: |
  Execute a reviewed plan by delegating to Codex/Cursor/Claude, with batch execution,
  code review, and auto-commit. Use when the user says /plan-execute, "execute plan",
  "执行计划", or wants to implement an approved technical plan.
---

# Plan-Execute: Orchestrated Plan Execution

Execute a reviewed and approved plan by delegating implementation to an executor agent (Codex, Cursor, or Claude Sonnet), with Claude Code orchestrating quality control.

## Executor Selection

Ask the user before starting:
- **codex-mcp** (default): MCP call to Codex, supports multi-round fix conversations
- **codex-cli**: Shell script direct Codex invocation
- **cursor-cli**: Via Cursor CLI
- **claude-sonnet**: Claude Code's own Sonnet sub-agent

## Workflow

### STEP 1: Load Plan

1. Read the specified plan file
2. If in a worktree, also read `.worktree-spec.md` for context
3. Check `KNOWN_ISSUES.md` for related entries

### STEP 2: Decompose into Execution Batches

Principles:
- Interdependent changes go in the same batch
- Each batch: 3-5 files maximum
- Infrastructure/foundation first, features later
- Create tracking file: `./plans/execution-{timestamp}.md`

### STEP 3: Execute Batches

For each batch:

**3a. Construct Execution Instructions**

Be explicit about:
- Exact file paths to create/modify
- Code changes expected
- Coding standards to follow
- Interface contracts to maintain

**3b. Delegate to Executor**

Via MCP:
- `PROMPT`: execution instructions
- `cd`: current working directory
- `sandbox`: `"workspace-write"`
- `return_all_messages`: `true`
- Save `SESSION_ID`

Via Shell fallback:
```bash
bash <plugin-scripts-dir>/ask_codex.sh "<instructions>" workspace-write "<working-dir>"
```

**3c. Immediate Code Review (Claude Code)**

After executor completes, read the modified files and check:
- Conformance to the plan
- New bugs or regressions
- Code style and conventions
- Edge cases and error handling

Write review to `./plans/batch-review-{N}.md`

**3d. Fix Loop (if review fails)**

Send fix instructions via the same SESSION_ID (MCP) or new shell call. Maximum 3 rounds.

**3e. Batch Passes**

Auto-commit:
```
{type}({scope}): implement {batch-description}

Batch {N}/{total} of plan {plan-name}
Reviewed by: Claude Code (auto-review passed)
```

Write EARS Checkpoint. Update `.worktree-spec.md` completed/pending lists.

### STEP 4: All Batches Complete

1. Run tests if a test command is known (check CLAUDE.md or package.json)
2. Output execution summary
3. `git push`
4. If vibe-kanban is running, update task status to Review

## Limits

- Each batch: max 3 fix rounds
- After 3 failed rounds: mark as NEEDS_MANUAL_FIX, write EARS Dead End, continue to next batch
- Report all NEEDS_MANUAL_FIX items in the final summary

## EARS Integration

- Each batch completion writes a Checkpoint
- Failed batches write a Dead End
- Recurring failures → promote pattern to KNOWN_ISSUES.md
