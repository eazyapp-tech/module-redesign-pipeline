---
name: module-redesign-pipeline
description: >-
  Use when redesigning an EXISTING module, screen, or section to a "top 1% / world-class"
  bar — visual craft, IA, motion, and UX-writing overhaul with functionality unchanged.
  Trigger on "redesign this module", "make X top 1%", "complete design overhaul",
  "audit and rebuild this screen", "this looks generic/dated, fix it", or any resumed
  "continue the X redesign" session. NOT for a feature that doesn't exist yet — that is
  feature-design-pipeline's job.
---

# Module Redesign Pipeline

Turn "this module looks generic / dated / not top 1%" into a shipped, live-verified redesign — grounded in the module's real code, benchmarked against real reference products, gated by a scored audit, and never accepted on a claim alone. This is the recipe mined from 66+ real sessions across the Reviews, Food/FoodV2, Tasks, and Change Room redesigns — every phase below is what was actually invoked, not a theoretical pipeline.

This skill **orchestrates other skills**, the same way `feature-design-pipeline` does — it doesn't replace `impeccable`, `interface-design`, or `emil-design-eng`, it invokes them in the right order with the right gates in between.

## What this is / isn't

- **Is:** the path from "this existing module is bad" to a merged, live-verified redesign — audit → build → motion → verify → dual gate → ship. Owns implementation, not just docs.
- **Isn't:** `feature-design-pipeline` (a NEW feature/backend spec that doesn't exist yet — that pipeline stops at a design doc and hands off; if the module doesn't exist yet, use that one, not this). Isn't a bug fix. Isn't a rewrite of business logic — if the redesign genuinely requires a data-model or API change, that change is scoped as its own narrow backend prereq (see Phase 3), not folded into this pipeline's business as usual.

## The one hard gate

**Lock the design with the user before any code, and don't claim "done" without live proof.** Two separate checkpoints, not one:
1. Pre-code: the design must be locked with the user — "the user is design-exacting." No implementation starts on an un-locked design.
2. Pre-"done": nothing is accepted as finished on a claim. It gets verified live (real login, real viewport, real screenshot) before it's reported complete.

## Scaffolding (persistent, not a phase)

- **A per-module redesign ledger** — `project_<module>-redesign.md`, read **in full** (not just latest entries) at the start of every resumed session. See `references/redesign-ledger-template.md` for the structure (Decisions Locked, Round N Feedback, Session Lineage, Adopted Playbooks, House Rules, Parallel-work boundaries).
- **One git worktree per module** (e.g. `rentok-manager-web-food`), with a paired backend worktree spun up only when a genuine backend prereq exists.
- **Cross-module playbook inheritance — always user-triggered, never assumed.** A new module doesn't start from zero, but the reuse only happens when the user explicitly says "recall how we did X, do the same for Y." Don't auto-apply a prior module's playbook without that prompt.

## The pipeline

