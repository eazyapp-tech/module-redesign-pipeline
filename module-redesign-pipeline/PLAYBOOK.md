# Module Redesign Pipeline — Playbook

The human-readable version of the `module-redesign-pipeline` skill. Worked examples throughout: the RentOk Reviews, Food/FoodV2, Tasks, and Change Room redesigns — 66+ real sessions mined for this, not a theoretical process.

---

## The shape of it

```
Ask → [0] Frame → [1] Ground → [1.5] Reference → [2] Design-lang → [3] Audit → [3.5] Lock → [4] Plan → [5] Build → [6] Motion → [7] Verify+instrument → [8] Final gate → [9] Ship
       fdp framing    registry +     Mobbin MCP      obsidian/         impeccable     artifact-   writing-  interface-    emil-       playwright +       impeccable×2 +     finishing-a-
       inline, or     Explore        (only if no      DESIGN.md         (scored /40)   design      plans     design via    design-eng  DevTools trace +   web-design-        dev-branch
       brainstorming  subagents      internal          PRODUCT.md        + parity       render =              subagent-                react-scan + axe   guidelines +       (+ post-merge
       (new screen)   (parallel)     precedent)                          matrix         THE LOCK              driven-dev                                  code-review +      audit)
                                                                                                                                                          code-reviewer
                                        ↑ phases 3–8 loop as ROUNDS; interim rounds end at [7]; [8] runs on the acceptance round ↑
```

Five ideas make it work, more than any single skill:
1. **Ground before you touch pixels.** Never redesign against a guess of what's there. Map the real module, and only reach outside (Mobbin) when there's genuinely no internal precedent.
2. **The user is the real final gate, not the skills.** `impeccable` and `code-review` catch a lot, but the sessions show the user's own verbatim rejections ("not top 1% at all") are what actually reopen a round. Preserve those quotes; don't soften them.
3. **Nothing is "done" without live proof.** The single highest-volume activity in every real session is browser verification — login, viewport, screenshot, pixel-check. A claim of "done" without that is not done.
4. **Wired gates, not shelf inventory.** Most installed design tooling was never invoked in the origin sessions. The gates here are mandatory in the phases, not optional add-ons: untraced = unmeasured = unverified.
5. **Grounding accumulates in a component registry, not in session context.** The origin sessions re-ran the same "map the canonical components" agents every session and discarded the answers. The registry accumulates them; round close pays it back.

---

## Phase 0 — Frame (and set up)

For a brand-new module redesign, run `feature-design-pipeline`'s **framing steps inline** — restate the ask, expand it, and **state it back to the user for alignment before acting** (verbatim from the sessions: *"current phase: think on the ask, expand/refine it, and state it back to the user for alignment before acting"*). Do **not** invoke the full skill: its document stack (`brief`, `pre-mortem`, `domain-modeling`, `grilling`, `doc-handoff-review`) never fired in a single redesign session, because the module already exists and the Phase-3 scored audit serves as the spec. For a new screen or tab inside an already-framed module, a lighter `superpowers:brainstorming` pass is enough.

First session in a module also does the setup block (SKILL.md "Phase 0 setup"): preflight the MCPs (Mobbin, Chrome DevTools — with named fallbacks), create the ledger at the project memory directory, create the worktree on `redesign/<module>-module`, and learn the launch rule — **LAUNCH FROM the main repo folder (memory keying), work in the worktree.** Real sessions state this in the prompt because a session launched from the worktree path doesn't auto-load the ledger.

If the user triggered playbook inheritance ("recall how we did Food, do the same here"), the observed procedure: one `Explore` per prior module's ledger to extract its playbook (parallel), one `Explore` to locate the new module in code, one `general-purpose` agent to live-audit the new module in the browser — synthesized into this module's fresh ledger. That's exactly how the Change Room kickoff ran.

The two pipelines also compose mid-project: a backend prereq too large to build directly (a new data model, a vendor integration, anything money/legal) becomes its own full `feature-design-pipeline` workstream — its complete research-and-spec treatment — and this pipeline resumes once it ships.

