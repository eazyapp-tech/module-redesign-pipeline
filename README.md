# module-redesign-pipeline

A reusable Claude Code **skill** that turns "this module looks generic / dated / not top 1%" into a shipped, live-verified redesign of an **existing** screen or section — grounded in the module's real code, benchmarked against real reference products where no internal precedent exists, gated by a scored audit and real performance traces, and never accepted on a claim alone.

> Redesigns an EXISTING surface end-to-end, through build and ship. Not a new-feature-scoping skill — see [feature-design-pipeline](https://github.com/eazyapp-tech/feature-design-pipeline) for that.

Every phase, gate, and standing rule in this skill is mined from **66+ real redesign sessions** (Reviews, Food/FoodV2, Tasks, Change Room on RentOk's manager webapp) — not a theoretical process. It's the tool sequence, the operator discipline, and the design principles that actually made each of those land, made reusable.

## What it does

Runs an ordered, looping pipeline: **frame → ground the codebase → reference (conditional) → check the house design language → scored audit → propose & lock (rendered artifact) → plan → build → motion pass → live verify + instrument → final gate (acceptance round) → ship.** Phases 3–8 repeat as rounds driven by the user's real feedback — real modules took 2–8 rounds. It orchestrates other skills (`impeccable`, `interface-design`, `emil-design-eng`, `playwright`, `web-design-guidelines`, `code-review`) rather than replacing them, and adds the connective tissue those don't cover on their own: the per-module memory ledger, the pre-code design lock, the instrumented verification gate, and a named human merge owner.

Five ideas do the heavy lifting:
1. **Ground before you touch pixels** — map the real module first; only reach outside (Mobbin, for real reference screens from best-in-class apps) when there's genuinely no internal precedent.
2. **The user is the real final gate, not the skills** — verbatim rejections get logged and carried forward, not paraphrased into something softer.
3. **Nothing is "done" without live proof** — a real login, a real viewport, a real screenshot. This is the single highest-volume activity in every real session behind this skill.
4. **Wired gates, not shelf inventory** — an audit of the source sessions found most installed design tooling was never invoked. This skill makes the gates *mandatory in the phases*, not optional add-ons: untraced = unmeasured = unverified.
5. **Grounding accumulates in a component registry, not in session context** — the origin sessions re-ran the same "map the canonical components" agents every session and discarded the answers. The pipeline maintains a per-repo `COMPONENT-REGISTRY.md` (canonical components with when-NOT-to-use notes, a do-NOT-copy legacy list, house conventions, dated code gotchas): registry-check before any new component at build, registry pay-back at every round close. Reuse with judgment, indexed — never blind copying.

## The Designer's Gates (enforced, not just documented)

Three checks tied to a moment in the work — not a rule pile someone has to remember. `references/gates.md` names them; two hooks in `~/.claude/settings.json` fire them whether or not anyone remembered, at the exact moment they matter. **Set up once per machine: `references/hooks-setup.md`.**

| Gate | Fires when | Passes when |
|---|---|---|
| **1 · Surface Ready** | a new component file is created | seven answers exist and the stakeholder has seen them: what it IS, the question she came with, the internal precedent, two outside references (Mobbin), two rendered directions, the pick and why, what the spec gets wrong |
| **2 · Done Probe** | `git commit` with a UI component staged | `scripts/run_probe.py` passes at 375 and an explicit 1440 (one centre per control row, sticky x unchanged after a pan, popovers portaled with a gutter, no 0px icons, flex peers within 2px, no sideways scroll, first-row y on the phone judged, nothing opened by a programmatic focus) and its output is in the commit message |
| **3 · Shared Primitive** | editing tokens, primitives, a shared header, theme | consumers grepped first, one concern per function, the probe re-run on a consumer after |

`references/gates.md` also holds the working contract with the stakeholder (lead with a pick, expand feedback before acting on it, their suggestion is an input not an order, say which of the seven is missing rather than claim 100%), the taste bar, and the code bar — this is where "the agent is the designer" becomes checkable rather than aspirational. Mined from a session with eleven corrections of one shape: a rule that existed as prose and still got broken, because the gap was never knowing the rule, it was the moment it should have fired.

**Model note.** Runs on Sonnet most of the time in practice, sometimes Opus, occasionally a stronger model dispatched for one framing decision. Nothing in the gates depends on the model remembering — the hook injects the check, the probe prints numbers, every pass condition has a threshold.

## The gates (what "done" actually requires, phase by phase)

| Phase | Gate | Tools |
|---|---|---|
| 3 — Audit | Scored, no-code audit before any build | `impeccable` (Nielsen's 10 heuristics × 0–4, /40) |
| 3.5 — Propose & lock | The user approves a **rendered artifact** (`artifact-design`) per surface — that approval IS the pre-code lock | `artifact-design` |
| 7 — Live verify + instrument | Visual proof AND measured performance vs a per-module budget (LCP < 2.5s · INP < 200ms · CLS < 0.1 defaults) | Web: `playwright` + **Chrome DevTools MCP** trace + `npx react-scan` + axe scan. Flutter: golden tests + `integration_test` + DevTools `--profile` overlay |
| 8 — Final gate (parallel, acceptance rounds only) | Design-craft, guidelines-compliance, motion-craft, and code-quality graded **separately** | `impeccable` ×2 independent + `web-design-guidelines` (mandatory, web) + `review-animations` (if the round touched motion) + `code-review --high` (8 angles) + a fresh context-free reviewer |
| 9 — Ship | A named human merge owner, not just the automated gates | `finishing-a-development-branch` |

## Platform profiles

Same pipeline, different tools per target — pick before Phase 4, record in the ledger:

- **Existing web app** — the incumbent stack is the frozen constraint (Chakra 2.5 in the origin project); build within it, never migrate mid-redesign. Verify with playwright + Chrome DevTools MCP + react-scan + axe.
- **Flutter** — golden tests for visual regression, `integration_test` for flows, DevTools performance overlay/timeline in `--profile` mode (16ms frame budget), `flutter analyze` = 0 replaces `tsc --noEmit` = 0. Compliance lens: `apple-design` (gestures/motion/reduced-motion) + Material guidance instead of `web-design-guidelines`.
- **Greenfield** — no legacy constraint: default to **shadcn/ui + Tailwind + Radix** and wire the registry MCPs (shadcn MCP, optionally 21st.dev Magic) from day one; `frontend-design` sets aesthetic direction before `interface-design` builds.

## Install

**As a personal skill** (per user):
```bash
cp -R module-redesign-pipeline ~/.claude/skills/
```
Restart Claude Code (or start a new session). It routes on asks like "redesign this module", "make X top 1%", "this looks generic/dated, fix it", or a resumed "continue the X redesign" session.

**As a project skill** (shared via a repo):
```bash
cp -R module-redesign-pipeline <your-project>/.claude/skills/
```

**Then wire the gates (once per machine, either install path)** — see `references/hooks-setup.md`. Without this, `SKILL.md` and `references/gates.md` are read as documentation, not enforced as gates.

**Recommended companions** (Phase 7 instrumentation expects these):
```bash
# Chrome DevTools MCP — real LCP/INP/CLS traces (Google official)
claude mcp add -s user chrome-devtools -- npx chrome-devtools-mcp@latest
# react-scan needs no install — the skill invokes `npx react-scan@latest <url>` directly
```
Mobbin MCP (reference screens) and the skills it orchestrates (`impeccable`, `interface-design`, `emil-design-eng`, `web-design-guidelines`, superpowers suite) should be present for the full pipeline; the skill degrades gracefully but the gates assume them.

## Files

| File | What |
|---|---|
| `module-redesign-pipeline/SKILL.md` | The orchestrator — the phase pipeline, the one hard gate, platform profiles, design principles, red flags (rationalization counters), known gaps, and how it composes with `feature-design-pipeline`. |
| `module-redesign-pipeline/PLAYBOOK.md` | Human-readable playbook — the pipeline linearly with the evidence per phase, and the round loop. Read/share this. |
| `module-redesign-pipeline/references/redesign-ledger-template.md` | The `project_<module>-redesign.md` structure to copy for a new module — the observed section vocabulary (§IA SIGNED OFF, §BACKEND SCOPE, Surface Status, Shared-Surface Playbook, Verify Recipe...), the emoji/prepend-to-top living conventions, and the resume-prompt shape. |
| `module-redesign-pipeline/references/component-registry-template.md` | The per-repo `docs/design/COMPONENT-REGISTRY.md` structure — canonical components (use / when-NOT-to-use / gotchas), layout recipes, tokens & hooks, house conventions, do-NOT-copy legacy list, extraction candidates, dated learnings. Lives in the target repo, versioned with the code. |
| `module-redesign-pipeline/references/gates.md` | **The Designer's Gates.** Surface Ready / Done Probe / Shared Primitive, the working contract with the stakeholder, the taste bar, the code bar, environment traps. Read this before `SKILL.md` if you only read one file. |
| `module-redesign-pipeline/references/hooks-setup.md` | The exact `settings.json` hook block that makes the gates fire, plus a verify snippet. Do this once per machine — a skill folder cannot wire hooks on its own. |
| `module-redesign-pipeline/references/expansion-rule-worked-example.md` | A real audit round that failed the expansion rule, worked through step by step, plus the state-combination measurement rule (measure alignment with every toggle ON, not the default state). |
| `module-redesign-pipeline/scripts/ui-probe.js` + `scripts/run_probe.py` | The Done Probe. A browser-side script that measures a live page (centre lines, sticky drift, popover portaling/gutter, icon widths, flex-peer widths, tap targets, focus leaks) and a Python/Playwright runner that drives it at any set of widths from one command. |
| `module-redesign-pipeline/learnings.md` | Dated corrections, newest first, each with the rule it produced — read at the start of every round, append whenever one lands. |

## Relationship to feature-design-pipeline

They compose at two points, not just "similar but different":

- **A brand-new module redesign opens by invoking [feature-design-pipeline](https://github.com/eazyapp-tech/feature-design-pipeline) itself** — real kickoffs (Reviews, Tasks, Change Room) all did this. Only its framing steps run, inline (the full skill is not invoked); its document stack (`brief`, `pre-mortem`, `domain-modeling`, `grilling`, `doc-handoff-review`) never fires here, because the module already exists and the scored audit in this pipeline serves as the spec.
- **A backend prereq uncovered mid-redesign that's too large to build directly** (a new data model, a vendor integration, anything touching money/legal) hands off to a full `feature-design-pipeline` run as its own workstream — this pipeline resumes once it ships.

| | feature-design-pipeline | module-redesign-pipeline |
|---|---|---|
| Starting point | A feature that doesn't exist yet | A module/screen that already exists and looks bad |
| Ends at | Design docs (brief + spec + pre-mortem), handoff to a plan | A shipped, live-verified, merged redesign |
| Core loop | Linear: frame → ground → research → spec → lock → persist | Looping rounds: audit → lock (rendered artifact) → build → motion → verify+instrument, repeated; full gate on the acceptance round |
| Gate | User approves the design docs | Scored `impeccable` audit (/40) + instrumented perf budget + three-dimension final gate + named human merge owner |

## Known gaps (deliberate, documented in the skill)

- **Field performance data** — Phase 7's traces are *lab* numbers; real-user vitals (RUM) still need a production analytics hookup per module.
- **Guided tours / coachmark widgets** — onboarding *flow strategy* is covered (`impeccable`'s onboard reference); the literal spotlight-tour UI pattern has no reference anywhere in the stack yet.
- **Flutter design/token skill** — the Flutter profile covers verification and compliance, but no dedicated Flutter design skill exists in any ecosystem yet (independently confirmed by two separate research passes).

## Provenance

Built by mining raw session transcripts (not memory summaries — those turned out to hallucinate specific skill-usage claims twice during this project) across 66+ sessions spanning the Reviews, Food/FoodV2, Tasks, and Change Room redesigns on RentOk's manager webapp. Comprehension-tested with fresh-context subagents at each revision — the first test caught a real gap (a persona from one module bleeding into an unrelated one through playbook inheritance), the wiring update was re-tested on four new behaviors (instrumented verify, Flutter profile, greenfield defaults, gate count) and passed all four.

Companion: [feature-design-pipeline](https://github.com/eazyapp-tech/feature-design-pipeline) — the sibling orchestrator for scoping a brand-new feature before any code exists.
