# Wiring the Gates (do this once per machine)

The skill files (`SKILL.md`, `references/gates.md`, `scripts/`) only give an agent the *rules*. **Enforcement is two hooks in `~/.claude/settings.json`**, which is a per-user, per-machine file — it is not part of a skill and does not install itself when you copy the skill folder. Without this step, Gates 1 and 3 never fire, and nothing reminds anyone to run the Done Probe before a commit.

## Prerequisites

- `jq` on PATH (`brew install jq` / `apt install jq`).
- Python 3 with Playwright for the Done Probe: `pip install playwright && python3 -m playwright install chromium`.
- The skill installed at `~/.claude/skills/module-redesign-pipeline/` (personal) or your project's `.claude/skills/module-redesign-pipeline/` (project-scoped — adjust the paths below to match).

## Install

1. Open `~/.claude/settings.json`. If it doesn't exist, create it with `{"hooks": {}}`.
2. Merge the block below into `hooks.PreToolUse`. If you already have a `PreToolUse` array, **append** these two entries to it — don't replace what's there.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "jq -r '.tool_input.file_path // empty' | { read -r f; case \"$f\" in */tokens.ts|*/tokens.tsx|*/primitives.tsx|*/constants.ts|*/theme/*|*/components/Common/*|*/components/HomeV2/shared/*|*/peopleListHeader.tsx) printf '%s' '{\"hookSpecificOutput\": {\"hookEventName\": \"PreToolUse\", \"additionalContext\": \"Gate 3, Shared Primitive (tokens, primitives, shared header, layout helper, theme). Before editing: grep every consumer and read how each uses this; one concern per function (a helper that positions must not also pad, a later prop will silently win); ask what else can set the same CSS property on that element. After editing: re-run the Done Probe on at least one consumer per kind at 375 and 1440: $HOME/.claude/skills/module-redesign-pipeline/scripts/run_probe.py. Full text: $HOME/.claude/skills/module-redesign-pipeline/references/gates.md\"}, \"suppressOutput\": true}' ;; */components/*.tsx|*/components/**/*.tsx|*/lib/*/widgets/*.dart|*/lib/*/screens/*.dart) if [ ! -e \"$f\" ]; then printf '%s' '{\"hookSpecificOutput\": {\"hookEventName\": \"PreToolUse\", \"additionalContext\": \"Gate 1, Surface Ready (new UI component file). Before building ANY surface, including a modal, dock, toast, popover, footer or empty state, the seven answers must exist and have been seen by the stakeholder: 1 what it IS in one noun sentence; 2 the question she came with; 3 the internal precedent by file; 4 two outside references pulled (Mobbin) with one idea each; 5 two rendered directions; 6 your pick and why; 7 what the spec gets wrong. Open the drawn artifact, not the prose. If all seven are written and approved, proceed. If not, stop and write them. Full text: $HOME/.claude/skills/module-redesign-pipeline/references/gates.md\"}, \"suppressOutput\": true}'; fi ;; esac; }"
        }
      ]
    },
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "jq -r '.tool_input.command // empty' | { read -r c; case \"$c\" in *'git commit'*) if git diff --cached --name-only 2>/dev/null | /usr/bin/grep -qE '(components|widgets|screens)/.*\\.(tsx|dart)$'; then printf '%s' '{\"hookSpecificOutput\": {\"hookEventName\": \"PreToolUse\", \"additionalContext\": \"Gate 2, Done Probe. This commit touches UI components. '\\''Verified'\\'' means numbers, not a claim: run $HOME/.claude/skills/module-redesign-pipeline/scripts/run_probe.py --url <page> --profile <pw-profile> --widths 375,1440 and paste the summary lines into the commit message. Pass = every control in a row on one centre (within 2px), sticky x unchanged after a pan and no sticky cell shorter than a sibling, every popover portaled with an 8px gutter, no icon at 0px, flex peers within 2px, no sideways page scroll, first content row y on the phone stated and judged, zero cards opened by a programmatic focus. The preview pane'\\''s desktop preset is 800px: set 1440 explicitly. Also: tsc 0, lint 0/0, check files pass. If already run for this diff, proceed. Full text: $HOME/.claude/skills/module-redesign-pipeline/references/gates.md\"}, \"suppressOutput\": true}'; fi ;; esac; }"
        }
      ]
    }
  ]
}
```

3. **Adjust the file-path globs to your stack.** The `Write|Edit` matcher's `case` patterns (`*/tokens.ts`, `*/components/*.tsx`, `*/lib/*/widgets/*.dart`, …) assume a React/Chakra + Flutter layout, because that's what the origin project uses. Point them at wherever *your* repo keeps shared primitives and UI components — a wrong glob means the gate silently never fires, which is worse than not having it, because it looks installed.
4. Restart Claude Code (or start a new session) so it picks up the new hook config.

## Verify it actually fires

```bash
echo '{"tool_input":{"file_path":"/absolute/path/to/some/NewComponent.tsx"}}' \
  | jq -r '.tool_input.file_path // empty' \
  | { read -r f; case "$f" in */components/*.tsx) [ ! -e "$f" ] && echo "Gate 1 would fire"; esac; }
```

You should see `Gate 1 would fire` for a path that doesn't exist yet on disk, and nothing for a path that does (editing an existing component doesn't re-litigate its design).

## Why this isn't baked into the skill install

Claude Code skills are read-only reference material the agent loads into context; they cannot register hooks on their own, and a skill silently rewriting `settings.json` on first use would be a surprising, hard-to-audit side effect. So installing the skill gives you the *rules* immediately; wiring the hooks (this file) is what turns them into a *standard* nobody can skip by not reading — do both.
