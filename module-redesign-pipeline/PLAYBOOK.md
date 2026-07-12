# Module Redesign Pipeline — Playbook

The human-readable version of the `module-redesign-pipeline` skill. Worked examples throughout: the RentOk Reviews, Food/FoodV2, Tasks, and Change Room redesigns — 66+ real sessions mined for this, not a theoretical process.

---

## The shape of it

```
Ask → [0] Frame → [1] Ground → [1.5] Reference → [2] Design-lang → [3] Audit → [4] Plan → [5] Build → [6] Motion → [7] Live-verify → [8] Dual gate → [9] Ship
       brainstorming   Explore      Mobbin MCP      obsidian/         impeccable   writing-  interface-   emil-       playwright +    impeccable×2 +   finishing-a-
       or feature-      subagents   (only if no      DESIGN.md         (scored,     plans     design via    design-eng  raw browser     code-review--     dev-branch
       design-pipeline  (parallel)  internal          PRODUCT.md        /40)                  subagent-                calls           high + code-
       Phase 1                     precedent)                                                driven-dev                               reviewer
```

Three ideas make it work, more than any single skill:
1. **Ground before you touch pixels.** Never redesign against a guess of what's there. Map the real module, and only reach outside (Mobbin) when there's genuinely no internal precedent.
2. **The user is the real final gate, not the skills.** `impeccable` and `code-review` catch a lot, but the sessions show the user's own verbatim rejections ("not top 1% at all") are what actually reopen a round. Preserve those quotes; don't soften them into a vague memory.
3. **Nothing is "done" without live proof.** The single highest-volume activity in every real session is browser verification — login, viewport, screenshot, pixel-check. A claim of "done" without that is not done.

---

## Phase 0 — Frame

For a brand-new module redesign, **invoke `feature-design-pipeline` itself** — that's what every real module kickoff did (Reviews, Tasks, Change Room all opened with it). Its job here: restate the ask, expand it, and **state it back to the user for alignment before acting** — verbatim from the sessions: *"current phase: think on the ask, expand/refine it, and state it back to the user for alignment before acting."* But only its framing phase runs — its document stack (`brief`, `pre-mortem`, `domain-modeling`, `grilling`, `doc-handoff-review`) never fired in a single redesign session, because the module already exists and the Phase-3 scored audit serves as the spec. For a new screen or tab inside an already-framed module, a lighter `superpowers:brainstorming` pass is enough.

The two pipelines also compose mid-project: when Phase 3 uncovers a backend prereq too large to build directly (a new data model, a vendor integration, anything touching money/legal), that prereq becomes its own `feature-design-pipeline` workstream — full Track A treatment — and this pipeline resumes once it ships.

Don't skip this because the module already exists — "it exists" is not the same as "the redesign's scope is agreed."

## Phase 1 — Ground (`Explore` subagents, parallel)

