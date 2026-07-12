---
name: module-redesign-pipeline
description: >-
  Use when redesigning an EXISTING module, screen, or section to a "top 1% / world-class"
  bar — visual craft, IA, motion, and UX-writing overhaul with business logic essentially
  unchanged (backend changes only as scoped prereqs). Trigger on "redesign this module",
  "make X top 1%", "complete design overhaul", "audit and rebuild this screen", "this
  looks generic/dated, fix it", or any resumed "continue the X redesign" session. NOT for
  a feature that doesn't exist yet — that is feature-design-pipeline's job.
---

# Module Redesign Pipeline

Turn "this module looks generic / dated / not top 1%" into a shipped, live-verified redesign — grounded in the module's real code, benchmarked against real reference products where no internal precedent exists, gated by a scored audit and real performance traces, and never accepted on a claim alone. This is the recipe mined from 66+ real sessions across the Reviews, Food/FoodV2, Tasks, and Change Room redesigns — every phase below is what was actually invoked, not a theoretical pipeline.

This skill **orchestrates other skills** — it doesn't replace `impeccable`, `interface-design`, or `emil-design-eng`, it invokes them in the right order with the right gates in between. (Skill names from the superpowers suite are written with the `superpowers:` prefix; depending on install they may resolve unprefixed — same skills.)

## What this is / isn't

- **Is:** the path from "this existing module is bad" to a merged, live-verified redesign — audit → lock → build → motion → verify → final gate → ship. Owns implementation, not just docs.
- **Isn't:** `feature-design-pipeline` (a NEW feature/backend spec that doesn't exist yet — that pipeline stops at a design doc and hands off; if the module doesn't exist yet, use that one, not this). Isn't a bug fix. Isn't a rewrite of business logic — backend changes happen only as scoped prereqs (see Backend Prereqs below).

## The one hard gate

**Lock the design with the user before any code, and don't claim "done" without live proof.** Two separate checkpoints, not one:
1. **Pre-code (Phase 3.5):** present the proposed design as a **rendered artifact** (`artifact-design`), per surface — not prose. The user approving *that artifact* is the lock. No implementation starts on an un-locked design — "the user is design-exacting."
2. **Pre-"done" (Phase 7):** nothing is accepted as finished on a claim. It gets verified live (real login, real viewport, real screenshot) before it's reported complete.

## Phase 0 setup (first session in a module — do these before the pipeline)

1. **Preflight the tools.** Check Mobbin MCP and Chrome DevTools MCP are connected (`mcp__mobbin__*`, `chrome-devtools`). Fallbacks if absent — log the substitution in the ledger: web reference search instead of Mobbin; playwright tracing + Lighthouse CLI instead of the DevTools trace.
2. **Create the ledger** from `references/redesign-ledger-template.md`, at the project's memory directory: `~/.claude/projects/<project-dir>/memory/project_<module>-redesign.md` (+ a pointer line in that directory's `MEMORY.md`). House Rules, persona, platform profile, and perf budget get locked into it as the framing produces them.
3. **Create the module worktree**: `git worktree add "../<repo>-<module>" -b redesign/<module>-module` from the default branch. Branch naming is a convention, not a suggestion: FE = `redesign/<module>-module`; backend prereqs = `feat/<module>-<thing>` (fixes: `fix/...`) in their own worktree `../<backend-repo>-<thing>`.
4. **Session launch rule (every session, not just the first):** resume prompts say "LAUNCH FROM `<main repo path>` (memory keying); do ALL work in `<worktree path>` (branch `<name>`)" — the ledger auto-loads off the launch directory, so a session launched from the worktree path won't see it. Session-open preflight: `git worktree list && git branch --show-current` in the named worktree before any edit (a real session once built on the wrong base).

## Scaffolding (persistent, not a phase)

