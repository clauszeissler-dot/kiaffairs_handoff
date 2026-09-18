#!/usr/bin/env python3
"""UserPromptSubmit hook: detect natural-language session-ending phrases and
nudge Claude to run the `/handoff` skill before its final reply.

Why this exists: Claude Code has no hook event that reports remaining
context percentage, so "call the handoff skill at ~20% context" cannot be
enforced mechanically. But a session ending in words ("that's it for today",
"we'll continue tomorrow", "good night") is a reliable, checkable signal —
this hook catches that signal and injects a directive into Claude's context
so it writes the handoff BEFORE responding, instead of relying on Claude to
notice on its own. Ported to Claude Code's UserPromptSubmit +
plain-stdout-as-context mechanism from the equivalent Codex CLI approach.

This hook only ever nudges — it never blocks the prompt (always exit 0).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ENDING_PATTERN = re.compile(
    r"(?:^|.*\b)("
    r"that'?s it for (?:today|now)"
    r"|(?:i'?m|we'?re) (?:done|calling it) for (?:today|now)"
    r"|good night"
    r"|(?:we'?ll|let'?s) (?:continue|pick this up|carry on) tomorrow"
    r"|see you tomorrow"
    r"|ende f(?:ü|u)r heute"
    r"|f(?:ü|u)r heute (?:reicht(?: es)?|ist (?:schluss|genug))"
    r"|feierabend"
    r"|gute nacht"
    r"|bis (?:morgen|sp(?:ä|a)ter)"
    r"|wir (?:machen|setzen) (?:morgen|sp(?:ä|a)ter) (?:weiter|fort)"
    r")[.!…]*$",
    re.IGNORECASE,
)

SAFETY_NET_SCRIPT = Path(__file__).parent / "auto-handoff-safety-net.sh"


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    prompt = normalize(str(event.get("user_prompt", "")))
    if not ENDING_PATTERN.search(prompt):
        return 0

    snapshot_status = "Safety-net snapshot could not be started."
    if SAFETY_NET_SCRIPT.is_file():
        try:
            result = subprocess.run(
                ["bash", str(SAFETY_NET_SCRIPT), "sessionend"],
                cwd=event.get("cwd") or ".",
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            snapshot_status = (
                "A minimal safety-net snapshot was already written."
                if result.returncode == 0
                else "The safety-net snapshot failed; write the full handoff anyway."
            )
        except (OSError, subprocess.TimeoutExpired):
            pass

    print(
        "MANDATORY HANDOFF TRIGGER: the user is ending this session. "
        f"{snapshot_status} Before your final reply, run the `handoff` skill "
        "now and write the full handoff document to disk."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
