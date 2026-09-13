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

> Before showing him anything, run the checklist in `~/agent-config/bars/manager-web-screen or manager-app-screen or marketplace-page, whichever the repo is.md` and name that file in the Checked line.

> Before anything else, read the operator's own lesson log for this skill if one exists (`~/.claude/docs/working-records/`): the corrections this stakeholder has already given for this kind of work. It is private to the operator and deliberately not in this repo.

# Module Redesign Pipeline

Turn "this module looks generic / dated / not top 1%" into a shipped, live-verified redesign — grounded in the module's real code, benchmarked against real reference products where no internal precedent exists, gated by a scored audit and real performance traces, and never accepted on a claim alone. This is the recipe mined from 66+ real sessions across the Reviews, Food/FoodV2, Tasks, and Change Room redesigns — every phase below is what was actually invoked, not a theoretical pipeline.

**Read `learnings.md` in this folder before starting any round. Append to it whenever a correction lands.** Lookup files, keyed by question not date: the project's **working record**, if one exists, at `~/.claude/docs/working-records/` (how rounds actually succeed with this particular stakeholder, built by reading their own turns across a whole project: read it before the first round and after any rejection; it is private to the operator and deliberately not in this repo), `references/gates.md` (rules), `references/patterns.md` (cross-repo patterns), `references/traps.md` (tooling), and in the target repo `docs/design/COMPONENT-REGISTRY.md` + `docs/design/PATTERNS.md`. **Gate 4 (Harvest) fires on every `git commit`:** five questions (the fifth is the working note), three tests, `scripts/registry_rot.py`. See `references/harvest.md`. It carries the corrections that produced the rules below, plus verified repo truths worth not re-deriving.

This skill **orchestrates other skills** — it doesn't replace `impeccable`, `interface-design`, or `emil-design-eng`, it invokes them in the right order with the right gates in between. (Skill names from the superpowers suite are written with the `superpowers:` prefix; depending on install they may resolve unprefixed — same skills.)

## What this is / isn't

- **Is:** the path from "this existing module is bad" to a merged, live-verified redesign — audit → lock → build → motion → verify → final gate → ship. Owns implementation, not just docs.
- **Isn't:** `feature-design-pipeline` (a NEW feature/backend spec that doesn't exist yet — that pipeline stops at a design doc and hands off; if the module doesn't exist yet, use that one, not this). Isn't a bug fix. Isn't a rewrite of business logic — backend changes happen only as scoped prereqs (see Backend Prereqs below).

## The Designer's Gates (read `references/gates.md` first; hooks enforce them)

Three checks tied to a moment in the work, fired by global hooks in `~/.claude/settings.json` whether or not anyone remembered them. They apply to **any UI surface in any project**, including new surfaces built through `feature-design-pipeline`, which is why the triggers are global and this file is their home.

| Gate | Fires when | Passes when |
|---|---|---|
| **1 · Surface Ready** | a new component file is created | the seven answers exist and the stakeholder has seen them: what it IS, the question she came with, the internal precedent, two outside references, two rendered directions, the pick and why, what the spec gets wrong |
| **2 · Done Probe** | `git commit` with a UI component staged | `scripts/run_probe.py` at 375 and an explicit 1440 passes (one centre per control row, sticky x unchanged and no sticky cell shorter than a sibling, popovers portaled with a gutter, no 0px icons, flex peers within 2px, no sideways scroll, first-row y judged, nothing opened by a programmatic focus) and its lines are in the commit message |
| **3 · Shared Primitive** | editing tokens, primitives, a shared header, theme | consumers grepped first, one concern per function, the probe re-run on a consumer after |

**Set up the hooks once per machine — `references/hooks-setup.md`** — or this is rules again, not gates: a skill folder cannot wire `~/.claude/settings.json` on its own.

`references/gates.md` also holds the working contract with the stakeholder (lead, expand before acting, their suggestion is an input, 100% sure or say which answer is missing), the taste bar, the code bar, and the environment traps. Written for the humans on the team as much as for the agent: the agent is the designer, the humans guide and decide.

**Model note.** This skill will mostly run on Sonnet, sometimes Opus, rarely Fable. Nothing in the gates depends on the model remembering: the hooks inject the check at the moment, the probe is a script that prints numbers, and every pass condition is a number with a threshold. If a gate fires and the answer is "not yet", say which item is missing; do not proceed on a feeling.

## The one hard gate