- **A per-module redesign ledger** — `project_<module>-redesign.md` (location above), read **in full** (not just latest entries) at the start of every resumed session. Structure: see the template — its section vocabulary (§IA SIGNED OFF, §BACKEND SCOPE, §Surface Status, §SHARED-SURFACE PLAYBOOK, emoji-status prepend-to-top convention) is what real resume prompts navigate by.
- **A per-repo component registry** — `docs/design/COMPONENT-REGISTRY.md` in the target repo, versioned with the code. Canonical components (path, use / when-NOT-to-use, adaptation gotchas), layout/shell recipes, tokens & hooks, house conventions, a **do-NOT-copy legacy list**, extraction candidates, and dated code-truth learnings. See `references/component-registry-template.md`. This is what stops every session re-deriving "map the canonical header pattern" from scratch — the origin sessions ran those Explore agents repeatedly and threw the answers away. First session in a repo without one: the Phase-1 Ground output IS the seed registry — write it, don't discard it.
- **Per-round plans and specs live in the worktree**, committed: `docs/<module>-redesign/` (e.g. `<surface>-plan.md`, `round<N>-<name>-plan.md`). The ledger's Round-N sections link them by path. Three knowledge homes total: registry = the repo's reusable surface; `docs/<module>-redesign/` = this redesign's specs/plans; ledger = process, decisions, feedback, lineage.
- **Two-commit rhythm per accepted stretch:** commit the accepted baseline first, then the polish pass as its own commit — both hashes logged in the ledger. Every state claim in ledger or resume prompt names its commit hash and a precise status word: `DONE + COMMITTED (<hash>)` / `BUILT + live-verified, UNCOMMITTED` / `BUILT, NOT verified`.
- **Cross-module playbook inheritance — always user-triggered, never assumed.** Only when the user explicitly says "recall how we did X, do the same for Y." The observed procedure when triggered: one `Explore` per prior module's ledger to extract its playbook (in parallel) + one `Explore` to locate the new module in code + one `general-purpose` agent to live-audit the new module in the browser — then synthesize into this module's fresh ledger. Personas still lock fresh (see Design Principles).

## The pipeline

