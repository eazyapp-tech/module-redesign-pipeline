> **2026-08-23:** repo facts ("Repo truths", "Patterns worth stealing") moved to the repo at `docs/design/PATTERNS.md`; tooling traps to `references/traps.md`; cross-repo patterns to `references/patterns.md`. This file keeps the *stories* behind rules. Harvest at every commit: `references/harvest.md`.

# module-redesign-pipeline — learnings

## 2026-08-23 (late) — Complaint Bot Setup, Try a ticket rejected at the design level

### A grid is not a design. Phase 3.5 has no "small surface" exemption.
Built Try a ticket straight from the HTML artifact + a behaviour grid. Correct at every state,
live-verified at two widths, and still rejected: "It could have been made so much better if you
had put some more thought into it, like a proper lead designer... You just go ahead and code
everything or take whatever you find and just replicate it." What he was pointing at: the
surface IS a journey (tenant raises → first responder's window → climbs → climbs → ends), and I
drew it as a roster (rows of people with a time beside each). The grid could not catch that,
because a grid asks "what does each cell do in each state", never "what is this thing".

**Rule produced:** before the grid, one sentence: "This surface IS a ___." Then 2–3 directions
that differ in MODEL, each with the product whose IDEA it borrows, rendered as an artifact,
with a pick. Then one question. Then lock. Then grid. Then code. This is Phase 3.5 as already
written; the failure was deciding a modal was too small to deserve it. No surface is.
Persisted as memory `feedback_design-before-code-every-surface`.

## 2026-08-23 (later night) — Complaint Bot Setup, one question triggered a 45-defect sweep

### A single design question, followed once, is the expansion rule's real trigger — not a scheduled audit phase
The stakeholder asked a narrow product question (one-click team-add on a copy mismatch). Answering it
surfaced one confirmed bug (`bringOver` silently drops the person — a write resolved through a
collection that can never contain it). He then asked "any other such similar or any kind of misses
anywhere else in the module? I'm skeptical now." That one follow-up, not a scheduled Phase-3
re-audit, is what should trigger a full re-sweep of everything already built — the pipeline's Phase
3 audit gate is written as a phase you pass through once; in practice a live session reopens it the
moment a stakeholder's own skepticism says to, mid-round, on surfaces already marked done.

**Rule produced:** treat "are there more like this?" as a standing trigger for a full adversarial
sweep (parallel Explore/audit agents per surface, not one agent skimming the whole module), not a
one-off grep for the same shape. A single pattern instance is a sample of the sweep, never proof
the sweep is unnecessary.

### One confirmed bug's root cause, chased one level further, revealed the real fix already exists in the app
The `bringOver` bug's cause is "the write lands in the wrong collection." The naive fix is a
client-side mock-add. Grounding it in the actual backend (a dedicated Explore dispatch on "does a
cross-property add-existing-person capability already exist anywhere in this app") found it does:
`POST /teamMember/addDeleteTeamAccessByUuid` grants an EXISTING person access to another property
in one call, the team list is already account-wide, and `CopyAppAccessDrawer.tsx` is the exact UI
shape (source → targets → review pre-filled from live data → confirm → toast+refetch) to adapt.

**Rule produced:** when a bug's fix looks like "build a small thing," spend one Explore dispatch
checking whether the REAL thing already exists elsewhere in the app before building a shadow
version of it. A mock-add invented at the point of failure becomes technical debt the real
endpoint has to unwind later; the same one-Explore-dispatch discipline that finds an internal
design precedent (Phase 1.5) also finds internal API precedent, and it's just as cheap to run.

### A pattern named once (not four times) is the deliverable, even when the sweep runs in parallel
Four parallel audit agents on four different slices of the same module independently surfaced the
SAME root pattern ("write in collection A, read resolves through collection B") in five different
call sites. Reporting them as five separate findings would have been step-0 list-matching again,
scaled up. The synthesis step — after the parallel agents return, before reporting to the
stakeholder — has to re-derive the pattern across ALL of them and count instances, not just
concatenate four reports.

**Rule produced:** when running a multi-agent sweep, the synthesis pass is not optional formatting.
It is where the actual expansion-rule work (name the pattern, sweep the count) happens — the
individual agents only supply the raw instances.

### A drawn grid still needs live proof at every named state combination, even for a small surface
`try-a-ticket-grid.md` named the exact state combination that would break the footer ("Six people
on First AND a long type name AND 390px") before any component existed. Live-clicking through it
at 390px, not just reading the drawing, caught a real overflow the grid predicted the SHAPE of but
not the specific bug (a footer button colliding with its neighbors). The grid earned its keep by
naming where to look; it did not replace looking.

**Rule produced (reconfirms an existing one, worth restating): grid callouts name the state to
verify, they are not a substitute for verifying it live. A grid with no live check against its own
named combination is half the discipline.


**Read this at the start of every round. Append whenever a correction lands.** Same convention as `feature-map/learnings.md`. This file is living: it records what we know so far, and it gets raised whenever we learn something, not at some later tidy-up.

Entries are dated, newest first. Each one names the correction, the cost, and the rule it produced.

---

## 2026-09-07 — brand site kit, the round that built the locked direction

### A locked artifact can carry a redundancy the build must not
The lock drew the house plan and then a name-led inventory row underneath it that said the same
thing again: eight marks beside "Single, 8 rooms, 8 beds", then a row reading "Single sharing,
8 rooms, 8 beds free". Both were right in isolation and together they spent a thin page's whole
budget saying one fact twice. Merging them into one row is what actually delivered the move the
artifact ranked first (the name sets the row, the picture demotes to the right), because the
photo-led and no-photo rows then differ only in what sits in that slot.

**Rule produced:** at Phase 4, read the locked artifact as a design argument rather than as a
layout to transcribe, and say out loud in the plan where the build leaves it and why. The lock
is the direction and the reasons; the drawing is evidence for them, not a spec to trace.

### A threshold reasoned from first principles was wrong until it met real data
The drawn plan's ceiling was set at 48 marks with a perception argument: above that a row stops
being a quantity somebody counts. Rendering it on Signet refused its real 58-bed and 57-bed
tiers, which are the two rows on that page where the picture matters most, because "17 beds
free" hides that the tier is seventy per cent full. What the drawing communicates is the
proportion, not a count anybody makes, so the real ceiling is a layout one and it is 96.

**Rule produced:** a threshold in a new primitive is not decided until it has been rendered
against the widest real record in the benchmark set. Write the number, then go and find the row
that argues with it.

### The brand that was not being built for is where the regression is
Changing a shared copy helper so a one-house brand leads on its street broke Signet, which
leaves its headline unauthored on purpose and draws a vermilion full stop after the name the kit
supplies. The swap turned that signature into "Malad.". Nothing in the tests or in the brand
being built for showed it; a six-brand server render and a diff of the h1 did, and the same
sweep found a second brand whose only address is a bare city.

**Rule produced:** an edit to any shared copy or formatting helper gets rendered across the full
benchmark set before it is committed, and the registered brands are read for what they
deliberately leave out. A deliberate omission in a brand's content file is a dependency on the
fallback, and it is invisible to a fixture.

## 2026-08-24 — Complaint Bot Setup, the session that produced the gates

**Eleven corrections in one session, all of one shape: the rule existed and was not applied at the moment it mattered.** The expansion rule sat in CLAUDE.md in capitals and failed four times. So the remedy is not more prose; it is `references/gates.md` (three gates tied to moments), `scripts/ui-probe.js` + `scripts/run_probe.py` (numbers, not claims), and global hooks in `settings.json` that fire them. Built, tested against real hook payloads, and the probe run against the page that produced it (it found a real finding on its first run: five tap targets under 44px).

**The specific corrections, so none is lost:**
- Built Try a ticket from a grid, no design step, for a "small" surface. Rejected at the design level: "is that how a senior designer works?" Gate 1.
- "Time is the axis" was one level too shallow; a second opinion (Opus, via /consult-style dispatch) named causality. Use a second model at a framing fork, not for routine questions.
- Mobbin was pulled only after being asked. References are Gate 1 item 4, before designing.
- "Looks good" was consent-shaped on a look-only surface; "Done" on a control that closes; "unnamed types" was the spec's word. Copy is design.
- Empty states announced the hole instead of offering the fix in place; the fix now opens OVER the modal and the ladder replays. "Not the user-first workflow."
- Toolbar and dock were assembled, not designed: 34px beside 28px, centres 184/187/189, hairline dividers, prose in a command bar, a gradient slab welded to a capsule, a keypad on the phone. Taste bar in gates.md.
- Half the phone was chrome (first row y=419) and nobody measured it. The probe's first number.
- "Verified at 1440" twice at 800: the preview pane's desktop preset. Environment trap, and the probe sets widths by number.
- Fix-one-break-another, three times: a `pl` overridden by a later prop; a flush-to-edge overcorrection; a wrapper Box adding a second flex basis. Gate 3.
- Popovers: opened on any focus (programmatic included), several open at once, none portaled, flush at 375 of 375. One contract in tokens (POPOVER_ROOT + POPOVER + Portal), one owner (`useHoverCard`), close on scroll.
- Dock geometry hand-set: five paddings, six icon sizes, `flex: 1` dead in a content-width container, icons at 0px. Derive from one token; icons in em; tray fluid on a phone.
- Sticky column slid 56px and covered the tick column: sticky pins at `left`, not at its resting x. Cells pin at their true x and cover the space to their left.
- Direction-based reveal on scroll-up did not exist in the repo (the header's is position-based). Raised the house pattern rather than copying it.
- "Copy to an area…" was a second door to a room one tap inside the first. Delete the second door.
- Older sessions, mined for this entry: the drawing wins over the prose (copy conflicts built as cards when the artifact said table); built-from-a-reference means check the reference today before "fixing" (two reverted fixes); scroll architecture must match the house skeleton; one workstream per branch as ruled; a real phone found what the pane missed.

**Probe false positive fixed on first run:** sticky-cell height must be compared against the tallest SIBLING cell, not the row box, because the row's own padding is not a gap.

## 2026-08-22 — Complaint Bot Setup, round 2

### The audit returned exactly what was asked for, and that was the failure
An audit produced 30 verified findings with real measurements. It still failed, because every finding was a defect in something already built, and not one asked what the module could not do. The stakeholder: "I just don't understand why you take everything I say and limit yourself to that... You should never limit yourself to what I just say. You should always expand on it."

**Rule produced:** the expansion rule, now a hard gate in `SKILL.md`. Feedback is a sample, never the scope.

**Cost:** a full extra round, and trust. His words the round before: "We are still going around in the loop again and again. Pretty disappointed here."

### Alignment was measured in the default state only
Column x was verified as identical on every row, at two widths. It was measured with select mode **off** and no children expanded. With both on, every column on a child row shifts, because the parent passes `selectMode` to category rows and not to subtype rows, so the two use different grid templates. The stakeholder found it by looking once.

**Rule produced:** measure with state toggles ON together. A grid that aligns in the default state proves nothing, because the default state is the one nobody files a bug about. Added to Phase 3 and the red flags.

### A screen audit cannot see a missing capability
The audit catalogued the flat property picker as "needs a select-all" and never asked what the list should be *grouped by*. It never asked what the persona repeats. At real scale she names one person on 30 types through 30 separate drawer trips, because selection exists only to feed Copy.

**Rule produced:** Phase 3 must contain a workflow walk at real data scale, not only a defect sweep. And the workflow-first section: where the tool ends, the workflow starts.

### Checking the stakeholder's premise saved a wrong fix
Two properties in the test account share a name, so the copy picker appeared to offer the current property as a target, which read as a broken self-filter. It was not. The filter was correct; the account genuinely has two properties called "Ishika". The real finding was different and better: the picker has no disambiguator at all.

**Rule produced:** verify every checkable claim, including your own reading and the stakeholder's, before asserting it. Stolen from `feature-map` contract #4.

### The reference bar has to be named up front
"Better than what is in this module" is not a bar. The stakeholder named the actual set: the **homescreen** (global search bar and modal, scroll and expand/collapse, popovers, the property selector), **Timeline / Bed Availability**, and **Rooms**.

**Rule produced:** Phase 0 step 1.5 — name the reference screens in the ledger before anything else.

---

## Repo truths worth not re-deriving (rentok-manager-web, verified 2026-08-22)

- **Grouped property selection already exists, in exactly one file.** `components/Home/PropertySider.tsx` with Property / Area / Groups tabs. Grouping is **server-side**: `GET /v1/home/property-selector?group_by=property|area|groups` returns `{groups: [{group_label, icon_url, property_count, beds, rooms, tenants, properties[]}]}`, identical shape per tab. Do not build a client-side grouper. Eight near-duplicate flat pickers surround it; four have a global select-all; **none** have per-group select-all except PropertySider.
- **"Groups" in that tab is `property_type`** (PG / Hostel / Coliving), not user-defined clusters — backend `homepage/service.ts:4494`. "Area" is `locality`, "Property" is `city`. All three are mutually exclusive partitions; a property is in exactly one group per tab. **Real user-defined groups do exist** at `/v1/property-groups` (full CRUD, creator-scoped) and are **entirely unconsumed by web**. Do not conflate the two.
- **Logos are missing from the selector payload.** Only `property/getHomeDashboard` returns `logo_url`. Backfill via `hooks/usePropertyLogoMap.ts`.
- **Same-named properties are disambiguated by `address`** (server-composed) with `eazypg_id` as the tiebreaker. `PropertyStickyHeaderRow`'s `subtitle` slot is effectively unclaimed across all call sites and is the natural home for it.
- **There is one real motion token object in the repo:** `ReviewsV1/tokens.ts` `MOTION = { ease: [0.23,1,0.32,1], swap: 0.18, enter: 0.25, card: 0.35, stagger: 0.05 }`. HomeV2 has colour tokens and **zero** timing tokens. Eleven durations and six easings exist across the homescreen for what is conceptually four gestures.
- **Four distinct popover treatments exist.** The most disciplined family is ComplaintSetup + ReviewsV1: fixed width 240–300px, radius 14px, `1px solid HOME_V2_COLORS.border`, warm-neutral shadow, and Reviews re-declares `boxShadow` inside `_focus` so Chakra's focus ring cannot flatten it. Build against that, add `isLazy` and `_focus:{outline:none}` from the HomeV2 calendar popover.
- **`useReducedMotion` is honoured in exactly one file** in HomeV2 (`HomeV2Header.tsx`). Everything else ignores it, including an 8s infinite glow animation.
- **Three expand/collapse mechanisms coexist**, at ~0.2s / 0.3s / 0.18s. `peopleListHeader` alone uses two of them.

## Patterns worth stealing, with file:line

1. **`GlobalSearch/components/PropertyGroupHeader.tsx:29-51`** — sticky group header that transforms on stick: inset pill (radius 10, mx 24, soft shadow) becomes a full-bleed bar (radius 0, mx 0, deeper shadow) over 0.15s, detected by an IntersectionObserver sentinel rather than scroll math. Shadow is brand-tinted, not black. Best single idea on that surface.
2. **`GlobalSearch/components/EmptyState.tsx:12-43`** — the loading skeleton mirrors the real row's anatomy exactly (40px circle, 55% name bar, two 28px action circles, divider, footer CTA), so arrival causes zero layout shift.
3. **`HomeV2/blocks/FinancialsBlock.tsx:30-41`** — expansions reset when the block scrolls out of view, so you never scroll back to a stale open row.
4. **`Common/peopleListHeader.tsx:184-205`** — header collapse with three separate anti-jitter mechanisms: 40/15px hysteresis dead band, a 350ms collapse lock (because collapsing shrinks scrollTop and would immediately re-trigger expand), and a user-override ref that retires scroll control permanently once the person touches the chevron. All refs, never state.
5. **`HomeV2/shared/BlockCard.tsx:27`** — the app's signature entrance: `opacity 0→1, y 20→0`, `0.35s easeOut`, `delay index*0.07`. Keep it identical in new modules so they read as the same app.
6. **`PropertySider.tsx:1015-1023`** — Apply at zero selection is `opacity 0.5` but **still tappable**, and firing it nudges instead of doing nothing. A disabled button is a dead end; this is not.

## 2026-08-22 (late) — Complaint Bot Setup, round 2 close

**"Correct" is the floor, not the bar.** A repair pass that removes every defect (alignment, overflow, occlusion, a half-built selection model) gets a module to correct. It does not make it top 1%. The test that separates them: does the screen ANTICIPATE the person's real question, or does it wait? The setup board's real question was "will anything fall through?" and the board never answered it. Before calling any pass done, name the one question the person came with and point at the element that answers it. If you cannot, the pass is a repair pass. Say so in the commit message.

**Cherry-picked from `screen-handoff-pipeline` (Phases 3.5, 5, 6.75), now part of this pipeline's Phase 3:**
1. **Draw the behaviour grid before drafting.** Every cell × every state; every tappable thing → exactly what opens. Prose rules are not a grid; the gaps only show when the grid is filled.
2. **The zeros router, per number, never per screen.** An empty First rung is a bad zero (complaints fall to the catch-all). An empty Last rung is a neutral zero. A board that draws both the same way is hiding the one that matters.
3. **Sibling check, line by line, once a second surface exists.** The board, the copy review table and the people drawer each rendered a person differently (4 treatments). No audit inside one file can see that.

**Copy in Indian English:** "6h" is not read as six hours here. Use "6 hrs", "1 hr". Never mix units down a column (no "2 days" next to "12 hrs"), comparison breaks.

**Controls do not belong beside a page title when they act on the board.** Two homes already in the house vocabulary: a toolbar row attached to the board top (Timeline's chip row) for filters and view toggles; a floating dynamic pill dock at the bottom centre for actions, ONE component whose idle state and selection state share a position and shape so the eye learns one place.

**Session protocol fired and was honoured:** >8 turns, three phase changes, next ask a new workstream. Hand off at the boundary, commit the verified pass, lock decisions in the ledger, fresh session for the build.

## 2026-08-23 (evening, cont'd) — Complaint Bot Setup, two findings reverted

### "This looks like a defect" still needs the reference checked, not just my own taste
Two more review findings — a non-square logo cropped by `object-fit: cover`, an address string
that repeated its city and buried the differentiator — got real fixes: `contain` on the property
mark, a small function that dropped a redundant leading city token (and, while there, a literal
"null null" that leaked through from empty backend fields). Both were built, verified live, and
wrong to ship. The stakeholder: "Do we have it in the original property selector? If we don't, we don't
need it here as well." Checked — `PropertySider.tsx`, the exact control this picker was built
from, uses `cover` on its own rows and shows the raw address with zero cleanup. Both "fixes" were
new behavior invented on top of a component whose entire design brief was "reuse the pattern she
already learned, don't build a ninth picker." Reverted both cleanly.

**Rule produced:** before fixing what reads as a defect in a component that was explicitly built
FROM a reference, check what the reference does RIGHT NOW, not what it should ideally do.
"Improve on the reference" and "match the reference" are two different asks with two different
authors — only the stakeholder makes the first one, by naming it, not by silence. A finding that
diverges from the reference's actual current behavior needs to be named as "the reference has
this too, want it fixed there first" before it gets built anywhere.

## 2026-08-23 (evening) — Complaint Bot Setup, review + arrow keys

### The Claude Browser preview pane cannot verify anything gated on real window focus
`document.hasFocus()` is `false` in that pane. Calling `.focus()` there moves
`document.activeElement` correctly, but never fires a native `focus`/`blur` DOM event —
so a component that opens on focus (a popover controlled by `onFocus`/`onBlur`), or a
`:focus-visible`-gated style (a keyboard focus ring), reads as broken in that pane even
when the code is correct. Confirmed by re-running the identical check in a Playwright
session with a real window (`document.hasFocus()` true there) and watching both pass.

**Rule produced:** any check that depends on a real focus/blur transition or
`:focus-visible` — not just "does the element have the right attribute" — needs a real
browser, not the preview pane. `feedback_playwright-persistent-profile-for-browser-verification`
already names Playwright as the fallback for auth flakiness; this is a second, independent
reason to reach for it, and it applies even mid-session on a pane that's otherwise working
fine for everything else.

### A shared flag doesn't mean a shared rule
`effective.inherited` is `true` for both an inherited SUBTYPE (nothing of its own to copy —
it travels with its parent) and an empty CATEGORY (nothing named yet, but still a real,
selectable row). A new selection-range feature that filtered on `inherited` alone silently
dropped every empty category from a Shift+range tick. The codebase already had the correct,
narrower rule one function over (`selectableRows`: skip a subtype only, never a category) —
missed because the two computations lived in different files and were never read side by
side before shipping the new one.

**Rule produced:** before filtering on a flag that already exists elsewhere in the same
module, find every other place that flag is read and check whether they agree on what it
means for THIS shape of thing (a subtype vs. a category is not the same shape, even though
both produce the same boolean).

### A loop's own guard can silently swallow the case it exists to handle
`PageDown` computed a page size correctly, added it to the current index, and started a
`while (i >= 0 && i < rows.length)` search from there — but on a short list, one page
already overshoots the end, so the FIRST bounds check failed and the loop body never ran.
No error, no movement, nothing to notice except "the key did nothing." Fixed by clamping
the starting index into the list before the search begins, so an oversized jump lands on
the boundary instead of nowhere.

**Rule produced:** a bounded search whose starting point is computed by addition (not by
walking one step at a time) needs its own clamp before the loop, distinct from the loop's
per-step guard — the guard protects the walk, not the jump that seeds it.

### Chakra's own prop-splitting decides where a rest prop lands, and it isn't always the input
`<Checkbox data-cell-row="x" tabIndex={-1} />`: `tabIndex` (a recognized prop) reached the
native `<input>`; the unrecognized `data-cell-row` landed on Chakra's wrapping `<label>`
instead — the label the user never focuses. A keyboard grid keying off `data-*` attributes
silently found the wrong node and `.focus()` on it did nothing (labels aren't natively
focusable). Fixed with a `ref` callback instead — Chakra's own documented contract routes a
component's `ref` to its real focusable input, unlike an arbitrary rest prop.

**Rule produced:** don't assume a rest prop on a compound Chakra component (Checkbox,
Radio, Switch) reaches the same DOM node its `ref` does. Verify by reading the rendered
`outerHTML`, not by reading the component's TypeScript prop signature.

## 2026-08-23 — Complaint Bot Setup, the design pass

### "Reuse the pattern she already learned" beats "build the right control"
The copy picker was designed as a clean area-grouped list with its own segmented toggle — correct, considered, and a ninth property picker. The stakeholder: "we don't need to reinvent the wheel for something that already exists." The top bar's PropertySider was named as a reference in Phase 0 and I still built beside it instead of from it.

**Rule produced:** before drawing any surface, ask which *named reference* already answers it, and start by exporting from that file. Five `export` keywords and one extracted hook replaced 180 lines of new UI. The diff that touches the reference is the smaller diff.

### A finding about one surface is a class; name it before fixing it
"Selected rows have no space between them" → *no spacing rule for adjacent filled states*. Sweeping that class found six instances across four files; the reported one was the only one he could see from where he was standing. The references' answer (a divider that survives the tint + a control carrying selection) produced one token rule, not one patch.

### Read the type scale off the reference files; never normalise by eye
The module had 22 distinct type values including 13.5 / 12.5 / 11.5 / 19 / 10px. The references use 7. One grep over ReviewsV1/shared.tsx, SectionHeader and BlockCard gave the ramp in a minute; guessing would have produced an eighth scale.

### Chakra toasts in this app: two managers are mounted
`useToast().closeAll()` and `.close(id)` silently miss the visible card; `.update(id)` stacks a second one. The dismiss function Chakra hands to `render({ onClose })` always works — lend it to the next card via a ref with an identity check (the outgoing card unmounts after the incoming one registers).

### An effect that writes the cache it reads must not depend on that cache's freshness
`usePropertyAreaMap` depended on `isFresh`; its own success flipped it, re-ran the effect, cancelled the in-flight request before `finally`, and left the spinner up forever. Decide freshness inside the effect from the closure; depend only on the real trigger.

### "Top 1%" is a standing bar, not a per-pass reminder
He said it mid-turn as a reminder, not a new instruction. The test from the previous round stands: does the screen anticipate her question (coverage count, dock sentence) or wait for it.

## 2026-08-27 — Analytics, the systems pass

### A token with no consumers is not a system, it is a claim
A round produced a full design system for a module: a type role-table read out of the
platform twin, a bar-gradient family table, a pure numeric engine (floors, floor-and-borrow,
nice-number axis, label fit, absence handling), motion and state tokens. It was wired into the
shell — page, card, header, one block — and the commit message said "one tokens file · fixes 15
findings". The stakeholder came back with: solid bars instead of gradients, wrong font weights,
missing currency marks, missing icons. Measuring the actual consumption settled it: across the
18 files that DRAW data, the gradient table had **0** consumers, the type table **1**, and the
numeric engine **0**. Nine files were still painting a flat payload hex directly.

The findings were fixed in the file and not on the screen, and every symptom he reported was one
unwired token.

**Rule produced: creating a token layer and CONSUMING it are two separate jobs, and only the
second one is visible. Never report a token layer as landed without a per-token consumer count,
and put that count in the commit message.** The same shape as the registry rule already here — an
unregistered reusable is invisible — one level further down: an unconsumed token is worse than
invisible, because the codebase now asserts a system it does not actually run.

Cheap check, worth running at the end of any tokens pass:
`for t in TOKEN_A TOKEN_B; do echo "$t → $(grep -rl "$t" <component dirs> | wc -l)"; done`

### Fixing what was pointed at, one level down
The same round was explicitly asked to stop doing whack-a-mole, ran a 41-finding systematic
sweep, and STILL shipped the stat tiles fixed and the money-lines directly beneath them in the
same card untouched. The expansion rule is not satisfied by sweeping for the pattern; it is
satisfied by sweeping for the pattern AND then re-reading the file you just edited for the
sibling sitting three lines below the thing you changed.

## 2026-09-05 (late) — Agreement Template Library, PR 1 (kit + list) built live

### "First PR = the kit alone" was a claim waiting to happen
A kit with no consumer cannot be live-verified, and the 2026-08-27 rule says a token with no consumers is a claim. Amended at plan time: PR 1 = kit + the one screen every operator lands on. Real data then closed the mock arithmetic on its own, and exposed a second one the mock could never show.

### Two frozen endpoints, two definitions of "tenant"
The list rendered "198 of 174 tenants" on the first live load: numerator from `/agreementTemplate/list`, denominator from the home dashboard's `tenant_count`. Filed #964. **Rule produced:** on a frozen backend, a proportion's numerator and denominator must come from the same endpoint. When the list's rows partition the whole (each room and tenant on exactly one agreement), the list's own sums are the denominator, and the bars add up by construction.

### The mock cannot show the legacy shape of the data
The proposal drew `{{mustache}}` variables. Real agreements still carry pre-migration `em_*` tokens and rendered as raw text until the editor's own converter ran first. **Rule produced:** before drawing any document surface, open the oldest live record, not the newest.

### Worktree hygiene that cost twenty minutes
A fresh worktree has no `.env.local`, no `node_modules`, and (this repo) uses yarn, not npm ci. The app then calls `undefined/...` and retries in a loop that looks like a broken page. Copy `.env.local`, `yarn install`, then judge.

### The revision was locked in prose and built without a second drawing
The stakeholder rejected the built list on sight: "no header, no table, inline expansion etc - that's stupid."
The accordion stack came from a revision he approved as a direction, never as a rendered page at real
data, and it broke the house list shell (PeopleListHeader + CustomTable) that Rooms and Tenants use.
**Rule produced:** a revision that changes the container of a locked surface needs its own Phase 3.5
artifact at the real property's numbers before code. "Framing approval is not a go" applies to
revisions too. And a list page in this app starts from the list shell; deviating from it is a
decision to show, not to make.


## 2026-09-07 — seven outside resources join the bar

The stakeholder added react-spring, GSAP, anime.js, Lenis templates, shaders.com, ls.graphics and promptlibrary.org as standing resources for every redesign round. Rule produced: they are inputs to Phase 1.5 (reference) and Phase 6 (motion), routed through `references/motion-and-reference-libraries.md`, and never a reason to add a dependency without the ladder line in the ledger. Shaders draw only at Tier 3, mockups never on the app section.

2026-09-07, later: he asked whether the resources were added the way a top 1% designer would use them. They were not; the first draft was only guards. Rule: any resource ruling carries two halves, the study routine and named moves (how to use), and the ladder and tiers (where it may draw). One signature move per page.

### A narrow check that only looks for overflow is half a check
Every narrow pass in the drawn-house round was made at 500px, because `resize_page` floors there,
and all of them asked the same question: does the page scroll sideways. It never did. Emulating a
real 390px phone (`emulate` with `390x844x3,mobile,touch`) and measuring every tap target in the
one flow a renter actually uses found two controls under the 44px floor that sixteen other files in
the same kit already hold: the fourteen day chips at 37px, and the escape-hatch link at about 18px.
**Rule produced:** a narrow pass measures the interactive elements of the flow, not only the page
box, and it runs at the width of a real phone. `[...dlg.querySelectorAll('button, input, select,
a')].filter(el => el.getBoundingClientRect().height < 44)` is the whole check.

### The backend requirement is a diff, not a description
"#686, the backend requirement" turned into a useful deliverable only after the payload was read at
source for seven brands, the same houses counted in the database, and the two `select` arrays that
drop the columns found by line number. The issue's own framing (one brand, two fields, a serializer
question) was wrong on all three counts. **Rule produced:** a requirement written for another repo
names the file, the line, the exact strings to add, and the one command that proves it after the
deploy. And it names the half that is ours: the section asking for the data was not ready to draw
it, which is a second issue, not a footnote.

### A ground that looks right is not a ground that is right
The Tier 3 atmosphere shipped on a desktop screenshot I was happy with. Told to continue only if
satisfied, I went back and measured instead of looking, and found four defects the screenshot had
hidden: one of three pools never drew at all (the rules were `nth-child` and the shader is the
container's first child, so every rule was off by one), the phone got a near-flat version because
the pools were sized in `vmax` off the long edge, `will-change` pinned three full-viewport blurred
layers in GPU memory for the life of the page, and the shader kept drawing after the hero scrolled
away despite "paused off screen" being in my own budget note for the round.
**Rule produced:** after a decorative layer looks right, enumerate its elements in the browser and
assert on their computed size, position, on-screen fraction and lifecycle. A composite that looks
good can be missing a layer, and the better it looks the less likely anyone goes back.

## A number that passes against a token can fail on the screen (7 September 2026)

The kit's hero eyebrow cleared 4.62:1 against the `surface-dark` token and was actually rendering at
**4.17:1**, because the hero's ground is a decorative layer — a scrim over blurred pools that drift
for over a minute — and the pixels behind the text were rgb(31 31 34), not the token's rgb(21 21 23).
It had been shipping that way while every check said it passed.

Three rules came out of it, and they apply to any text over any non-flat ground:

1. **Hide the type before sampling the ground.** Antialiased glyph edges are intermediate colours; a
   naive pixel sample picks them up and hands you a confident wrong number. Twice in one round it
   reported a "ground" that was really the edge of a letter.
2. **Pause the animation at both ends and take the brightest pixel under the whole type block**, not
   the average and not one frame. A moving ground has no single number.
3. **Bound the ground, do not lighten the text.** No text colour can be guaranteed against a
   background that keeps changing. Then feed the measured worst case back as the reference the
   tokens are built against.

A fourth, specific to colour systems: **OKLCH lightness does not predict WCAG contrast.** Relative
luminance weights green at 0.72 and blue at 0.07, so a magenta and a green at identical perceptual
lightness differ by about 2:1 in ratio. "Fix the lightness and contrast is guaranteed" is wrong, and
only a sweep across all 360 hues catches it — the real values in the database did not.

## Look at the output before believing the extractor (7 September 2026)

A pipeline that derived brand colour from owner logos reported "34 of 44 logos yielded a hue", which
sounds like a working feature. Rendering a contact sheet of each logo beside the ramp it produced
killed it in one look: a sixth of the `logo_url` values are photographs of buildings, and the chroma
clamp collapsed five unrelated brands onto the same dusty rose. **A summary statistic cannot see
that five rows are the same colour.** For anything that generates a visual, build the contact sheet
before you build the pipeline — and check whether the data you already hold answers the question,
because 903 owners had typed the colour in by hand.

## Edit the named layer, not its frame (12 September 2026)

A request to replace childish art inside a phone mockup was misread as permission to replace the
phone composition itself. That destroyed the strongest product proof while solving the wrong layer.
**Rule produced:** before a visual edit, name and lock the frame, the editable layer and the protected
layers. "Inside the phone" means the device, position, scene and composition remain fixed. Source
screens prove capability but do not set the art direction. Premium branded surfaces also pass an
identity sweep: use the exact brand mark wherever the product or property is named, and reject
invented marks, slogans, mascots and off-tone illustration before placement.

## The states nobody rendered, and the harvest that forgot the human half (14 September 2026)

Two days on the pay.rentok.com redesign produced a clean PR and five screens nobody had ever
looked at: expired, not found, checking, failed, unsure. They existed in the code as branches, so
no gate fired on them — Gate 1 fires on a new surface, Gate 2 on a claim of done. The expired one
turned out to be what **most arrivals land on**, the most-visited screen in the product, shipped
with a 72px strip of an asset whose full version sat in the same file, and defended in a paragraph
written without opening the render. All five were found by one stakeholder question: "did you
redesign the expired page thoughtfully, or did you miss any?" **Rule produced: Gate 5, State
Census** — enumerate the branches from the code rather than from memory, force each one, look at
it, and count how many people reach it before deciding what it deserves. Sizing is what turned the
expired screen from plumbing into a design.

Three checks in the same session reported success without running: an overflow audit measured
against `window.innerWidth`, which grows to contain the overflow; six verification scripts pointed
at the port of the previous worktree; a secret scan that errored and printed "(empty = clean)",
which was then pushed on. **Confirm a check could have failed before quoting it**, and never
`scan && push` in one command.

The harvest itself then failed in a way the harvest cannot catch. Six traps and five patterns were
written, every one about the artifact, and nothing at all about the working relationship — until
the stakeholder asked what he had corrected and how we had worked, and pointed out that he had
never been told. Questions 1 to 4 all ask what the code taught you, so none of them notices that
half. **Rule produced: a fifth harvest question, the working note**, routed to the Working Contract.
Its first entries: his hedged observations ("could be just my mistake, but something feels off")
were right three times out of three and must be measured rather than answered; "why is this here?"
is a deletion question, not a request for a rationale; a ruling that inverts a default has to be
swept through every place the old default is *described*, because the PR body came one sentence
from reaching the reviewer contradicting his own decision; and "blocked on the backend" is not
permission to ship a dead end , he had to supply the WhatsApp deep-link design himself.

- 2026-09-15 | Measured a P1 bug, proved its mechanism, and was one step from
  installing the fix when a check of the issue's own comments found the fix
  already written and sitting in an open PR (#982, open 8 days, unreviewed).
  | Before building a fix for a filed issue, read the issue's comments AND
  `gh pr list --state open` for that module. An unreviewed PR looks exactly
  like unfinished work from the code side. Nearly duplicated 56 lines.