**Lock the design with the user before any code, and don't claim "done" without live proof.** Two separate checkpoints, not one:
1. **Pre-code (Phase 3.5):** present the proposed design as a **rendered artifact** (`artifact-design`), per surface — not prose. The user approving *that artifact* is the lock. No implementation starts on an un-locked design — "the user is design-exacting."
2. **Pre-"done" (Phase 7):** nothing is accepted as finished on a claim. It gets verified live (real login, real viewport, real screenshot) before it's reported complete.

## The expansion rule (feedback is a sample, never the scope)

**This is the second hard gate, and it is the one this pipeline failed on most often.** The recurring failure is not bad craft. It is treating a stakeholder's message as the work order. Every pointer you get is one visible instance of a pattern that is almost always present in several other places. Fixing only what was pointed at guarantees another round, and the next round costs their trust, not just time. Their words: "I just don't understand why you take everything I say and limit yourself to that."

**Run these five steps on every piece of feedback, before any code. No exceptions for "small" or "obvious" items.**

1. **Name the pattern.** Ask what class of mistake this is an instance of. Not "the chip overlaps" but "there is no spacing rule for adjacent filled states." Not "the property list is flat" but "I ignored a domain model the app already encodes."
2. **Sweep for siblings.** Walk every other surface in the module for that same class. One reported instance usually means three to six unreported ones. Report the count you found, not just the fix.
3. **Find the internal precedent.** Before designing anything, find the screen in this repo that already solved it. Registry first, then the app. Adapt the idea, never paste the implementation.
4. **Walk the workflow, not the screen.** Replay the user's real job end to end at real data scale. Missing capability is invisible to a screen audit and it is what the stakeholder actually feels. Ask: what will she do twenty times that she should do once?
5. **Come back expanded.** Present the pattern, every instance, the precedent, the capability gaps, and your recommendation. You are the lead. A list that matches the feedback item for item is proof you only did step 0.

**The stakeholder's suggestion is an input, not an order.** They can be wrong, and they have said so out loud: "never blindly copy or follow what i say... you can push back always." Cross-check every suggestion against the codebase and the references before adopting it. Disagree once, with reasons and a pick. When you do adopt it, adapt it: reuse the model behind the suggestion, not necessarily the component it named.

**The domain test.** Before designing any list, picker, or grouping, ask what the real-world unit is. People do not think in flat lists. Properties cluster by area and by custom group. Staff cover clusters, not single addresses. Categories contain subtypes. If your UI's unit is smaller than the user's mental unit, you have handed them arithmetic.

**The identity test.** Anything that names a person or a place carries its face. Avatar for people, logo for properties, in table cells, modal rows, confirmations, and toasts. One `PersonChip` and one `PropertyIdentity` per repo, or they drift into four near-copies.

**The bar is the best screen in this app, not the module you are replacing.** Name the reference screens in the ledger at Phase 0 and measure against them at Phase 3 and Phase 8. "Better than what was here" is not the bar. "Better than the best thing we have shipped" is.

## Working with the stakeholder (the contract)

Adapted from `feature-map`'s contract, which was learned the hard way on a doc that took six versions. The same failures happen in a redesign round, so the same rules apply here.

1. **Gather the whole round before acting on any of it.** He gives input in waves. Starting on point 1 while points 2 to 6 are still arriving is the whack-a-mole failure, and it produces a rebuild per wave. Hold a running inventory, expand every item per the expansion rule, then state the complete picture back in one message.
2. **Framing approval is not a go.** "Yes, that is the right read" authorizes the direction, not the build. The go is on content he has actually seen: the rendered artifact at Phase 3.5.
3. **Verify every checkable claim before asserting it.** "X already exists" gets a grep. "The app has no Y" gets a search. Both directions of error have burned real sessions. This applies to *his* claims too, and checking one saved a wrong fix in this module: two properties shared a name, so what looked like a self-copy bug was not one.
4. **Push back once, with reasons and a pick. After a ruling, never re-raise it** unless genuinely new information arrives. Raising a concern is diligence; raising it twice after a ruling is not listening.
5. **His taxonomy wins.** Never merge concepts he keeps separate, never rename his concepts. If his word for something differs from the code's word, his word goes in the UI and the mapping goes in the ledger.
6. **When he reframes your concern instead of trimming his idea, the reframe is usually the answer.** Recognise it, adopt it, move on.
7. **Sort findings with reasons, never as a flat list.** Same four buckets as `feature-map`: **spine** (the module does not make sense without it), **supporting**, **parked** (name the condition that revives it), **cut** (name the reason). A flat list of 30 defects makes him do the prioritising you were hired to do.
8. **Ask only questions whose answers change the work.** One at a time.
9. **Inventory diff before delivering.** Every item he raised is present in the plan or deliberately absent with a reason. Nothing silently dropped between rounds. This is the check that catches the item that quietly disappeared in version 3.

