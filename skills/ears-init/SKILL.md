---
name: ears-init
description: |
  Project-aware EARS initialization. Scans the current project, detects tech stack,
  and generates customized CLAUDE.md, KNOWN_ISSUES.md, traces/, ears-config.json,
  and optionally Cursor rules and Codex AGENTS.md.
  Use when the user says /ears-init, "initialize EARS", "setup EARS for this project",
  "adapt EARS", or when starting work on a new project that lacks EARS configuration.
---

# EARS Init: Project-Aware EARS Initialization

Analyze the current project and generate customized EARS configuration files so that Claude Code (and optionally Cursor and Codex) can capture knowledge effectively.

## When to Use

- Starting work on a new project that has no EARS setup
- Onboarding a project that another developer started
- Upgrading a project from generic EARS to project-specific EARS
- After significant project restructuring

## Workflow

### Phase 1: Project Analysis

Scan the project to build a profile:

1. **Detect language and framework:**
   - Look for `package.json` → Node.js/TypeScript
   - Look for `pyproject.toml` or `setup.py` or `requirements.txt` → Python
   - Look for `Cargo.toml` → Rust
   - Look for `go.mod` → Go
   - Look for `pom.xml` or `build.gradle` → Java/Kotlin
   - Look for `*.sln` or `*.csproj` → C#/.NET
   - Look for `Makefile` + `*.c`/`*.cpp`/`*.h` → C/C++
   - Look for `Gemfile` → Ruby
   - Look for `mix.exs` → Elixir
   - Multiple matches = polyglot project

2. **Detect build commands:**
   - `package.json` → read `scripts` (build, test, dev, start)
   - `pyproject.toml` → read `[project.scripts]` and `[tool.pytest]`
   - `Makefile` → list top-level targets
   - `Cargo.toml` → `cargo build`, `cargo test`
   - `go.mod` → `go build`, `go test`

3. **Detect test commands:**
   - Python: `pytest`, `python -m unittest`, `tox`
   - Node.js: `jest`, `vitest`, `mocha`, `npm test`
   - Rust: `cargo test`
   - Go: `go test ./...`
   - Java: `mvn test`, `gradle test`

4. **Understand architecture:**
   - List top-level directories with brief descriptions
   - Read existing README.md for project overview
   - Identify key patterns (monorepo, MVC, microservices, library, CLI tool, etc.)

5. **Check for existing EARS artifacts:**
   - `CLAUDE.md` → exists? has EARS section?
   - `KNOWN_ISSUES.md` → exists?
   - `LEARNING.md` → exists?
   - `traces/` → exists? has content?
   - `ears-config.json` → exists?
   - `.cursor/rules/` → has EARS rules?
   - `AGENTS.md` → exists?

### Phase 2: Generate Project CLAUDE.md

Use the project analysis to fill in a CLAUDE.md. Use the template from the Synapse plugin's `templates/PROJECT-CLAUDE.md` as the base structure.

**If CLAUDE.md already exists:**
- Read it fully
- Check if it has an EARS section
- If no EARS section: offer to append the EARS block
- If has EARS section: compare and offer to update
- NEVER overwrite existing content without asking

**If CLAUDE.md does not exist:**
- Generate a complete one using the template
- Fill in all placeholders from the analysis:
  - Project name from package manifest or directory name
  - Overview from README.md or directory structure
  - Build & test commands from detected tools
  - Architecture from directory scan
  - EARS section fully populated

**The EARS section must include:**
- PostToolUse hook behavior explanation
- All three entry formats (Error, Checkpoint, Dead End) with examples
- Four-tier knowledge architecture with promotion rules
- "How to respond" guidance when seeing `[EARS]` prompts
- Project-specific error patterns to watch for

### Phase 3: Create EARS Skeleton

Create the directory structure and files:

1. **`traces/` directory** — create if missing
2. **Initial trace.md** — ask user for the current task name, create `traces/<task-name>/trace.md`:
   ```markdown
   # Trace: <task-name>

   Started: <current timestamp>
   ```
3. **`KNOWN_ISSUES.md`** — create from template if missing
4. **`LEARNING.md`** — create if missing:
   ```markdown
   # Learning Log

   Tech decisions, new concepts, mistakes, and lessons for this project.
   ```