| # | Phase | Skill / tool | Notes |
|---|---|---|---|
| 0 | **Frame** | Run `feature-design-pipeline`'s framing steps **inline** for a brand-new module redesign — restate the ask, expand it, state it back for alignment. Do NOT invoke the full skill (its doc stack — `brief`, `pre-mortem`, `domain-modeling`, `grilling`, `doc-handoff-review` — must not run; the module already exists and the Phase-3 audit is the spec). `superpowers:brainstorming` alone for a new screen/tab inside an in-flight module | Nothing gets touched before the restated ask is aligned. If the user triggered playbook inheritance, run the inheritance procedure (Scaffolding, above) now |
| 1 | **Ground** | Component registry first, then `Explore` subagents (2–5 in parallel) for the gaps | **Registry-first:** read `COMPONENT-REGISTRY.md` and verify the entries this module will touch (paths still real, components unchanged — a stale registry is worse than none). Explore agents then map what the registry doesn't cover: this module's end-to-end flow and real data shapes. **One dispatch is always a backend capability check** — what do the current endpoints/templates actually allow for the surfaces in scope? Its output classifies each surface FE-only vs MIXED in the ledger's §BACKEND SCOPE. Discoveries get written INTO the registry, not discarded |
| 1.5 | **Reference** | **Mobbin MCP** (`search_flows` / `search_screens` / `search_sections`) | Only for surfaces with no internal precedent (a new onboarding flow, an analytics dashboard). Pick the *best ideas*, never copy wholesale. This is the actual reference mechanism — not Figma, not any catalogued "taste" skill (both essentially unused in the evidence) |
| 2 | **Design-language check** | `obsidian` + repo-root `DESIGN.md` / `PRODUCT.md` | Pull the pinned house design language (these files are `impeccable`'s own `teach.md` output). **If the repo has neither:** run impeccable's teach flow once to generate them, commit alongside the registry, note it in the ledger |
| 3 | **Audit (no code)** | `impeccable`, sometimes + `web-design-guidelines` | The audit needs the app **live**: stand up the dev server and get test credentials from the user NOW, recording both in the ledger's §Verify Recipe. Scored via `impeccable/reference/heuristics-scoring.md` — Nielsen's 10 heuristics × 0–4 = /40. **The score is the baseline the redesign must beat**, re-scored at the acceptance round (a real observed acceptance: 36/40). Re-run the audit any time a build gets rejected at craft level. Also produce the **feature-parity matrix** here (one Explore: every capability of the old surface × status in the new), stored in `docs/<module>-redesign/` — Phase 8's removed-behavior audit checks the final diff against it. `impeccable` already covers onboarding, UX copy, layout, spacing, interactive states, delight, and performance internally via its `reference/*.md` — don't build separate steps; invoke it and let it route. Backend needs discovered here → see **Backend Prereqs** below |
| 3.5 | **Propose & lock** | `artifact-design` | Present the proposed redesign direction per surface as rendered artifacts — IA, layout, states, key copy. The user's approval of the artifact IS the pre-code lock (hard gate #1). Log the locked spec in the ledger's §IA SIGNED OFF, per surface |
| 4 | **Plan** | `superpowers:writing-plans` | Turn the locked design into a task-by-task implementation plan, written to `docs/<module>-redesign/<surface>-plan.md` in the worktree and committed. Plans are written only against a locked design |
| 5 | **Build** | `interface-design` (loaded by the parent), executed via `superpowers:subagent-driven-development` | **Session scope = one surface** (a tab, a wizard, a header) — never "the module" in one session; that's how every real module was actually built. Strict per-task loop: Implement Task N → Review Task N (spec + quality) → Fix → Re-review, fanned to `general-purpose` subagents. In a round-wide rebuild, batch tightly-related surfaces in pairs per parallel subagent (e.g. "SurveysTab + OverviewTab"), keeping Review as its own dispatch. **Each build-subagent prompt carries:** the plan task, the relevant §IA SIGNED OFF spec section, the House Rules block, and the registry's relevant entries — a subagent that can't see the registry parallel-invents with full confidence. Registry check before any new component: found → adapt per its notes (never literal-copy); do-NOT-copy list → use the named replacement; absent → one Explore confirm, then build. **After a parallel multi-surface rebuild:** one hygiene subagent to dedupe/consolidate the helpers the parallel builders just duplicated, *before* the round's verify — parallel building creates duplicates by construction |
| 6 | **Motion** | `emil-design-eng` (build/direct), `apple-design` as the standing principles reference (springs, interruptibility, gesture correctness — for any gesture-heavy or mobile surface, not just Flutter), `animation-vocabulary` to name an effect precisely when speccing it | Micro-interaction pass. Motion built or changed this round **MUST** be gated at Phase 8 by `review-animations` (see below). If the module's motion needs a whole-codebase debt audit (not just this round's diff), run `improve-animations` — read-only, produces prioritized plans |
| 7 | **Live verify + instrument** | Per platform profile (below). Web: `playwright` + raw browser calls + **Chrome DevTools MCP** trace (LCP/INP/CLS vs the ledger's budget) + `npx react-scan@latest <url>` + axe scan. Flutter: golden tests, `integration_test`, `--profile` overlay | **The highest-volume step in every real session** — real login, real viewport, real screenshots, pixel checks. The instrumentation half is MANDATORY: untraced = unmeasured = unverified. **Mock discipline:** if reaching a state needs injected mock data, verify → **revert every mock** → `git status` residue check → then commit. **Shared-component rule:** touched a component other modules consume (the registry's Used-by column tells you) → live spot-check each consumer module at the breakpoint matrix before calling it done |
| 8 | **Final gate (parallel)** | `impeccable` ×2 + `web-design-guidelines` + `review-animations` (if motion touched) + `code-review --high` + `agent-skills:code-reviewer` | Runs on **acceptance-candidate rounds only** — interim rounds end at Phase 7. Dimensions graded separately, never folded: **design-craft** (two parallel `general-purpose` subagents, each given the live URL/screenshots and impeccable's critique flow, no shared context), **guidelines-compliance** (`web-design-guidelines` against the FINAL code — mandatory for web), **motion-craft** (`review-animations` — dedicated strict block/approve gate against 10 non-negotiable standards; **required for any round that added or changed animation** — it's `disable-model-invocation`, so it NEVER runs unless named here; skip only on a round with no motion change), **code-quality** (`code-review --high`, 8 angles incl. removed-behavior checked against the feature-parity matrix; plus a fresh context-free `code-reviewer` pre-merge pass) |
| 9 | **Ship** | `superpowers:finishing-a-development-branch` | Merge/PR/cleanup — through the project's real merge owner (a named human gatekeeper). **Post-merge (optional but observed):** a fresh code-review + design pass on the merged diff *before human reviewers read it*, fixes landing on `fix/<module>-post-merge-<topic>` |

## Rounds — how the pipeline actually loops

- **The first full pass through phases 3–8 is Round 1** — log it in the ledger before any feedback exists. Subsequent rounds open with the user's verbatim feedback.
- **Interim rounds end at Phase 7** (live-verified, honestly statused). The full Phase-8 gate runs only on a round you believe is the acceptance round — it's expensive by design.
- A craft-level rejection ("not top 1% at all") reopens the Phase-3 audit, not just the build. Real modules took 2–8 rounds (Reviews ran 8).
- **A dogfood round** (observed as "Round 3: dogfood + polish") = walk every workflow end-to-end as the locked persona, at realistic data scale, harvesting an itemized fix list before polishing. Rounds can also carry a **rule change** — a House-Rules amendment logged mid-project in the ledger.
- **Round close updates the registry, every time:** new reusables registered (an unregistered reusable is the seed of the next duplicate), code-truth gotchas dated, near-duplicates logged as extraction candidates (3+ call sites → extract to canonical). Tooling gotchas go in the ledger's §Verify Recipe instead — the registry is about the code, not our tools.