| # | Phase | Skill / tool | Notes |
|---|---|---|---|
| 0 | **Frame** | Invoke `feature-design-pipeline` itself for a brand-new module redesign (this is what every real module kickoff did — Reviews, Tasks, Change Room); `superpowers:brainstorming` alone for a new screen/tab inside an in-flight module | Restate the ask, expand it, state it back for alignment — before touching anything. Only its framing phase runs here: its doc stack (`brief`, `pre-mortem`, `domain-modeling`, `doc-handoff-review`) stays out, because the module already exists and the Phase-3 audit is the spec |
| 1 | **Ground** | `Explore` subagents, 2–5 in parallel | Map the module end-to-end, characterize the house design system, trace the real data shapes. Never design against a guess |
| 1.5 | **Reference** | **Mobbin MCP** (`mcp__mobbin__search_flows` / `search_screens` / `search_sections`) | Pull real screens from named best-in-class apps — only for surfaces with no internal precedent (a new onboarding flow, an analytics dashboard). Pick the *best ideas* from references, never copy wholesale — see Design Principles below. This is the actual reference mechanism; it is not Figma and not any catalogued "taste" skill (both are essentially unused in this pipeline) |
| 2 | **Design-language check** | `obsidian` + repo-root `DESIGN.md` / `PRODUCT.md` | Pull the pinned house design language (these files are `impeccable`'s own `teach.md` output — read them, don't reinvent them) |
| 3 | **Audit (no code)** | `impeccable`, sometimes + `web-design-guidelines` | Scored gate via `impeccable/reference/heuristics-scoring.md` — Nielsen's 10 heuristics × 0–4 = /40 (a real observed score: 36/40). Re-run any time a build gets rejected. `impeccable` already covers onboarding flows (`onboard.md`), UX copy (`ux-writing.md`), layout/visual-weight (`layout.md`), spacing/nesting (`spatial-design.md`), interactive states/tooltips (`interaction-design.md`), delight (`delight.md`), and performance (`optimize.md`) internally — don't build separate steps for these, invoke `impeccable` and let it route. If a genuine backend data/logic change is needed to support the redesign, scope it here as an isolated prereq — build and commit it first, in its own worktree, before frontend work starts against it. A *small* prereq (an endpoint, a field) is built directly; a *large* one (new data model, vendor integration, money/legal surface) hands off to a full `feature-design-pipeline` run as its own workstream, and this pipeline resumes when that ships. Otherwise the API contract stays frozen |
| 4 | **Plan** | `superpowers:writing-plans` | Turn the locked design into a task-by-task implementation plan |
| 5 | **Build** | `interface-design`, executed via `superpowers:subagent-driven-development` | Strict per-task loop: Implement Task N → Review Task N (spec + quality) → Fix → Re-review, fanned to `general-purpose` subagents. Reuse existing components/services — never invent a parallel one for something the codebase already has |
| 6 | **Motion** | `emil-design-eng` | Micro-interaction pass. `apple-design`, `animation-vocabulary`, `review-animations`, `improve-animations` are available as deeper motion references/audits but were not part of the sessions this pipeline is verified against — reach for them when the motion needs go beyond `emil-design-eng`'s coverage |
| 7 | **Live verify** | `playwright` skill + raw browser tool calls | **The highest-volume step in every real session** — real login (test credentials), real mobile viewport, real screenshots, pixel-level checks (e.g. a divider that must only render between inactive tabs). Nothing is "done" without this |
| 8 | **Final gate (dual, parallel)** | `impeccable` (2 independent critique assessments) + `code-review --high` (8 angles: line-by-line, removed-behavior, cross-file, reuse, simplification, efficiency, altitude, CLAUDE.md conventions) + `agent-skills:code-reviewer` fresh pre-merge pass | Design-craft and code-quality are graded **separately**, not folded into one pass |
| 9 | **Ship** | `finishing-a-development-branch` | Merge/PR/cleanup — route through the project's real merge owner (a named human gatekeeper), not just these automated gates |

**The pipeline loops.** Phases 3–8 repeat as **rounds** driven by user feedback — real modules took 2–8 rounds (Reviews ran 8). A round opens with the user's verbatim feedback logged in the ledger, re-runs the audit if the rejection was craft-level, and closes with live verification. Ship (Phase 9) only happens after a round ends with acceptance, not after the first pass.

## Design principles (apply throughout, not a phase)

These are the user's own recurring standing directives, verified verbatim across sessions — not inferred:

- **User-first, restated every time, not assumed remembered.** "Always think user first... top 1% design, code, quality, & experience." Treat a vague "make it better" as insufficient — the bar gets re-stated per session because it's easy to drift from.
- **Reuse existing patterns, never blindly.** "Don't copy blindly. Think & brainstorm — pick only the best things from the references." When adapting an internal precedent (e.g. Rooms' header for a new module) or an external reference (via Mobbin), adapt the *underlying idea*, not the literal implementation. "Cohesion is the north star."
- **A house-rules block, carried into every session.** Concrete, non-negotiable constraints — the observed set: don't hardcode colors/hex values (use the shared token/color hook), keep the API contract frozen unless Phase 3 explicitly scopes a prereq, `tsc --noEmit` must be clean before anything counts as done, ask before committing but checkpoint-ask along the way, never delete without confirming.
- **Parallel-work boundaries.** When multiple modules are being redesigned concurrently (separate worktrees), name the no-touch zones explicitly (e.g. never touch the shared Home/Dashboard components) so one module's redesign doesn't collide with another's.
- **Persona-grounded constraints, locked as decisions — per module.** A mobile-first, low-literacy, spotty-connectivity user isn't re-argued every round — it's locked once in the ledger and referenced as "per prior locked decisions." But personas belong to the module's actual users: don't import another module's persona through playbook inheritance (Food's cleaning-staff bar doesn't transfer to a manager-facing surface). Lock this module's persona fresh, in its own ledger.
- **Self-certify before proceeding.** "We may proceed, only if you're satisfied with your plan & approach — 100% sure." Don't move from plan to build on a hedge.
- **Quote rejections verbatim, carry them forward.** A real rejection ("the runner ui is not top 1% at all") gets preserved as a citable record in the ledger, not paraphrased into something softer — precision here is what prevents relitigating the same critique.

## Red flags — STOP, you're about to break the pipeline

| Thought | Reality |
|---|---|
| "The diff looks right, I'll report it done" | Done = live-verified. Real login, real viewport, real screenshot — then it's done. |
| "This module is basically Food/Reviews, I'll apply that playbook" | Inheritance is user-triggered only. If the user didn't say "do the same as X", don't. |
| "It needs one small backend tweak, I'll do it inline" | Backend changes are isolated prereqs — own worktree, committed first. Never inline. |
| "The build was rejected but the audit already ran" | A craft-level rejection reopens the audit. Re-run `impeccable`, don't patch blind. |
| "I'll paraphrase the user's feedback in the ledger" | Quote it verbatim. Paraphrase is how the same critique gets relitigated next round. |
| "The design is good, I'll start building and confirm later" | Lock with the user BEFORE code. No exceptions — the user is design-exacting. |
| "This new surface needs outside inspiration, let me browse" | Check internal precedent first. Mobbin only when there genuinely is none. |
| "tsc has a couple of pre-existing errors, close enough" | `tsc --noEmit` = 0 is the bar for "counts as done." |

## Known gaps (real, not yet covered — add explicitly if the module needs them)

1. **Performance is judged, not measured.** `impeccable`'s `optimize.md` step is a qualitative/code-level assessment. No session in the verified set ever ran an actual measurement tool (Lighthouse, bundle-analyzer, web-vitals). If the module has a real performance concern, add an instrumented pass — don't assume the audit step covers it.
2. **Guided tours / coachmark UI patterns aren't covered.** `impeccable`'s `onboard.md` covers onboarding *flow strategy* (time-to-first-value), not the specific spotlight/coachmark tour widget. If the module needs a literal product tour, design it explicitly — there's no existing reference for it.

## Persistence

At the end of each session (or any heavy context boundary):
1. **Redesign ledger** — `project_<module>-redesign.md`, updated with the round's decisions, feedback, and session lineage. See `references/redesign-ledger-template.md`.
2. **mem0** — the same checkpoint, stored verbatim, for cross-session recall.
3. **Git** — commit only what's been live-verified; leave anything unverified in the working tree, unstaged.

Then hand the user a copy-paste resume prompt that names the exact next phase.

## Pointers

- `PLAYBOOK.md` — the human-readable, worked-example version of this pipeline, with the evidence behind each phase.
- `references/redesign-ledger-template.md` — the `project_<module>-redesign.md` structure to copy for a new module.
