# `project_<module>-redesign.md` — Ledger Template

Copy this for a new module, at `~/.claude/projects/<project-dir>/memory/project_<module>-redesign.md` (+ one pointer line in that directory's `MEMORY.md`). Created in Phase 0, read **in full** (not just the newest section) at the start of every resumed session — this single habit is what keeps a multi-session, multi-worktree redesign coherent.

**Living conventions (observed in every real ledger):**
- **Active-round sections are PREPENDED at the top of the file** with a status emoji — `🔜` next round's feedback/asks, `✅` built/done, `⭐` adopted playbook or major pass, `⚠️` not-done/warning — so "read the top" is always "read the current round."
- **Resume prompts cite sections by their literal §names** (e.g. §"IA SIGNED OFF", §"🔜 ROUND 2 FEEDBACK").
- **Every state claim names its commit hash** and a precise status word: `DONE + COMMITTED (<hash>)` / `BUILT + live-verified, UNCOMMITTED` / `BUILT, NOT verified`.

```markdown
# <Module> Redesign — Project Ledger

## 🔜 <ACTIVE ROUND — prepend newest here>
(current round's verbatim feedback / next asks — see Round N Feedback format below)

## Benchmark
What "top 1%" means for this module, stated once, referenced every round.
e.g. "Benchmark: HomeV2 homescreen quality + Airbnb-level polish."
Include the Phase-3 impeccable baseline score (e.g. "baseline 24/40 — redesign must beat it;
acceptance round re-scores").

## Platform Profile
Which profile from SKILL.md (existing web / Flutter / greenfield) and the stack
constraint that follows (e.g. "Chakra 2.5 + framer-motion, frozen").

## House Rules (non-negotiable, carry into every session)
The observed set:
- Color/token usage: e.g. usePlanColors, no hardcoded hex
- API contract: frozen unless a prereq is scoped in §BACKEND SCOPE
- `tsc --noEmit` = 0 (web) / `flutter analyze` = 0 (Flutter) before anything counts as done
- Commit discipline: ask before committing, but checkpoint-ask along the way
- No-delete without explicit confirmation
- Merge gate: who actually merges (name the person)
Recommended default (added 2026-07, not from the observed set — keep or drop deliberately):
- Responsive: components adapt to their CONTAINER, not just the viewport — container
  queries + clamp() fluid type for anything reused across surfaces; verify at the
  breakpoint matrix (mobile 390 / mid 800 / desktop 1280 or the module's real set)
Rounds can amend this block — log the amendment as a dated "rule change."

## Performance Budget (Phase 7 gate — lab numbers via Chrome DevTools MCP trace)
Defaults unless overridden: LCP < 2.5s · INP < 200ms · CLS < 0.1 ·
no wasted-render hotspots (react-scan) on the primary flow.
Flutter: no dropped frames past 16ms on the primary flow in --profile mode.

## Parallel-Work Boundaries
No-touch zones while this worktree is active alongside others, e.g.
"Never touch components/Home/Dash — Home redesign runs concurrently."

## Locked Personas / Constraints
This module's actual users, locked once, cited by reference afterward — never
imported from another module's ledger. e.g. "low-literacy, spotty-connectivity,
cleaning staff on cheap phones — the harshest simplicity bar in this module."

## BACKEND SCOPE
Per-surface classification from Phase 1's backend capability check:
| Surface | FE-only / MIXED | Contract notes (locked Phase 3) | Endpoint status |
|---|---|---|---|

## IA SIGNED OFF
The per-surface locked spec — what the user approved at Phase 3.5 (artifact links +
the decisions). This is the build spec; plans are written only against entries here.
One subsection per surface.

## Surface Status
One line or block per surface, updated as state changes:
§<SURFACE> — <emoji> <state + hash>
e.g. §HEADER v2 — ✅ DONE + COMMITTED (58df750e) · §REVIEW TAB — ✅ BUILT, live-verified,
UNCOMMITTED · §MENU EDITING — ⚠️ REJECTED round 4 (see verbatim quote)

## Shared-Surface Playbook
The canonical recipe for surfaces this module shares with siblings (header, KPI tiles,
list shells): where the recipe originated, how THIS module adapted it, which consumer
modules must be spot-checked when it changes.

## Backend Prereqs
| Prereq | Branch / worktree | Contract locked? | Built? | Committed (hash)? |
|---|---|---|---|---|
Backend commits are user-asked, never automatic.

## Decisions Locked
Running list, most recent first: what was decided, why, which round.

## Round N Feedback
One section per round (Round 1 = the first full pass, logged before feedback exists).
Each round:
- What was reviewed (surfaces) + plan file link: docs/<module>-redesign/round<N>-*.md
- Verbatim user feedback — QUOTE IT, don't paraphrase. "the runner ui is not top 1%
  at all" is a citable record, not a vibe.
- impeccable score if run
- What changed as a result (+ any rule change to House Rules)

## Adopted Playbooks
Which prior module's pattern this one explicitly reused — only when the user said
"do the same as X," never inferred. e.g. "Adopted Food's cohesive-header recipe per
user request 2026-07-07."

## Verify Recipe (tooling gotchas — ours, not the code's)
Dev-server command + port, test login (phone/OTP + quirks: non-auto-submitting OTP,
mobile-viewport route redirects), persistent browser-profile path, viewport matrix.
Recorded at Phase 3 (the audit needs the app live), used every Phase 7.
Code-truth gotchas go in the repo's COMPONENT-REGISTRY.md instead.

## Session Lineage
One line per session, oldest first:
<session-id> · <worktree/branch> · <one-line: what happened + hashes>

## Next Steps
What the next resumed session should do first.
```

---

## Resume-Prompt Shape

Every session ends by handing the user a copy-paste prompt for the next one:

```
Continue the <Module> redesign — <the ONE specific next step>.

READ FIRST, IN FULL: memory project_<module>-redesign.md — especially
§"<literal section name for this round>". Not just the latest entries.

LAUNCH FROM <main repo path> (memory keying); do ALL work in
<worktree path> (branch redesign/<module>-module).

Context: <2-4 lines — surface status with hashes (DONE + COMMITTED (<hash>) /
BUILT + live-verified UNCOMMITTED / REJECTED with the verbatim quote)>.

<Verify Recipe essentials the next session needs: port, login, viewport, gotchas.>
```

Rules: name ONE next step, not a list. State commit status precisely with hashes. Carry rejections as verbatim quotes. Always include the LAUNCH FROM line — a session launched from the worktree path won't auto-load this ledger.

> Companion artifacts: the repo's `docs/design/COMPONENT-REGISTRY.md` (reusable surface) and `docs/<module>-redesign/` (this redesign's specs + round plans). The ledger records *process*; those record *the code's truth* and *the design's spec*. Round close updates all three.
