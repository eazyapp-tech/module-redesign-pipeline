#!/usr/bin/env python3
"""Gate 4 (Harvest) and Gate 5 (State Census), fired on `git commit`.

Both gates were documented as hook-fired and neither was. The skill's own
argument is that a rule you have to recall is advice, and that is what they
were: on 14 Sep 2026 a four-day project reached its end with no working note
written, exactly the failure Harvest exists to prevent.

Harvest fires on any commit. State Census fires when the staged diff carries UI,
because that is when unrendered states ship.
"""
import json
import re
import subprocess
import sys

GATES = "$HOME/.claude/skills/module-redesign-pipeline/references/gates.md"

HARVEST = (
    "Gate 4, Harvest. Before this commit, answer five questions with one line each or "
    "\"none\": (1) a rule that must hold on every surface from now on, (2) a reusable with a "
    "path and when NOT to use it, (3) a pattern, problem plus the house's answer, with "
    "file:line, (4) a trap, a tooling or environment fact that cost time, (5) a WORKING NOTE, "
    "something about how the work went with the stakeholder: what they corrected, what they had "
    "to say twice, what they hedged about and were right about, what turned out to be their call "
    "and not yours. Question 5 is the one that gets skipped, because the first four all ask what "
    "the code taught you and none of them can notice that nothing was written about how the work "
    "ran. Save an answer only if it passes four tests: worth more than five minutes for a fresh "
    "session to re-derive, stable, not already recorded, and RUNNABLE, meaning that if it "
    "prescribes a command you have run that command here once and seen its output. A wrong entry "
    "is worse than none: it prescribes the failure and the failure is silent. Rule to gates.md, "
    "reusable to the repo's COMPONENT-REGISTRY.md, pattern to PATTERNS.md or the skill's "
    "patterns.md, trap to traps.md, working note to the Working Contract in gates.md. "
    f"Full text: {GATES}"
)

CENSUS = (
    "Gate 5, State Census. This commit carries UI, so before calling the module done: list EVERY "
    "branch that renders a screen, taken from the code and not from memory. Early returns, status "
    "values, error and empty and loading paths, server-side redirects and notFound. Force each one, "
    "LOOK at it, and judge it against the same bar as the happy path. Count how many people reach "
    "each state before deciding what it deserves. Pass condition: one row per branch with the state, "
    "how it was forced and a screenshot, every row filled or explicitly marked unreachable. This "
    "exists because five states that lived in the code as plumbing shipped unlooked-at on a real "
    "payment page, including the one most arrivals land on. Reasoning about a screen you have not "
    "seen is how a confident wrong rationale gets written. "
    f"Full text: {GATES}"
)

UI = ("components/", "widgets/", "screens/", "pages/", "/p2/")
UI_EXT = (".tsx", ".jsx", ".dart", ".vue", ".svelte", ".js", ".css")

# `git commit` must be the command being RUN, not the words appearing inside a
# quoted string. A plain substring test fired this gate on a command that merely
# contained the phrase, twice, within minutes of it being wired up. So: strip
# quoted spans first, then require a command boundary (start of line, or ; && || |).
# Bias stays toward firing, because a missed real commit is the failure this gate
# exists to prevent and a spurious reminder only costs a few lines.
QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")
IS_COMMIT = re.compile(r"(?:^|[;&|]\s*|\n\s*)git\b[^;&|\n]{0,80}?\bcommit\b")


def staged_touches_ui() -> bool:
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=5,
        ).stdout
    except Exception:
        return False
    for line in out.splitlines():
        if line.endswith(UI_EXT) and any(p in line for p in UI):
            return True
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if not IS_COMMIT.search(QUOTED.sub(" ", cmd)):
        return 0

    parts = [HARVEST]
    if staged_touches_ui():
        parts.append(CENSUS)

    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": "\n\n".join(parts),
        },
        "suppressOutput": True,
    }, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