## Living files (the registry, DESIGN.md, the grammar, the LOCKS — all of them)

**Every reference document in this system is a living file.** The component registry, `DESIGN.md`, the house grammar rules, the module's LOCKS, the ledger, and this skill. They record what we know *so far*. They are a floor to build on, never a lid, and never a museum.

- **Read them as the starting position, not the answer.** "The registry has no such component, so we cannot" is the wrong sentence. Build it, then register it.
- **Write back the moment you learn something.** A new reusable, a code-truth gotcha, an adapted pattern, a rule he set mid-round: it lands in the right living file in the same round it was learned, not "later". Unregistered is invisible, and invisible is recreated.
- **When we raise the bar, the file gets raised with it.** If this module's people-cell is better than what the registry describes, the registry entry changes. If he sets a new rule (the drawn artifact wins over LOCKS prose; subtypes are selectable too), it amends LOCKS with a date and a note that it supersedes.
- **Correct them when they are wrong.** A stale registry is worse than none. Verify entries you rely on, and fix what has rotted rather than routing around it.
- **`learnings.md` in this skill folder is the same kind of file.** Read it at the start of every round; append whenever a correction lands.

## Workflow-first, not tool-first (where the tool ends, the workflow starts)

> This phrase is already established RentOk design grammar: `feature-map` names "the tool ends where the workflow begins" as a cross-cutting mechanic. Treat it as a house rule, not a new idea.

**The default failure mode of a competent build is a tool.** A tool exposes a control and stops. A workflow carries the person from what they came to do all the way to the outcome, and tells them where they are the whole way. Almost every "technically correct but it feels thin" verdict is this gap. This principle governs Phase 3 (what you audit for), Phase 3.5 (what you propose), and Phase 5 (what you build). It is not a polish step at the end.

**The three questions, asked of every surface, every state:**

1. **What did she come here to do?** Not "what does this screen show." The screen exists to serve an intent. Write the intent down. If you cannot, the surface has no job.
2. **Where does the tool end?** Find the exact point where the product stops helping and hands her back a result. That point is where the workflow starts and where most designs quit. After the save, after the copy, after the error, after the empty state, after the last item in the list. Something has to be there.
3. **Does it guide, or does it wait?** A screen that waits for her to know what to do is a tool. Suggest the next right step, pre-fill what you can already infer, and put the escape hatch in reach. Never make her hold state in her head or compute a number the product already knows.

**Empathy is concrete, not a mood.** It is these, and they are checkable:

- **No dead ends.** Every terminal state (done, empty, error, no results, nothing selected) offers the next action, in her words. An empty state that only says "nothing here" is a dead end.
- **No lost work.** Anything destructive or hard to reverse gets an undo, offered where the action was confirmed. A confirmation dialog is not an undo, it is a speed bump before the same loss.
- **Consequences in her words, before the click.** "Replacing overwrites who currently gets these complaints" beats a button labelled Replace. Say what happens to *her* thing, not what the system does.
- **Never make her repeat herself.** If she will do it more than about five times, it needs a bulk path. Count the taps for the real data scale, not the demo scale.
- **Say where she is and what is true right now.** Live or not live, saved or not saved, how many of how many. Status is not decoration, it is the thing that lets her trust the screen.
- **Errors name the fix, not the failure.** And they leave everything else she did intact.

**The workflow test, run before you call any surface done:** narrate her whole job out loud from intent to outcome, at real data scale, including the state she lands in afterwards. Every sentence where she has to leave, guess, count, remember, or start over is a finding. This is the test that catches what a defect audit structurally cannot.

## Phase 0 setup (first session in a module — do these before the pipeline)