## Backend prereqs (when the redesign needs the backend)

What the evidence actually shows — sequenced by *contract*, not by build order:

1. **Classify early:** Phase 1's backend capability check marks each surface FE-only or MIXED in §BACKEND SCOPE.
2. **Lock the contract in Phase 3** — endpoint shape, fields, semantics — as part of the audit/spec work. The API is otherwise frozen (house rule).
3. **FE may build against the locked contract with mocks while the endpoint is pending** — real sessions did exactly this. The endpoint MUST exist before Phase 7 live-verify: unverifiable = not done.
4. **Own worktree, never inline:** backend work happens in `../<backend-repo>-<thing>` on `feat/<module>-<thing>` (or `fix/...`). Backend commits are **user-asked, never automatic**.
5. **Size split:** a small prereq (an endpoint, a field) is built directly. A large one (new data model, vendor integration, money/legal) hands off to a full `feature-design-pipeline` run as its own workstream — this pipeline resumes when it ships.

## Design principles (apply throughout, not a phase)

These are the user's own recurring standing directives, verified verbatim across sessions — not inferred:

- **User-first, restated every time, not assumed remembered.** "Always think user first... top 1% design, code, quality, & experience." Treat a vague "make it better" as insufficient — the bar gets re-stated per session because it's easy to drift from.
- **Reuse existing patterns, never blindly.** "Don't copy blindly. Think & brainstorm — pick only the best things from the references." When adapting an internal precedent (e.g. Rooms' header for a new module) or an external reference (via Mobbin), adapt the *underlying idea*, not the literal implementation. "Cohesion is the north star." The component registry is this principle made cheap: it records not just what exists but *when not to use it* and how past modules adapted it — reuse with judgment, indexed.
- **A house-rules block, carried into every session.** Concrete, non-negotiable constraints — the observed set: don't hardcode colors/hex values (use the shared token/color hook), keep the API contract frozen unless a prereq is explicitly scoped, `tsc --noEmit` = 0 (web) / `flutter analyze` = 0 (Flutter) before anything counts as done, ask before committing but checkpoint-ask along the way, never delete without confirming.
- **Parallel-work boundaries.** When multiple modules are being redesigned concurrently (separate worktrees), name the no-touch zones explicitly (e.g. never touch the shared Home/Dashboard components) so one module's redesign doesn't collide with another's.
- **Persona-grounded constraints, locked as decisions — per module.** A mobile-first, low-literacy, spotty-connectivity user isn't re-argued every round — it's locked once in the ledger and referenced as "per prior locked decisions." But personas belong to the module's actual users: don't import another module's persona through playbook inheritance (Food's cleaning-staff bar doesn't transfer to a manager-facing surface). Lock this module's persona fresh, in its own ledger.
- **Self-certify before proceeding.** "We may proceed, only if you're satisfied with your plan & approach — 100% sure." Don't move from plan to build on a hedge.
- **Quote rejections verbatim, carry them forward.** A real rejection ("the runner ui is not top 1% at all") gets preserved as a citable record in the ledger, not paraphrased into something softer — precision here is what prevents relitigating the same critique.

## Platform profiles — same pipeline, different tools per phase

Pick the profile before Phase 4, record it in the ledger:

- **Existing web (any repo):** the incumbent UI stack is the frozen constraint — build within it, never migrate mid-redesign. (In rentok-manager-web that means Chakra 2.5 + framer-motion.) Verify: playwright + Chrome DevTools MCP + react-scan + axe. Gate adds `web-design-guidelines`.
- **Flutter (e.g. RentOk Manager App):** Build: the app's existing widget/theme system — same reuse-don't-parallel-invent rule. Verify: golden tests for visual regression, `integration_test` for flows, DevTools performance overlay + timeline in `--profile` mode (jank = dropped frames past 16ms), `flutter analyze` = 0. Gate: `impeccable` and `code-review` apply unchanged; `web-design-guidelines` does not — use `apple-design` (gestures/motion/reduced-motion sections) + Material guidance as the compliance lens.
- **Greenfield (no legacy constraints):** default the stack to **shadcn/ui + Tailwind + Radix** and wire the registry MCPs (shadcn MCP, optionally 21st.dev Magic) from day one — the ecosystem AI tooling has standardized on. `frontend-design` (Anthropic) sets aesthetic direction before `interface-design` builds. Everything else applies unchanged.

## Red flags — STOP, you're about to break the pipeline

| Thought | Reality |
|---|---|
| "The diff looks right, I'll report it done" | Done = live-verified. Real login, real viewport, real screenshot — then it's done. |
| "This module is basically Food/Reviews, I'll apply that playbook" | Inheritance is user-triggered only. If the user didn't say "do the same as X", don't. |
| "It needs one small backend tweak, I'll do it inline" | Backend work lives in its own worktree on a `feat/`/`fix/` branch, against a contract locked in Phase 3. Never inline in the FE worktree. |
| "The build was rejected but the audit already ran" | A craft-level rejection reopens the audit. Re-run `impeccable`, don't patch blind. |
| "I'll paraphrase the user's feedback in the ledger" | Quote it verbatim. Paraphrase is how the same critique gets relitigated next round. |
| "The design is good, I'll start building and confirm later" | Lock with the user BEFORE code — a rendered artifact they approved, not a plan they nodded at. |
| "This new surface needs outside inspiration, let me browse" | Check internal precedent first. Mobbin only when there genuinely is none. |
| "tsc has a couple of pre-existing errors, close enough" | `tsc --noEmit` = 0 (web) / `flutter analyze` = 0 (Flutter) is the bar for "counts as done." |
| "The screenshots look great, skip the perf trace" | Instrumentation is part of Phase 7, not garnish. Untraced = unmeasured = unverified. |
| "Verified it with the mock data still in" | Revert mocks → `git status` residue check → then commit. A mock in a commit is a shipped lie. |
| "Guidelines audit ran early, no need at the gate" | `web-design-guidelines` runs at Phase 8 against the FINAL code — early audits don't cover what was built after them. |
| "Built the animations, they feel fine, moving to ship" | Motion this round is gated by `review-animations` at Phase 8. It's `disable-model-invocation` — if you don't name it, no motion gate runs at all, and "feels fine" isn't the 10-standard bar. |
| "I'll just build a quick version of this card/table/header" | Registry first. A quick parallel version of an existing component is the most common slop — and it's how the codebase got fragmented tokens in the first place. |
| "The registry says X is canonical, straight to build" | Verify the path/component still matches before relying on it — registries rot, and stale grounding is worse than none. |
| "I built a nice reusable component, moving on" | Register it at round close or it's the seed of the next duplicate. Unregistered = invisible = recreated. |
| "It's a shared component but my module looks fine" | Spot-check every consumer module (registry's Used-by column) before "done." Sibling regressions are still regressions. |

## Known gaps (real, not yet covered — add explicitly if the module needs them)

1. **Field performance data.** Phase 7's Chrome DevTools trace gives *lab* numbers (closed the old judged-not-measured gap). Still missing: *field* data — real-user Web Vitals from production (CleverTap/RUM). Lab numbers prove the redesign is fast on your machine; field numbers prove it's fast for a manager on a cheap phone in a low-signal area. Add a ledger "Success Metrics" baseline + checkpoint when the module ships.
2. **Guided tours / coachmark UI patterns aren't covered.** `impeccable`'s `onboard.md` covers onboarding *flow strategy* (time-to-first-value), not the specific spotlight/coachmark tour widget. If the module needs a literal product tour, design it explicitly — there's no existing reference for it.
3. **No Flutter design/token skill exists — anywhere.** The Flutter profile covers verification and the compliance lens, but no dedicated Flutter design skill exists in any ecosystem (independently confirmed by two research passes). Build thin and custom if/when the Flutter app gets a redesign round.

## Persistence

At the end of each session (or any heavy context boundary):
1. **Redesign ledger** — updated with the round's decisions, verbatim feedback, commit hashes, and session lineage.
2. **Repo docs** — specs/plans committed in `docs/<module>-redesign/`; registry updated at round close.
3. **mem0** — the same checkpoint, stored verbatim, for cross-session recall.
4. **Git** — commit only what's been live-verified; leave anything unverified in the working tree, unstaged.

Then hand the user a copy-paste resume prompt (shape in the ledger template): one next step, LAUNCH FROM the main repo path, precise commit-status words, verbatim rejections.

## Pointers

- `PLAYBOOK.md` — the human-readable, worked-example version of this pipeline, with the evidence behind each phase.
- `references/redesign-ledger-template.md` — the ledger structure, section vocabulary, and resume-prompt shape.
- `references/component-registry-template.md` — the per-repo `COMPONENT-REGISTRY.md` structure: canonical components, do-NOT-copy list, conventions, dated gotchas.
