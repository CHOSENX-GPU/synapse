---
name: plan-review
description: |
  Adversarial plan review: Claude Code creates a plan, Codex/Cursor reviews it critically,
  iterate until approved. Use when the user says /plan-review, "review plan",
  "审查计划", or needs a technical plan vetted by a second AI agent.
---

# Plan-Review: Adversarial Plan Review

Claude Code creates a technical plan, then delegates adversarial review to Codex (or Cursor). The reviewer's role is to find flaws. Iterate until the plan is solid.

## Prerequisites

- If working in a worktree, confirm `.worktree-spec.md` exists
- Check `KNOWN_ISSUES.md` for issues relevant to the current task

## Working Directory

- Plan files: `./plans/` (create if it doesn't exist)
- EARS records: `./traces/<task-name>/trace.md`

## Workflow

### STEP 1: Requirements Analysis and Initial Plan

1. Understand the user's requirements
2. **Check KNOWN_ISSUES.md** for related known issues to avoid repeating past mistakes
3. Create initial plan at `./plans/plan-{timestamp}.md` containing:
   - **Objective**: what the plan achieves
   - **Technical Approach**: how it will be implemented
   - **Files to Change**: exact file paths and what changes
   - **Risks**: cross-reference with KNOWN_ISSUES.md
   - **Acceptance Criteria**: how to verify success

### STEP 2: Delegate Adversarial Review to Codex

**Via MCP (preferred):**

Call the `codex` MCP tool with:
- `PROMPT`: Full plan text + review instructions:
  > "Review this technical plan critically. Evaluate from 5 dimensions:
  > 1. Technical Feasibility — can this actually work?
  > 2. Completeness — are there missing steps or edge cases?
  > 3. Risk Assessment — what could go wrong?
  > 4. Maintainability — will this be easy to maintain?
  > 5. Performance — are there performance concerns?
  >
  > For each issue found, tag severity: CRITICAL / HIGH / MEDIUM / LOW.
  > Be adversarial — your job is to find problems."
- `cd`: current working directory
- `sandbox`: `"read-only"`
- `return_all_messages`: `true`
- Save the `SESSION_ID` for follow-up rounds

**Via Shell fallback (if MCP unavailable):**

```bash
bash <plugin-scripts-dir>/ask_codex.sh "<review-prompt>" read-only "<working-dir>"
```

### STEP 3: Evaluate Review and Revise

1. Read the review response
2. **Independently evaluate each issue** — do not blindly accept all feedback
   - If you disagree, document the disagreement with rationale
3. CRITICAL and HIGH issues: must be addressed in revision
4. MEDIUM and LOW issues: evaluate case-by-case
5. Write revised plan: `./plans/plan-{timestamp}-v{N}.md`
6. Archive review: `./plans/review-{timestamp}-round{N}.md`
7. **Write EARS Checkpoint**:
   ```
   ### EARS — Checkpoint ({timestamp})
   - Discovery: Codex review found {N} issues, {M} CRITICAL
   - Decision: Revised {list}, kept {list} (rationale: ...)
   - Status: Round {N} complete, {pending} issues remaining
   ```

### STEP 4: Iteration Decision

- **Unresolved CRITICAL issues remain** → return to STEP 2 (same SESSION_ID)
- **Only MEDIUM/LOW remain** → ask user whether to address or accept
- **User satisfied** → update `.worktree-spec.md` context section → output final plan path
- **Maximum 5 rounds** — if still unresolved after 5, escalate to user

### Output

- Final plan file path
- If in a worktree, auto-update `.worktree-spec.md` Context section
- If review revealed recurring problem patterns, consider promoting to KNOWN_ISSUES.md

## EARS Integration

- Each review round writes a Checkpoint to `traces/<task>/trace.md`
- Recurring issues across multiple reviews → promote to KNOWN_ISSUES.md
- If the plan is abandoned → write EARS Dead End entry
