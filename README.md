# module-redesign-pipeline

A reusable Claude Code **skill** that turns "this module looks generic / dated / not top 1%" into a shipped, live-verified redesign of an **existing** screen or section — grounded in the module's real code, benchmarked against real reference products, gated by a scored audit, and never accepted on a claim alone.

> Redesigns an EXISTING surface end-to-end, through build and ship. Not a new-feature-scoping skill — see [feature-design-pipeline](https://github.com/eazyapp-tech/feature-design-pipeline) for that.

Every phase, gate, and standing rule in this skill is mined from **66+ real redesign sessions** (Reviews, Food/FoodV2, Tasks, Change Room on RentOk's manager webapp) — not a theoretical process. It's the tool sequence, the operator discipline, and the design principles that actually made each of those land, made reusable.

## What it does

Runs an ordered, looping pipeline: **frame → ground the codebase → reference (conditional) → check the house design language → scored audit → plan → build → motion pass → live verify → dual final gate → ship.** Phases 3–8 repeat as rounds driven by the user's real feedback — real modules took 2–8 rounds. It orchestrates other skills (`impeccable`, `interface-design`, `emil-design-eng`, `playwright`, `code-review`) rather than replacing them, and adds the connective tissue those don't cover on their own: the per-module memory ledger, the pre-code design lock, the dual craft/code final gate, and a named human merge owner.

Three ideas do the heavy lifting:
1. **Ground before you touch pixels** — map the real module first; only reach outside (Mobbin, for real reference screens from best-in-class apps) when there's genuinely no internal precedent.
2. **The user is the real final gate, not the skills** — verbatim rejections get logged and carried forward, not paraphrased into something softer.
3. **Nothing is "done" without live proof** — a real login, a real viewport, a real screenshot. This is the single highest-volume activity in every real session behind this skill.

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

## Files

| File | What |
|---|---|
| `module-redesign-pipeline/SKILL.md` | The orchestrator — the phase pipeline, the one hard gate, design principles, red flags (rationalization counters), known gaps, and how it composes with `feature-design-pipeline`. |
| `module-redesign-pipeline/PLAYBOOK.md` | Human-readable playbook — the pipeline linearly with the evidence per phase, and the round loop. Read/share this. |
| `module-redesign-pipeline/references/redesign-ledger-template.md` | The `project_<module>-redesign.md` structure to copy for a new module — Decisions Locked, Round N Feedback, House Rules, Session Lineage, and the resume-prompt shape. |

## Relationship to feature-design-pipeline

They compose at two points, not just "similar but different":

- **A brand-new module redesign opens by invoking [feature-design-pipeline](https://github.com/eazyapp-tech/feature-design-pipeline) itself** — real kickoffs (Reviews, Tasks, Change Room) all did this. Only its framing phase runs; its document stack (`brief`, `pre-mortem`, `domain-modeling`, `doc-handoff-review`) never fires here, because the module already exists and the scored audit in this pipeline serves as the spec.
- **A backend prereq uncovered mid-redesign that's too large to build directly** (a new data model, a vendor integration, anything touching money/legal) hands off to a full `feature-design-pipeline` run as its own workstream — this pipeline resumes once it ships.

| | feature-design-pipeline | module-redesign-pipeline |
|---|---|---|
| Starting point | A feature that doesn't exist yet | A module/screen that already exists and looks bad |
| Ends at | Design docs (brief + spec + pre-mortem), handoff to a plan | A shipped, live-verified, merged redesign |
| Core loop | Linear: frame → ground → research → spec → lock → persist | Looping rounds: audit → build → motion → verify → gate, repeated until accepted |
| Gate | User approves the design docs | Scored `impeccable` audit (Nielsen heuristics /40) + dual final gate + named human merge owner |

## Provenance

Built by mining raw session transcripts (not memory summaries — those turned out to hallucinate specific skill-usage claims twice during this project) across 66+ sessions spanning the Reviews, Food/FoodV2, Tasks, and Change Room redesigns on RentOk's manager webapp. Comprehension-tested with fresh-context subagents before and after fixes — the first test run caught a real gap (a persona from one module bleeding into an unrelated one through playbook inheritance), which is now an explicit rule in the skill.

Companion: [feature-design-pipeline](https://github.com/eazyapp-tech/feature-design-pipeline) — the sibling orchestrator for scoping a brand-new feature before any code exists.