## Phase 1 — Ground (registry first, then `Explore` subagents in parallel)

**Read the repo's `COMPONENT-REGISTRY.md` first** (template: `references/component-registry-template.md`), and verify the entries this module will touch — paths still real, components unchanged. A stale registry is worse than none, same as stale grounding.

Then fan out 2–5 read-only subagents for what the registry doesn't cover: this module's own end-to-end flow, the real data shapes. Observed dispatch titles: "Map Reviews module end-to-end," "Ground Attendance data shapes," "Map canonical section header pattern." **One dispatch is always a backend capability check** — "Verify backend template limits," "Backend food/attendance capability check" — so the design never assumes an endpoint that doesn't exist. Its output classifies each surface FE-only vs MIXED in the ledger's §BACKEND SCOPE.

The failure this fixes: those dispatch titles repeated **across sessions** — the same canonical-header and reusable-kit maps re-derived again and again, then discarded. The registry is where the answers accumulate; a repo with no registry gets one seeded from this phase's output.

**Three knowledge homes, kept distinct:**
1. **Component registry** (in the repo, versioned) — canonical components with when-NOT-to-use notes, layout recipes, tokens/hooks, conventions, the do-NOT-copy legacy list, dated code-truth gotchas.
2. **`docs/<module>-redesign/`** (in the worktree, committed) — this redesign's specs, feature-parity matrix, and per-round plan files.
3. **Module ledger** (memory) — process: decisions, rounds, verbatim feedback, statuses with hashes, session lineage. Tooling gotchas (login quirks, viewport redirects) live in its §Verify Recipe — they're about our tools, not the code.

## Phase 1.5 — Reference (Mobbin MCP — conditional)

Only when the module has **no internal precedent** — a new onboarding flow, an analytics dashboard, a campaign builder. Search named best-in-class apps directly: `"Airbnb host creating a listing step by step onboarding"`, `"survey results analytics page with response rate"`. This is a live lookup against real shipped products — none of the catalogued taste skills were ever used in these sessions, and Figma was essentially unused (2 marginal lookups, never generative). **Pick the best ideas, never copy wholesale:** *"don't copy blindly... we should pick only the best things from the references."*

## Phase 2 — Design-language check (`obsidian` + `DESIGN.md`/`PRODUCT.md`)

Pull the pinned house design language before designing anything new. These files are the documented output of `impeccable`'s own `teach.md` sub-flow. **If the repo has neither, run the teach flow once** to generate them, commit alongside the registry, and note it in the ledger.

## Phase 3 — Audit, no code (`impeccable`, sometimes + `web-design-guidelines`)

The audit needs the app **live** — stand up the dev server and get test credentials from the user now, recording both in the ledger's §Verify Recipe (they'll be needed every Phase 7 anyway). There's no separate brief/pre-mortem stage the way `feature-design-pipeline` has: the module exists, and the audit IS the grounding. Scored against Nielsen's 10 heuristics at 0–4 each (`impeccable/reference/heuristics-scoring.md`); **the score is the baseline the redesign must beat**, re-scored at the acceptance round (a real observed acceptance: 36/40). Re-run the audit any time a build gets rejected at craft level — the Tasks Runner was re-audited mid-project after *"the runner ui is not top 1% at all... a real rejection, not a nitpick."*

Also produced here: the **feature-parity matrix** — one Explore dispatch ("Build feature-parity matrix" opened Reviews Round 2) listing every capability of the old surface × its status in the new, stored in `docs/<module>-redesign/`. Phase 8's removed-behavior audit checks the final diff against it — this is how "UI/UX only, functionality unchanged" gets enforced rather than asserted.

`impeccable` covers onboarding flows, UX copy, layout, spacing, interactive states, delight, and performance internally via its `reference/*.md` — don't build separate steps; invoke it and let it route. Backend needs surfaced by the audit go through the Backend Prereqs sequence (below).

## Phase 3.5 — Propose & lock (`artifact-design`)

