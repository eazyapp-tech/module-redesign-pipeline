# `project_<module>-redesign.md` — Ledger Template

Copy this structure for a new module redesign. Read the whole file (not just the newest section) at the start of every resumed session — this single habit is what keeps a multi-session, multi-worktree redesign coherent.

```markdown
# <Module> Redesign — Project Ledger

## Benchmark
What "top 1%" means for this module, stated once, referenced every round.
e.g. "Benchmark: HomeV2 homescreen quality + Airbnb-level polish. Goal: top 1% world-class design."

## House Rules (non-negotiable, carry into every session)
- Color/token usage: e.g. usePlanColors, no hardcoded hex
- API contract: frozen unless a prereq is explicitly scoped (see Backend Prereqs below)
- `tsc --noEmit` must be 0 before anything counts as done
- Commit discipline: ask before committing, but checkpoint-ask along the way
- No-delete without explicit confirmation
- Merge gate: who actually merges (name the person)

## Parallel-Work Boundaries
No-touch zones while this module's worktree is active alongside others, e.g.:
"Never touch components/Home/Dash — Home redesign is running concurrently in another worktree."

## Locked Personas / Constraints
The user(s) this surface actually serves, locked once, cited by reference afterward —
not re-argued every round. e.g. "low-literacy, spotty-connectivity, cleaning staff on
cheap phones — the harshest simplicity bar in this module."

## Backend Prereqs
Any backend change this redesign required, and its status:
- [ ] <endpoint/model change> — committed in <worktree path>, branch <name>

## Decisions Locked
Running list, most recent first. Each entry: what was decided, why, which round.

## Round N Feedback
One section per round. Each round:
- What was reviewed (screens/surfaces)
- Verbatim user feedback — QUOTE IT, don't paraphrase. A rejection like
  "the runner ui is not top 1% at all" is a citable record, not a vibe.
- impeccable score if run (e.g. 36/40)
- What changed as a result

## Adopted Playbooks
Which prior module's pattern this one explicitly reused, and why — only recorded
when the user actually said "do the same as X," not inferred.
e.g. "Adopted Food's cohesive-header recipe per user request 2026-07-07."

## Session Lineage
One line per session, oldest first:
<session-id> · <worktree/branch> · <one-line: what happened>

## Next Steps
What the next resumed session should do first.
```

---

## Resume-Prompt Shape

Every session ends by handing the user a copy-paste prompt for the next one. The shape that worked across all real sessions:

```
Continue the <Module> redesign — <the one specific next step>.

READ FIRST, IN FULL: memory project_<module>-redesign.md — especially
§"<the section with this round's context>". Not just the latest entries.

Context: <2-4 lines — what's DONE (committed vs uncommitted vs unverified),
what was rejected and the verbatim quote if any, which worktree/branch>.

<Any live-verify specifics the next session needs: dev-server port, test
login, viewport, known gotchas.>
```

Rules: name ONE next step, not a list. State commit status precisely (done+committed / built+unverified / rejected). Carry rejections as verbatim quotes.
