#!/usr/bin/env python3
"""EARS (Evolving Autonomous Research System) — Improved PostToolUse Hook.

Combines the best of the original Python hook and the EARS-deploy bash hook:
- trace.md auto-discovery (walks up directory tree)
- Per-context naming and rate limiting
- Missing trace.md reminders
- Project-specific error patterns via ears-config.json
- Noise filtering for false positives
- Windows-compatible (no jq/bash dependency)

Triggers:
  Path A: Error detection after Bash commands (120s cooldown per context)
  Path B: Periodic checkpoint every 10 Write/Edit ops (10min cooldown per context)
  Path C: Missing trace.md reminder (5min cooldown per context)

Input: JSON from Claude Code hook system via stdin
Output: JSON with additionalContext to inject EARS prompts
"""

import sys
import json
import time
import re
import tempfile
from pathlib import Path
from datetime import datetime

DEFAULT_ERROR_PATTERNS = [
    "Traceback (most recent call last)",
    "FATAL:",
    "fatal:",
    "fatal error",
    "CONFLICT (",
    "merge conflict",
    "CalledProcessError",
    "SyntaxError:",
    "TypeError:",
    "ValueError:",
    "KeyError:",
    "IndexError:",
    "AttributeError:",
    "ImportError:",
    "ModuleNotFoundError:",
    "FileNotFoundError:",
    "PermissionError:",
    "RuntimeError:",
    "AssertionError:",
    "ZeroDivisionError:",
    "NameError:",
    "OSError:",
    "ConnectionError:",
    "ConnectionRefusedError:",
    "TimeoutError:",
    "HTTPError:",
    "panic:",
    "PANIC:",
    "command not found",
    "Permission denied",
]

NOISE_PATTERNS = [
    "0 error",
    "0 Error",
    "no error",
    "No Error",
    "error: 0",
    "errors: 0",
    "Error: 0",
    "Errors: 0",
]

SKIP_PATH_SEGMENTS = {
    ".claude", ".git", "__pycache__", "node_modules",
    ".egg-info", ".mypy_cache", ".pytest_cache", ".tox",
}

ERROR_COOLDOWN = 120
CHECKPOINT_COOLDOWN = 600
CHECKPOINT_INTERVAL = 10
REMINDER_COOLDOWN = 300


def find_trace_context(file_path, cwd):
    """Walk up from file (then cwd) to find nearest trace.md or repo root.

    Returns (context_dir, context_name, has_trace).
    """
    for start in [file_path, cwd]:
        if not start:
            continue
        d = Path(start)
        if not d.is_dir():
            d = d.parent
        while d != d.parent:
            if (d / "trace.md").exists():
                return d, d.name, True
            if (d / ".git").exists() or (d / ".git").is_file():
                return d, d.name, False
            d = d.parent
    return None, None, False


def should_skip(file_path):
    """Skip meta-files and trace.md self-edits."""
    if not file_path:
        return False
    p = Path(file_path)
    if p.name == "trace.md":
        return True
    for part in p.parts:
        if part in SKIP_PATH_SEGMENTS:
            return True
    return False