The audit says what's wrong with the *old* module — it is not the new design. Present the proposed redesign direction **per surface as rendered artifacts** (`artifact-design` fired at exactly this seam in six-plus origin sessions — artifacts are what replaced Figma here): IA, layout, states, key copy. **The user approving that artifact is the pre-code lock** — hard gate #1. Log the approved spec in the ledger's §IA SIGNED OFF, per surface. *"Lock the design with the user BEFORE coding — the user is design-exacting. No coding yet — 1st plan & brainstorm & lock it with me."*

## Phase 4 — Plan (`superpowers:writing-plans`)

Turn the locked §IA SIGNED OFF spec into a task-by-task plan, written to `docs/<module>-redesign/<surface>-plan.md` (or `round<N>-<name>-plan.md`) in the worktree and committed — that's where every real plan lived ("Execute docs/food-redesign/feedback-plan.md", "docs/reviews-redesign/round8-systematic-polish-plan.md"). Plans are written only against a locked design.

## Phase 5 — Build (`interface-design` via `superpowers:subagent-driven-development`)

**Session scope = one surface** — a tab, a wizard, a header — never "the module." That's how every real module was built: "DESIGN + build the Attendance tab," "build the FoodV2 Settings tab," "HEADER-ONLY ground-up design pass."

The parent loads `interface-design`; execution fans to `general-purpose` subagents in a strict per-task loop: Implement Task N → Review Task N (spec + quality) → Fix → Re-review. In a round-wide rebuild, batch tightly-related surfaces in **pairs** per parallel subagent — "Rebuild SurveysTab + OverviewTab," "Build TrendLine + Diagnostic (T4,T6)" — keeping Review as its own dispatch.

**Each build-subagent prompt carries:** the plan task, the relevant §IA SIGNED OFF section, the House Rules block, and the registry's relevant entries. A subagent that can't see the registry parallel-invents with full confidence. Registry check before any new component: found → adapt per its notes; do-NOT-copy list → named replacement; absent → one Explore confirm, then build.

**After a parallel multi-surface rebuild, run one hygiene subagent** ("Hygiene refactor shared helpers" closed Reviews Round 2) to dedupe the helpers the parallel builders just duplicated — *before* the round's verify. Parallel building creates duplicates by construction; don't wait for the registry's "3+ call sites" bar within a single round.

## Phase 6 — Motion (`emil-design-eng`)

Micro-interaction pass — autosave indicators, popovers, tactile swipe rows. `apple-design`, `animation-vocabulary`, `review-animations`, `improve-animations` are deeper motion tooling for when needs exceed `emil-design-eng`'s coverage (they weren't part of the origin sessions).

## Phase 7 — Live verify + instrument

**The single highest-volume activity in every real session** — hundreds of browser calls in some. Real login with the §Verify Recipe credentials, a real mobile viewport (390×844 recurring), real screenshots, pixel-level checks. "Done" is declared after this step, only after this step.

Two mandatory halves:
- **Visual/behavioral:** playwright screenshots, flow walks, pixel checks. Flutter: golden tests + `integration_test`.
- **Instrumented:** Chrome DevTools MCP `performance_start_trace` on the primary flow — real LCP/INP/CLS against the ledger's Performance Budget — plus `npx react-scan@latest <url>` and an axe scan. Flutter: `--profile` overlay, no dropped frames past 16ms. Untraced = unmeasured = unverified.

Two observed disciplines that live here:
- **Mock-then-revert:** when reaching a state needs injected mock data, the sequence is verify → **revert every mock** → `git status` residue check → commit ("finish live-verifying ROUND 2, then revert mocks + commit").
- **Sibling spot-check:** touched a shared component → live spot-check its other consumer modules at the breakpoint matrix ("verified at 390/800/1280px + spot-checked Leads for regressions"). The registry's Used-by column is the consumer list.

## Phase 8 — Final gate (parallel, acceptance rounds only)