5. **`ears-config.json`** — create with project-specific error patterns:

   For **Python** projects:
   ```json
   {
     "error_patterns": [
       "Traceback (most recent call last)",
       "SyntaxError:", "TypeError:", "ValueError:", "KeyError:",
       "IndexError:", "AttributeError:", "ImportError:",
       "ModuleNotFoundError:", "FileNotFoundError:", "RuntimeError:",
       "AssertionError:", "PermissionError:", "ConnectionError:"
     ],
     "checkpoint_interval": 10,
     "error_cooldown_seconds": 120,
     "checkpoint_cooldown_seconds": 600,
     "ignore_paths": [".claude/", ".git/", "__pycache__/", ".venv/", ".mypy_cache/"]
   }
   ```

   For **Node.js/TypeScript** projects:
   ```json
   {
     "error_patterns": [
       "ReferenceError:", "TypeError:", "SyntaxError:", "RangeError:",
       "ENOENT:", "EACCES:", "ECONNREFUSED:", "ERR_MODULE_NOT_FOUND",
       "Cannot find module", "Unexpected token", "FATAL ERROR:",
       "UnhandledPromiseRejection"
     ],
     "checkpoint_interval": 10,
     "error_cooldown_seconds": 120,
     "checkpoint_cooldown_seconds": 600,
     "ignore_paths": [".git/", "node_modules/", "dist/", ".next/", "coverage/"]
   }
   ```

   For **Rust** projects:
   ```json
   {
     "error_patterns": [
       "error[E", "panicked at", "fatal runtime error",
       "thread 'main' panicked", "cannot find", "mismatched types",
       "borrow of moved value", "lifetime"
     ],
     "checkpoint_interval": 10,
     "error_cooldown_seconds": 120,
     "checkpoint_cooldown_seconds": 600,
     "ignore_paths": [".git/", "target/"]
   }
   ```

   For **Go** projects:
   ```json
   {
     "error_patterns": [
       "panic:", "fatal error:", "undefined:", "cannot use",
       "too many arguments", "not enough arguments",
       "imported and not used", "declared and not used"
     ],
     "checkpoint_interval": 10,
     "error_cooldown_seconds": 120,
     "checkpoint_cooldown_seconds": 600,
     "ignore_paths": [".git/", "vendor/"]
   }
   ```

   For **other/mixed** projects: use the default patterns from the hook.

### Phase 4: Multi-Tool Setup (Optional)

Ask the user: "Do you use Cursor or Codex for this project? I can generate EARS rules for them too."

**If Cursor is used:**
Generate `.cursor/rules/ears-project.mdc` (create `.cursor/rules/` if needed):
- Use the `templates/cursor-ears.mdc` template
- Fill in project name and tech stack
- Set `alwaysApply: true`

**If Codex is used:**
Generate project-level `AGENTS.md`:
- Use the `templates/PROJECT-AGENTS.md` template
- Fill in project overview, build/test commands, architecture
- Include EARS instructions

### Phase 5: Hook Check (Optional)

1. Check if `~/.claude/scripts/ears-trace.py` exists
2. If it exists, inform the user about the improved hook in the Synapse plugin
3. Offer to install/upgrade:
   - Copy `hooks/ears-trace.py` from the plugin to `~/.claude/scripts/ears-trace.py`
   - Verify `~/.claude/settings.json` has PostToolUse hooks configured
4. If the user declines, that's fine — the existing hook works, just without auto-discovery

## Output Summary

After completion, display a summary:

```
EARS initialized for <project-name>:
  - CLAUDE.md: <created | updated | already exists>
  - traces/<task>/trace.md: created
  - KNOWN_ISSUES.md: <created | already exists>
  - LEARNING.md: <created | already exists>
  - ears-config.json: created (<tech-stack> patterns)
  - Cursor rules: <created | skipped>
  - Codex AGENTS.md: <created | skipped>
  - Hook: <upgraded | current | skipped>

You're ready to go. EARS will automatically prompt you to record
errors, checkpoints, discoveries, and dead ends as you work.
```

## Important Principles

- **Never overwrite** existing files without asking
- **Merge, don't replace** — append EARS sections to existing CLAUDE.md
- **Project-specific** — error patterns, ignore paths, and commands should reflect the actual project
- **Minimal by default** — only create what's needed, ask before adding optional pieces
- **Respect existing setup** — if the project already has EARS, offer upgrades, don't force changes