def load_project_config(context_dir):
    """Load project-specific EARS config if ears-config.json exists."""
    if not context_dir:
        return {}
    config_file = Path(context_dir) / "ears-config.json"
    if config_file.exists():
        try:
            return json.loads(config_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def get_error_patterns(project_config):
    """Merge default and project-specific error patterns."""
    custom = project_config.get("error_patterns", [])
    if custom:
        combined = list(DEFAULT_ERROR_PATTERNS)
        for p in custom:
            if p not in combined:
                combined.append(p)
        return combined
    return DEFAULT_ERROR_PATTERNS


def has_real_error(text, patterns):
    """Check if text contains real error patterns, filtering noise."""
    if any(noise in text for noise in NOISE_PATTERNS):
        clean = text
        for noise in NOISE_PATTERNS:
            clean = clean.replace(noise, "")
        return any(p in clean for p in patterns)
    return any(p in text for p in patterns)


def extract_file_path(tool_name, tool_input):
    """Extract the relevant file path from tool input."""
    if tool_name in ("Write", "Edit"):
        return tool_input.get("file_path", "")
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        match = re.search(r'(?:papers|benchmarks|src|lib|app|tests?|scripts?)/[^\s]+', cmd)
        return match.group(0) if match else ""
    return ""


def state_file_for(ctx_name, kind):
    """Per-context state file in temp directory."""
    tmp = Path(tempfile.gettempdir())
    return tmp / f"ears_{ctx_name}.{kind}"


def check_cooldown(ctx_name, kind, cooldown_seconds):
    """Check and update rate limit. Returns True if action is allowed."""
    sf = state_file_for(ctx_name, kind)
    now = time.time()
    if sf.exists():
        try:
            last = sf.stat().st_mtime
            if (now - last) < cooldown_seconds:
                return False
        except OSError:
            pass
    try:
        sf.write_text(str(now))
    except OSError:
        pass
    return True


def get_op_count(ctx_name):
    """Get and increment per-context operation count."""
    sf = state_file_for(ctx_name, "ops")
    count = 0
    if sf.exists():
        try:
            count = int(sf.read_text().strip())
        except (ValueError, OSError):
            pass
    count += 1
    try:
        sf.write_text(str(count))
    except OSError:
        pass
    return count


def make_output(event_name, context):
    """Build the JSON output for Claude Code hook system."""
    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
        }
    }


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    event_name = hook_input.get("hook_event_name", "")
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})
    tool_response = hook_input.get("tool_response", {})
    cwd = hook_input.get("cwd", "")

    file_path = extract_file_path(tool_name, tool_input)

    if should_skip(file_path):
        sys.exit(0)

    context_dir, ctx_name, has_trace = find_trace_context(file_path, cwd)
    if not context_dir:
        sys.exit(0)

    project_config = load_project_config(context_dir)
    error_patterns = get_error_patterns(project_config)
    interval = project_config.get("checkpoint_interval", CHECKPOINT_INTERVAL)
    err_cooldown = project_config.get("error_cooldown_seconds", ERROR_COOLDOWN)
    cp_cooldown = project_config.get("checkpoint_cooldown_seconds", CHECKPOINT_COOLDOWN)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = None

    # --- Path A: Error detection (Bash) ---

    if event_name == "PostToolUseFailure":
        error_msg = hook_input.get("error", "unknown error")
        if check_cooldown(ctx_name, "err", err_cooldown):
            command = tool_input.get("command", "unknown")
            output = make_output("PostToolUseFailure", (
                f"[EARS] {ctx_name}: Error detected.\n"
                f"Command: {command}\n"
                f"Error: {error_msg}\n\n"
                f"After you fix it, append to trace.md:\n\n"
                f"### EARS — Error ({timestamp})\n"
                f"- Problem: what failed and the error message\n"
                f"- Diagnosis: how you identified the root cause\n"
                f"- Fix: what you changed and why it works\n"
                f"- Lesson: what would prevent this in the future"
            ))

    elif tool_name == "Bash":
        response_str = (
            json.dumps(tool_response, ensure_ascii=False)
            if isinstance(tool_response, dict)
            else str(tool_response)
        )
        tail = response_str[-3000:] if len(response_str) > 3000 else response_str

        if has_real_error(tail, error_patterns):
            if check_cooldown(ctx_name, "err", err_cooldown):
                command = tool_input.get("command", "unknown")
                output = make_output("PostToolUse", (
                    f"[EARS] {ctx_name}: Error pattern detected in: {command}\n\n"
                    f"After you fix it, append to trace.md:\n\n"
                    f"### EARS — Error ({timestamp})\n"
                    f"- Problem: what failed and the error message\n"
                    f"- Diagnosis: how you identified the root cause\n"
                    f"- Fix: what you changed and why it works\n"
                    f"- Lesson: what would prevent this in the future"
                ))

    # --- Path B: Periodic checkpoint (Write/Edit) ---

    if tool_name in ("Write", "Edit") and output is None:
        count = get_op_count(ctx_name)

        if count % interval == 0:
            if check_cooldown(ctx_name, "cp", cp_cooldown):
                output = make_output("PostToolUse", (
                    f"[EARS] {ctx_name}: Checkpoint — {interval} file operations "
                    f"since last reflection.\n\n"
                    f"Update trace.md if any of these apply:\n\n"
                    f"### EARS — Checkpoint ({timestamp})\n"
                    f"- Problem solved: what broke, how you debugged it, what fixed it\n"
                    f"- Discovery: something surprising or non-obvious you learned\n"
                    f"- Decision: a design choice you made and the trade-off\n"
                    f"- Dead end: an approach you abandoned and why it failed\n\n"
                    f"Skip if nothing notable happened."
                ))

    # --- Path C: Missing trace.md reminder ---

    if not has_trace and output is None and tool_name in ("Write", "Edit"):
        if check_cooldown(ctx_name, "remind", REMINDER_COOLDOWN):
            output = make_output("PostToolUse", (
                f"[EARS] {ctx_name}: No trace.md found. "
                f"Create one to capture your problem-solving experience:\n\n"
                f"  # Trace: {ctx_name}\n\n"
                f"Place it in the project root or task subdirectory."
            ))

    if output:
        json.dump(output, sys.stdout)

    sys.exit(0)


if __name__ == "__main__":
    main()