Interim rounds end at Phase 7. The full gate runs when a round is believed to be the acceptance round — it's expensive by design. Three dimensions graded **separately, never folded**:
- **Design-craft:** two parallel `general-purpose` subagents, each given the live URL/screenshots and impeccable's critique flow, no shared context.
- **Guidelines-compliance:** `web-design-guidelines` against the FINAL code — mandatory for web (in the original 66+ sessions this ran only twice, as an optional sidekick; that was a wiring failure, not a judgment). Flutter swaps in `apple-design`'s gesture/motion/reduced-motion sections + Material guidance.
- **Code-quality:** `code-review --high` (8 angles; the removed-behavior angle checks against the Phase-3 feature-parity matrix) + a fresh, context-free `agent-skills:code-reviewer` pre-merge pass, deliberately unanchored on the others' assumptions.

## Phase 9 — Ship (`superpowers:finishing-a-development-branch`)

Merge/PR/cleanup, through a **named human gatekeeper** ("awaiting Vivek's review per house rules — only Vivek merges") — the automated gates earn the right to ask that person, they don't replace asking. **Post-merge, optionally but observed:** a fresh code-review + design pass on the merged diff *before human reviewers read it* ("post-merge top-1% design & code quality audit, so Nimit/Vivek/Ishika don't reject it"), fixes landing on `fix/<module>-post-merge-<topic>`.

---

## The round loop

Phases 3–8 repeat as **rounds**, each opened by the user's feedback on the last. **The first full pass is Round 1** — logged in the ledger before any feedback exists. Reviews ran 8 rounds; Food and Tasks several each. A round: log the verbatim feedback (prepended at the top of the ledger with a status emoji) → re-audit if the rejection was craft-level → plan → build → verify. Interim rounds end at Phase 7; the Phase-8 gate runs on the acceptance round.

Observed round flavors: "Round 2: audit + top-of-the-line polish," "Round 3: dogfood + polish," "Round 4: enterprise taste pass," "Round 8: systematic polish." A **dogfood round** = walk every workflow end-to-end as the locked persona, at realistic data scale, harvesting an itemized fix list before polishing ("actually walk the workflows at scale, critique systematically, then execute a coherent pass"). Rounds can carry a **rule change** — a dated House-Rules amendment in the ledger.

## Backend prereqs — sequenced by contract, not build order

What the sessions actually did (the naive "backend first, then FE" is NOT it):
1. Phase 1's capability check classifies each surface FE-only vs MIXED (§BACKEND SCOPE).
2. Phase 3 locks the **contract** — endpoint shape, fields, semantics. The API is otherwise frozen.
3. **FE builds against the locked contract with mocks while the endpoint is pending** — the Feedback tab's FE was built, reviewed, and tsc-clean before its endpoint existed. The endpoint **must exist before Phase 7** live-verify: unverifiable = not done.
4. Backend work in its own worktree (`../<backend-repo>-<thing>`, branch `feat/<module>-<thing>` or `fix/...`), commits **user-asked, never automatic** ("Ask me whether to commit the backend change").
5. Small prereq (endpoint, field) → build directly. Large (data model, vendor, money/legal) → its own `feature-design-pipeline` workstream; resume when it ships.

## Standing discipline (the whole time, not a phase)

- **READ FIRST, IN FULL** — every resumed session reloads the entire ledger (151 occurrences in the evidence). The active defense against context loss across parallel worktrees.
- **Restate the bar, don't assume it's remembered** — "top 1%" re-stated at the start of nearly every session (227 occurrences).
- **Quote rejections verbatim** — carried into the next session's prompt as a citable record, never paraphrased.
- **Cross-module reuse is user-triggered, never assumed** — the user says "recall how we did X, do the same for Y" first, every time.
- **Self-certify before moving from plan to build** — "we may proceed, only if you're satisfied with your plan & approach — 100% sure."

## What "done" looks like

A module where: the audit baseline was scored and beaten (not just "looks good"), the design was locked as a user-approved artifact before code, the build was reviewed task-by-task against §IA SIGNED OFF, the motion pass happened, every claim of "working" has a real screenshot and a real trace behind it, mocks were reverted before every commit, shared-component siblings were spot-checked, the final gate passed on all three dimensions independently (design-craft, guidelines-compliance, code-quality), and a named human approved the merge. Anything short of that is a round, not a ship.
