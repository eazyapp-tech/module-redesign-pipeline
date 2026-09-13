# Component Registry — `<repo/app name>` Template

Copy this into the target repo as `docs/design/COMPONENT-REGISTRY.md` (that exact path — Phase 1 reads it there). It lives **in the repo, versioned with the code** — team-visible, not trapped in Claude memory. This is the index that makes "reuse, don't recreate" cheap and reliable; the ledger stays the per-module process record.

> **Read before building ANY new UI element. Update at every round close.**
> A stale registry is worse than none — every entry cites a real path; verify the paths you're about to rely on before trusting them (Phase 1 does this for the module's surface).

## How to use (the non-blind reuse loop)

1. **Before creating a component:** search here first. Found → read its "When NOT to use" and adaptation notes, then adapt the *underlying idea* to your surface — cohesion is the north star, literal copying is not.
2. **Not found here:** run one Explore pass over the codebase to confirm it genuinely doesn't exist (the registry indexes, it doesn't guarantee completeness), then build new.
3. **Built something reusable:** register it at round close — name, path, use/not-use, gotchas. An unregistered reusable component is the seed of the next duplicate.
4. **Found a copy-with-drift:** log it under Extraction Candidates. Three call sites with near-copies = extract to canonical, then register.

## Canonical components

| Component | Path | Use for | When NOT to use | Gotchas / adaptation notes | Used by |
|---|---|---|---|---|---|
| e.g. PeopleListHeader | `components/.../PeopleListHeader.tsx` | Section headers with search/filter/tabs | Full-bleed marketing-style heroes | Folds tiles past 40px scroll via TableScroll — don't fight it | Tasks, Rooms |

## Layout & shell patterns

Recipes bigger than one component — the things that got "ported" module to module:
- e.g. Cohesive header (gradient merge with global header): origin `<module/path>`, adapted by `<modules>` — adaptation notes, not a literal copy.
- e.g. Two-pane editor (card stack + sticky live preview): origin `<path>`.

## Tokens & hooks

| Token/Hook | Path | Rule |
|---|---|---|
| e.g. usePlanColors | `<path>` | ALL plan-tier colors — hardcoded hex is a build failure |
| e.g. spacing scale | DESIGN.md §spacing | 20px card gaps, 12–16px section gaps |

## House conventions

Naming, file placement, state patterns, a11y patterns, motion durations — the rules that make new code look native. Keep each to one line; link DESIGN.md for the visual system itself.

## Legacy / do-NOT-copy

As load-bearing as the canonical list — what looks reusable but must not spread:

| Component | Path | Why not | Use instead |
|---|---|---|---|
| e.g. old Reviews components | `components/Property/Reviews/` | Pre-redesign, superseded by ReviewsV2 | `components/Property/ReviewsV2/` |

## Extraction candidates

Near-duplicates spotted but not yet unified. Three+ call sites → extract, register above, delete this row.

| Pattern | Copies at | Blocking? |
|---|---|---|

## Gotchas, workarounds & learnings (append-only, dated)

Code-truths only — things about THIS codebase that cost a session to learn. (Tooling gotchas — dev-server login quirks, viewport routing — go in the module ledger's verify recipe instead.)

- `YYYY-MM-DD` — `<gotcha>` → `<workaround>` (source: `<module/round>`)
