# Gate 4: Harvest (at every commit, and at handoff)

**Why this gate exists.** Every session re-derives the same facts: which token exists, which helper matches by id and not by name, that there are six hand-rolled dropzones, that the preview pane is 800px. The origin sessions ran the same Explore agents again and again and threw the answers away. "Update the registry at round close" was prose, and prose does not fire. This is the moment it fires.

**The hook.** Any `git commit` fires it. The handoff checklist fires it again.

## The five questions (answer each with one line, or "none")

| # | Did this stretch produce… | It goes to |
|---|---|---|
| 1 | **a rule**: something that must be true on every surface from now on | `gates.md` (taste bar / code bar) if it fired in two modules; the module's LOCKS if it fired in one |
| 2 | **a reusable**: a component, token, hook or helper with a path, and when NOT to use it | the repo's `docs/design/COMPONENT-REGISTRY.md` |
| 3 | **a pattern**: a problem and the house's answer to it, with `file:line` | the repo's `docs/design/PATTERNS.md` (repo-specific) or this skill's `references/patterns.md` (true across repos) |
| 4 | **a trap**: a tooling or environment fact that cost time | `references/traps.md` |
| 5 | **a working note**: something about how the work went with the stakeholder — what he corrected, what he had to say twice, what turned out to be his call and not yours, what he hedged about and was right about | the Working Contract in `gates.md` |

The fifth question exists because it is the one that got skipped. On 2026-09-14 the harvest for a two-day payment-page session produced six traps and five patterns, every one of them about the artifact, and nothing at all about the working relationship — until he asked "did you go through the behavioural things, what did I correct, how we worked?" Questions 1 to 4 cannot catch that omission: they all ask what the code taught you. This one asks what he taught you, and it is the half that decides how many rounds the next session takes. It fails the "already recorded" test often, and that is fine — check the Working Contract first and write nothing if it is there.

A **do-not-copy** is a reusable with a negative sign: register it in the registry's do-NOT-copy section with the reason and the replacement.

## The four tests (all four, or it is not saved)

1. **Re-derivation cost.** A fresh session would spend more than five minutes finding this out.
2. **Stable.** It is not a one-off of this task. It will still be true next month.
3. **Not already recorded.** Not in the code, the git history, CLAUDE.md, or one of the files above. Grep first.

4. **Runnable.** If the entry prescribes a command, the command has been run on this machine, once, and its output seen. On 2026-09-14 an entry told every future session to wrap a vault write in `timeout 30`; macOS has no `timeout`, so the guarded command silently never ran. A grep of every session transcript found that failure **95 times across 12 sessions and three projects**, unrecorded for months, while the entry prescribing it sat in the learnings file. **A wrong entry is worse than no entry, because it prescribes the failure and the failure is silent.**

## How an entry looks

One line, keyed by the question a session would ask, never by the date it was learned:

```
| Sticky first cell that cannot slide | `ComplaintSetup/tokens.ts:177` `stickyTypeCell` | pins at resting x via negative margin; pair with STICKY_EDGE |
```

Dates belong in `learnings.md`, which keeps the story behind a rule and links to it. The registry files are lookup tables, not diaries.

## Promotion, not accumulation

- A pattern that fired in **two repos** is promoted from the repo's `PATTERNS.md` to this skill's `patterns.md`.
- A rule that fired **twice** is promoted from LOCKS to `gates.md`; a gate that fired in **three sessions** is promoted to global CLAUDE.md.
- Everything else stays where it was born. The files grow by promotion, so they stay short enough to read.

## Rot

Every entry carries a path. `scripts/registry_rot.py <repo-root>` checks every `path:line` and backticked path in the registry files still exists, and prints the dead ones. Run it at the same commit. A stale registry is worse than none, and staleness is caught by a script, not by a reader.

```
python3 ~/.claude/skills/module-redesign-pipeline/scripts/registry_rot.py "$(git rev-parse --show-toplevel)"
```

## Where the registry lives

Per-repo facts live **in the repo**, committed: `docs/design/COMPONENT-REGISTRY.md` and `docs/design/PATTERNS.md`. They ride the PR, engineers see them, other worktrees get them. An untracked registry is a private note (2026-08-23: it had been untracked on main for two days and invisible to every worktree).

Cross-repo facts live **in this skill**: `gates.md`, `patterns.md`, `traps.md`.