Fan out 2–5 read-only subagents: map the module end-to-end, characterize the house design system (usually anchored on one flagship surface — in RentOk's case, HomeV2), trace the exact data shapes the redesign will touch. Observed dispatch titles: "Map Reviews module end-to-end," "Characterize homescreen design system," "Ground Attendance data shapes," "Map canonical section header pattern."

## Phase 1.5 — Reference (Mobbin MCP — conditional)

Only reach for this when the module has **no internal precedent** to draw from — a new onboarding flow, an analytics dashboard, a campaign builder. Search named best-in-class apps directly: `"Airbnb host creating a listing step by step onboarding"`, `"food menu management"`, `"survey results analytics page with response rate, per-question breakdown"`. This is a live lookup against real shipped products, not a taste/style skill — none of the catalogued taste skills (`design-taste-frontend`, `gpt-taste`, `high-end-visual-design`, etc.) were ever used in these sessions; Mobbin is the actual mechanism. Figma is likewise essentially unused (2 marginal lookups against an already-locked spec, never generative).

**Pick the best ideas, never copy wholesale.** This is a direct, repeated user instruction: *"don't copy blindly. Think & brainstorm — we should pick only the best things from the references... that cohesion is the north star."* Applies equally to internal reuse (adapting Rooms' header pattern for a new module) and external reference (Mobbin results) — adapt the underlying idea, not the literal implementation.

## Phase 2 — Design-language check (`obsidian` + `DESIGN.md`/`PRODUCT.md`)

Pull the pinned house design language before designing anything new. These two files aren't ad hoc — they're the documented output of `impeccable`'s own `teach.md` sub-flow (strategic register/users/purpose in PRODUCT.md; visual theme/tokens/components in DESIGN.md, following the Stitch DESIGN.md format). Read them, don't reinvent them per module.

## Phase 3 — Audit, no code (`impeccable`, sometimes + `web-design-guidelines`)

This is the real spec step for a redesign — there's no separate brief/pre-mortem/domain-modeling stage the way `feature-design-pipeline` has, because the module already exists and the audit IS the grounding. `impeccable` is scored against Nielsen's 10 usability heuristics at 0–4 each (`reference/heuristics-scoring.md`) — a real observed pass scored **36/40**. Re-run this any time a build gets rejected, not just once at the start; the Tasks Runner redesign was re-audited mid-project after the user rejected the first build outright: *"the runner ui is not top 1% at all... a real rejection, not a nitpick."*

`impeccable` already has dedicated sub-references for onboarding flows (`onboard.md`), UX copy (`ux-writing.md`), layout/visual-hierarchy (`layout.md`), spacing/nesting (`spatial-design.md`), interactive states (`interaction-design.md`), delight (`delight.md`), and performance (`optimize.md`). **Don't build separate pipeline steps for these** — invoking `impeccable` routes to whichever reference the audit needs. The two things it does *not* cover: instrumented performance measurement (it judges, doesn't measure) and literal guided-tour/coachmark widgets (its onboarding coverage is flow-strategy, not that specific UI pattern) — add those explicitly if a module needs them.

**If the redesign genuinely needs a backend change**, scope it here as a narrow, isolated prereq — build and commit it first, in its own paired backend worktree, before the frontend build starts against it. Otherwise the API contract stays frozen — the observed house-rules block includes "frozen API" as a hard line, and the pattern shows up repeatedly: *"Committed backend prereq; built Today tab; built Menu tab."*

## Phase 4 — Plan (`superpowers:writing-plans`)

Turn the locked design into a task-by-task implementation plan. This is where the pre-code lock happens: *"Lock the design with the user BEFORE coding — the user is design-exacting."* No task list gets written against an unlocked design.

## Phase 5 — Build (`interface-design` via `superpowers:subagent-driven-development`)

Execute the plan with a strict per-task loop, each step its own `general-purpose` subagent: Implement Task N → Review Task N (spec + quality) → Fix (if the review finds something) → Re-review. This discipline is what prevents a fast build from silently drifting off the locked spec.

Reuse existing components and services (Rooms, Dues, Collections, Expenses, shared UI primitives) rather than parallel-inventing them — this is the same "don't copy blindly, but don't rebuild blindly either" instinct applied to code, not just visuals.

## Phase 6 — Motion (`emil-design-eng`)

Micro-interaction pass — autosave indicators, popovers, tactile swipe rows. `apple-design`, `animation-vocabulary`, `review-animations`, and `improve-animations` (the emilkowalski skill pack) sit adjacent to this phase as deeper motion tooling, but weren't part of any session this playbook is verified against — reach for them when a module's motion needs go beyond what `emil-design-eng` covers on its own (e.g. `review-animations` as a stricter gate, `improve-animations` for a retroactive whole-module motion audit).

## Phase 7 — Live verify (`playwright` + raw browser tool calls)

**This is the single highest-volume activity in every real session** — hundreds of browser calls in some sessions. Real login with test credentials, a real mobile viewport (390×844 is the recurring default), real screenshots, pixel-level checks (a divider that must only render between inactive tabs, never adjacent to the active pill). "Done" is not a status Claude gets to declare from reading its own diff — it gets declared after this step, and only after this step.

## Phase 8 — Final gate, dual and parallel

Design-craft and code-quality are graded **separately, not folded into one pass**:
- `impeccable` — 2 independent critique assessments run in parallel, not one
- `code-review --high` — 8 angles, also in parallel: line-by-line diff scan, removed-behavior audit, cross-file call-site tracer, reuse, simplification, efficiency, altitude, CLAUDE.md conventions
- `agent-skills:code-reviewer` — a fresh, context-free pre-merge diff review, deliberately separate from the two above so it isn't anchored on the same assumptions

## The round loop (before Phase 9)

The pipeline is not linear — phases 3–8 repeat as **rounds**, each opened by the user's feedback on the last one. Reviews ran 8 rounds; Food and Tasks each ran several. A round: log the verbatim feedback in the ledger → re-audit if the rejection was craft-level (not just a bug list) → plan → build → verify. The observed round names tell the story: "Round 2: audit + top-of-the-line polish," "Round 3: dogfood + polish," "Round 4: enterprise taste pass," "Round 8: systematic polish." Ship only follows an accepted round.

## Phase 9 — Ship (`finishing-a-development-branch`)

Merge/PR/cleanup decision. In the observed sessions, the actual merge routes through a **named human gatekeeper** ("awaiting Vivek's review per house rules — only Vivek merges") — the automated gates above are what earn the right to ask that person, not a replacement for asking them.

---

## Standing discipline (the whole time, not a phase)

- **READ FIRST, IN FULL** — every resumed session reloads the entire redesign ledger, not just recent entries. This is the single most repeated instruction across all sessions (151 occurrences) — it's the active defense against context loss across many parallel worktrees.
- **Restate the bar, don't assume it's remembered** — "top 1%" gets re-stated at the start of nearly every session (227 occurrences), because it's easy to drift toward "good enough" across a long multi-session project.
- **Quote rejections verbatim** — a real rejection like *"the runner ui is not top 1% at all"* gets carried forward into the next session's prompt as a citable record, not paraphrased into something softer.
- **Cross-module reuse is user-triggered, never assumed** — Claude doesn't autonomously decide "this worked for Food, let me apply it to Tasks too." The user says "recall how we did X, now do the same for Y" first, every time.
- **Self-certify before moving from plan to build** — "we may proceed, only if you're satisfied with your plan & approach — 100% sure."

## What "done" looks like

A module where: the audit score is recorded (not just "looks good"), the build was reviewed task-by-task against the locked spec, the motion pass happened, every claim of "working" has a real screenshot behind it, the dual gate (design-craft + code-quality, independently) passed, and a named human approved the merge. Anything short of that is a round, not a ship.