1. **Preflight the tools.** Check Mobbin MCP and Chrome DevTools MCP are connected (`mcp__mobbin__*`, `chrome-devtools`). Fallbacks if absent — log the substitution in the ledger: web reference search instead of Mobbin; playwright tracing + Lighthouse CLI instead of the DevTools trace.
1.5. **Name the reference screens, in the ledger, before anything else.** Ask the user which shipped screens in this app represent the bar, and record them by name and route. Every audit and every gate measures against those, not against the module being replaced. (In `rentok-manager-web` the standing set is: the **homescreen** — global search bar and its modal, scroll and expand/collapse behaviour, popovers, the property selector; **Timeline / Bed Availability** — row rhythm, sticky columns, filter chips; **Rooms** — list density and sticky header.)
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
| 1.5 | **Reference** | **Mobbin MCP** (`search_flows` / `search_screens` / `search_sections`) | Only for surfaces with no internal precedent (a new onboarding flow, an analytics dashboard). Pick the *best ideas*, never copy wholesale. For marketing and brand surfaces, where Mobbin is thin, the scroll and motion showcases in `references/motion-and-reference-libraries.md` (Lenis templates, GSAP showcase) fill in. This is the actual reference mechanism — not Figma, not any catalogued "taste" skill (both essentially unused in the evidence) |
| 2 | **Design-language check** | `obsidian` + repo-root `DESIGN.md` / `PRODUCT.md` | Pull house language as a **floor, not a lid** (see **Living house language**). Tokens/patterns from Home V2 / latest modules — do not paste an existing screen. **If the repo has neither file:** run impeccable's teach flow once, commit alongside the registry, note it in the ledger |
| 3 | **Audit (no code)** | `impeccable`, sometimes + `web-design-guidelines` | The audit needs the app **live**: stand up the dev server and get test credentials from the user NOW, recording both in the ledger's §Verify Recipe. Scored via `impeccable/reference/heuristics-scoring.md` — Nielsen's 10 heuristics × 0–4 = /40. **The score is the baseline the redesign must beat**, re-scored at the acceptance round (a real observed acceptance: 36/40). Re-run the audit any time a build gets rejected at craft level. **Two things the audit must contain beyond defects, or it is only half an audit** (see `references/expansion-rule-worked-example.md`): a **workflow walk** at real data scale that names what the persona repeats and what she cannot do at all (capability gaps are invisible to a screen audit and are what a stakeholder actually feels), and **state-combination measurement** — alignment, overflow, truncation and sticky checks run with the toggles ON together (select mode on *and* a group expanded *and* a filter applied *and* a long name), plus at the width where a flexible column hits its `minmax` floor. A grid that aligns in the default state proves nothing. Also produce the **feature-parity matrix** here (one Explore: every capability of the old surface × status in the new), stored in `docs/<module>-redesign/` — Phase 8's removed-behavior audit checks the final diff against it. `impeccable` already covers onboarding, UX copy, layout, spacing, interactive states, delight, and performance internally via its `reference/*.md` — don't build separate steps; invoke it and let it route. Backend needs discovered here → see **Backend Prereqs** below |
| 3.5 | **Propose & lock** | `artifact-design` (web) / the `design` canvas skill with phone-sized artboards (Flutter/native) | **Gate 1 runs here, per surface, modals and docks included.** Present the proposed redesign direction per surface as rendered artifacts — IA, layout, states, key copy. Medium follows the platform profile: web HTML artifacts for web, phone-framed mobile comps for Flutter. The user's approval of the artifact IS the pre-code lock (hard gate #1). Log the locked spec in the ledger's §IA SIGNED OFF, per surface |
| 4 | **Plan** | `superpowers:writing-plans` | Turn the locked design into a task-by-task implementation plan, written to `docs/<module>-redesign/<surface>-plan.md` in the worktree and committed. Plans are written only against a locked design |
| 5 | **Build** | `interface-design` (loaded by the parent), executed via `superpowers:subagent-driven-development` | **Session scope = one surface** (a tab, a wizard, a header) — never "the module" in one session; that's how every real module was actually built. Strict per-task loop: Implement Task N → Review Task N (spec + quality) → Fix → Re-review, fanned to `general-purpose` subagents. In a round-wide rebuild, batch tightly-related surfaces in pairs per parallel subagent (e.g. "SurveysTab + OverviewTab"), keeping Review as its own dispatch. **Each build-subagent prompt carries:** the plan task, the relevant §IA SIGNED OFF spec section, the House Rules block, and the registry's relevant entries — a subagent that can't see the registry parallel-invents with full confidence. Registry check before any new component: found → adapt per its notes (never literal-copy); do-NOT-copy list → use the named replacement; absent → one Explore confirm, then build. **After a parallel multi-surface rebuild:** one hygiene subagent to dedupe/consolidate the helpers the parallel builders just duplicated, *before* the round's verify — parallel building creates duplicates by construction |
| 6 | **Motion** | `emil-design-eng` (build/direct), `apple-design` as the standing principles reference (springs, interruptibility, gesture correctness — for any gesture-heavy or mobile surface, not just Flutter), `animation-vocabulary` to name an effect precisely when speccing it; **`references/motion-and-reference-libraries.md` for which library (CSS → framer-motion → GSAP → Lenis, via the ladder), and where shaders and mockups may draw** | Micro-interaction pass. Motion built or changed this round **MUST** be gated at Phase 8 by `review-animations` (see below). If the module's motion needs a whole-codebase debt audit (not just this round's diff), run `improve-animations` — read-only, produces prioritized plans |
| 7 | **Live verify + instrument** | **Gate 2: `scripts/run_probe.py` at 375 and 1440, lines pasted into the commit.** Per platform profile (below). Web: `playwright` + raw browser calls + **Chrome DevTools MCP** trace (LCP/INP/CLS vs the ledger's budget) + `npx react-scan@latest <url>` + axe scan. Flutter: golden tests, `integration_test`, `--profile` overlay | **The highest-volume step in every real session** — real login, real viewport, real screenshots, pixel checks. The instrumentation half is MANDATORY: untraced = unmeasured = unverified. **Mock discipline:** if reaching a state needs injected mock data, verify → **revert every mock** → `git status` residue check → then commit. **Shared-component rule:** touched a component other modules consume (the registry's Used-by column tells you) → live spot-check each consumer module at the breakpoint matrix before calling it done |
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
- **Reuse existing patterns, never blindly.** "Don't copy blindly. Think & brainstorm — pick only the best things from the references." When adapting an internal precedent (e.g. Rooms' header for a new module) or an external reference (via Mobbin), adapt the *underlying idea*, not the literal implementation. "Cohesion is the north star." The component registry is this principle made cheap: it records not just what exists but *when not to use it* and how past modules adapted it — reuse with judgment, indexed. **House language is a floor, not a lid** — see **Living house language**.
- **A house-rules block, carried into every session.** Concrete, non-negotiable constraints — the observed set: don't hardcode colors/hex values (use the shared token/color hook), keep the API contract frozen unless a prereq is explicitly scoped, `tsc --noEmit` = 0 (web) / `flutter analyze` = 0 (Flutter) before anything counts as done, ask before committing but checkpoint-ask along the way, never delete without confirming.
- **Parallel-work boundaries.** When multiple modules are being redesigned concurrently (separate worktrees), name the no-touch zones explicitly (e.g. never touch the shared Home/Dashboard components) so one module's redesign doesn't collide with another's.
- **Persona-grounded constraints, locked as decisions — per module.** A mobile-first, low-literacy, spotty-connectivity user isn't re-argued every round — it's locked once in the ledger and referenced as "per prior locked decisions." But personas belong to the module's actual users: don't import another module's persona through playbook inheritance (Food's cleaning-staff bar doesn't transfer to a manager-facing surface). Lock this module's persona fresh, in its own ledger.
- **Self-certify before proceeding.** "We may proceed, only if you're satisfied with your plan & approach — 100% sure." Don't move from plan to build on a hedge.
- **Quote rejections verbatim, carry them forward.** A real rejection ("the runner ui is not top 1% at all") gets preserved as a citable record in the ledger, not paraphrased into something softer — precision here is what prevents relitigating the same critique.

## Living house language (Phase 2 + 3.5)

**When:** the user says “house language”, Home V2, Tasks, “latest modules”, or “ground it in our design system.”

**How:** start from house tokens and components (cards, headers, empty states, staff rows, sticky footers, plan colours). Then **raise** the shared language — donate a reusable pattern (register it at round close). Existing screens are a starting floor, never a lid, never a museum replica.

**Test:** if the new UI cannot be reused as a pattern, we made a one-off — we did not raise the house.

**Bar:** top 1% always (human, soulful, production). Airbnb / Linear / Stripe = quality of thought, not a look to clone. Materials start from the house; craft must still clear 1%. Get better always.

**Anti-patterns:**
- Blind-copy an existing screen (Tasks empty-start hid this module’s board — failed). House paint ≠ paste that layout.
- Match Home V2 air when this job needs a denser row — don’t smash the job into a marketing card, and don’t hide the job to look airy.
- Clone Stripe/Airbnb typefaces or chrome so it “looks premium.”
- Treat registry/Home V2 as a ceiling: “that component doesn’t exist, so we can’t.”

## Platform profiles — same pipeline, different tools per phase

Pick the profile before Phase 4, record it in the ledger:

- **Existing web (any repo):** the incumbent UI stack is the frozen constraint — build within it, never migrate mid-redesign. (In rentok-manager-web that means Chakra 2.5 + framer-motion.) Verify: playwright + Chrome DevTools MCP + react-scan + axe. Gate adds `web-design-guidelines`.
- **Flutter (e.g. RentOk Manager App):** Build: the app's existing widget/theme system — same reuse-don't-parallel-invent rule. **Propose/lock (Phase 3.5): the `design` canvas skill with phone-sized artboards, NOT `artifact-design`** — a web page does not represent a native screen; lock against phone-framed comps he can edit on the canvas. Verify: golden tests for visual regression, `integration_test` for flows, DevTools performance overlay + timeline in `--profile` mode (jank = dropped frames past 16ms), `flutter analyze` = 0. Gate: `impeccable`, `code-review`, and `review-animations` (motion) apply unchanged; `web-design-guidelines` does not — use `apple-design` (gestures/motion/reduced-motion sections) + Material guidance as the compliance lens. (No Flutter design/token skill exists in any ecosystem — see Known Gaps; build thin and custom if this becomes frequent.)
- **Greenfield (no legacy constraints):** default the **product-app** stack to **shadcn/ui + Tailwind + Radix** and wire the registry MCPs (shadcn MCP, optionally 21st.dev Magic) from day one — the ecosystem AI tooling has standardized on. Two profile differences from the existing-web case, because there's no incumbent to ground against: **Phase 2 GENERATES the design language instead of pulling it** — run `stitch-design-taste` (produces a `DESIGN.md` in the Stitch format, the greenfield-purpose-built generator; `impeccable`'s teach flow is the fallback) and commit it as the pinned baseline. **Phase 1.5 reference is always-on, not conditional** — internal precedent is absent by definition, so pull Mobbin refs, and when Mobbin has no match, generate reference comps with `artifact-design` / `imagegen-frontend-mobile`. `frontend-design` (Anthropic) sets aesthetic direction before `interface-design` builds. **If the greenfield target is a marketing/landing site, not a product app,** the builder swaps: `frontend-design` / `frontend-skill` / `high-end-visual-design` (art-direction-led) instead of `interface-design` (data-UI-led). Everything else in the pipeline applies unchanged.

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
| "The user listed 5 problems, I fixed 5 problems" | You did step 0 of the expansion rule. Each item was a sample. Name the pattern, sweep the module, come back with the count. |
| "They asked for X, so I'm building X" | Their suggestion is an input, not an order. Cross-check it, adapt the model behind it, and say so if you disagree. They invited the pushback. |
| "It's a list of things, I'll render a list" | What is the user's real unit? Area, group, cluster, parent category. A flat list of 47 is arithmetic homework. |
| "The toast confirms it worked" | Does it carry the face of the person or place it names? Identity everywhere, or nowhere. |
| "This is better than what was in this module before" | The bar is the best screen in the app, named in the ledger — not the thing you are replacing. |
| "I measured the grid and columns line up" | In which state? Measure with every toggle on: select mode, expanded children, filters, long names, deep data. Alignment bugs hide in the states you didn't switch on. |
| "I'll copy Tasks empty-start / Home V2 so it looks like the house" | Floor, not lid. Don’t paste another screen if it hides this module’s job. Raise a reusable pattern; register it. |
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
- `learnings.md` — **read at the start of every round, append on every correction.** Dated corrections with the rule each one produced, plus verified repo truths (where grouped property selection already lives, which motion token object is real, which popover family to build against) so no session re-derives them.
- `references/motion-and-reference-libraries.md` — the seven resources the stakeholder named on 7 Sep 2026 (react-spring, GSAP, anime.js, Lenis templates, shaders.com, ls.graphics, promptlibrary.org): which library via the ladder, where to look for scroll and motion references, and where shaders and mockups may draw under the media tiers.
- `references/expansion-rule-worked-example.md` — **read this the first time you get feedback in any round.** The five steps of the expansion rule run against a real round that failed them, plus the state-combination rule for measuring alignment and overflow.
