# Patterns (true across repos)

Keyed by the problem. Repo-specific patterns with `file:line` live in that repo's `docs/design/PATTERNS.md`; a pattern is promoted here when it has fired in two repos.

| Problem | The house's answer | Born in |
|---|---|---|
| A surface must show many things that are "not quite right" without shouting | **Three rungs, two weights.** Silent / note (quiet line, one-tap alternative, does not hold the primary) / blocker (ring, counted, holds the primary). Never a red row, never an errors column, never a modal review. | Complaint Bot Setup import, 2026-08-23 |
| The same wrong value appears many times | **A word is global, a person is local.** A vocabulary fix applies to the whole file with Undo; a fix that names a person applies within its property; crossing the property line goes through a per-property sentence she ticks, never a blind apply. | Import, 2026-08-23 |
| She has to find the N cells that need her in a long table | **Three levels of "where is the work":** section header count (which group), column header count (which question), a walk pill (which cell, Next lands on Save). The filter alone cuts rows, not columns. | Import, 2026-08-23 |
| The product knows something she would otherwise look up | **Offer it in place, never write it alone.** Ghost chip she accepts with one tap; "12 have an obvious answer · Fill all" with Undo at the group level. | Import, 2026-08-23 |
| A list spans many properties | **One continuous scroll, one full-height section per property**, sticky section header, chevrons to jump. Never a collapse (it hides rows), never a property column (it repeats the name 20 times). | Multi-property lists; Import |
| A bulk action needs confirmation | The primary button carries the count it will do ("Save 187 · adds 2 people"); off until blockers are zero; after it, the surface stays and shows per-group result (Saved / Failed · Retry). | Import |
| Something plays out over time (escalation, retries) | **Causality, not time.** The wait is its own object on the spine; each step names the interval and the cumulative landing point; the terminus is a real row. One step = a sentence, never a ladder. | Try a ticket, 2026-08-23 |
| A control family is hand-rolled in several places | Extract on the third copy and sweep for the fourth; one height per size; register it. | Segmented, 2026-08-24 |
| A dock or tray of actions | A capsule with air inside, inset primary pill, count chip with the X inside it, no dividers, geometry derived (`PAD = (H-ITEM)/2`). | SetupDock |
| A phone is not a smaller desktop | Chrome folds: status to a dot, search to an icon, toolbar away on scroll and back on scroll-up, labels under icons, first row's y measured. | Board, 2026-08-24 |
| A chart has a bar that is not part of its run (Overdue, Never rented, No term recorded, Unknown) | **A bucket outside the run hides at zero; a bucket inside the run never hides.** Removing a sequence bar leaves a hole and the reader stops trusting the axis; removing an outside bar leaves nothing. Test: does dropping it leave a gap in a sequence? | Analytics Tenant + Inventory, D30, 2026-08-25 |
| A split renders a zero on one side | **Ask whether the zero means "none" or "not recorded".** A zero meaning none is a real answer and always shows ("no short-term tenants"). A zero meaning not recorded is an absence and the whole split hides. Same card family, opposite rules. | Analytics Stay vs Renting type, D32, 2026-08-25 |

- **Who gets told when a number changes?** Everyone whose number moves, not the one person who commissioned the note. Enumerate the people standing around the change before writing a word: on RentOk's money-model rename the brief asked for two operator notes, and the same releases moved a **staff member's** custody balance (he starts carrying UPI he has taken for years, and unannounced that reads as an accusation) and a **tenant's** deposit and total-paid, both of which go **down** when a display bug is corrected. The tenant note turned out to be the one that protects the operator, because every one of those calls lands on them. Two notes became four. **Test: for each changed figure, name every person who reads it, then check each has a note.**

- **How do we tell someone what their old figure would have been?** Usually you do not have to store it. If the change splits one number into its parts, the parts reconstruct the original, so publish the parts and show the arithmetic once on a real example rather than carrying a second historical figure on every screen. RentOk: old home Collection was collection after refunds and after discounts, and Collected / Refunded / Net Collected / Total Discount Given put it back exactly (`docs/change-map/11-operator-note.md`).

- **How do I find the errors a doc review will not?** Write the support script. Answering "what will this operator's number actually do on the day, and by how much" forces arithmetic that a change map and a release note never have to do, and the arithmetic is where the defects are. Writing RentOk's ten support answers found a P1 nobody had seen in three prior passes over the same file, and corrected a worked example in the release note that had been signed off the day before. **Any change that moves a number owes itself one worked case per affected surface, out loud, before anyone writes copy about it.**

- **How do I test a change where the correct answer is the thing that changed?** Build an oracle from the rules, not from the code, and **always include a control case chosen because nothing unusual happens in it.** The control is what separates "my model is right" from "my arithmetic happens to match". On RentOk's money model the control property agreed to the rupee across all three figures while thirteen of the other nineteen disagreed, which is the only reason the thirteen could be read as findings rather than as noise. Second rule: the test set is a **coverage set, not a sample** (one case per row, written down), because the rare cases are where the defects live: caution money existed on ten properties out of eighty thousand and carried one of the largest errors found.

- **Which real accounts belong in any test set for this codebase?** The ones whose ids are hardcoded in the source. Grep for account or tenant id literals and put every live one in the set, because those are the only places that branch ever runs and no random sample will hit them. On RentOk this surfaced four such accounts, and checking them against production also showed that one of the "three customers" with a special-cased policy is the company's own demo account and another has taken no payments in months.
- **Why does my microcopy read like a template even though every line is true?** Two habits, both invisible while writing and obvious on a read-back. First, an abstraction stands where the product already has a word ("the part already past its due date" for *bills*), which makes the reader find the referent before the sentence means anything. Second, a fact belonging to the whole block gets stamped on every row, so N rows read as one sentence photocopied. **Write, then read the rendered thing back as the user, before showing it.** Fix one: use the app's own noun. Fix two: say block facts once, on the block's first item, and repeat only where a specific label can mislead. Also check the surface can even hold a block-level line: RentOk's analytics (i) sheet is a title plus a list of items with no description slot (`src/v1/analytics/hints.ts`), so block facts must ride on item one or be moved into the definitions.

- **A long tracking doc reads like a scavenger hunt even though every sentence is plain. What is actually wrong?** Not the wording. Three structural faults, and they travel together. **(1) The action table is verbs with no objects** ("Show `fy_ytd` instead of `current_fy`") so the row only means something once you open the entry it cites, and that table is the first thing every reader is told to open. Rewrite each row to carry what is wrong, what to do, and where, so it can be acted on where it sits; the ID stays as a pointer to the reasoning, never as the carrier of the meaning. **(2) State is stored in two or three places** (the entry's own Open/Closed header, a narrative status board, the action table) and they drift the moment anything ships. Pick the place the work is done from, put state only there, and strip the mutable label from the entries; a closed entry keeps a permanent "closed by X" clause, which is a fact, not state. **(3) Nothing records when an item was last checked or against what**, so every re-check restarts from zero and costs the same as the first. Stamp the table with the commit and date it was verified against. Then sweep for siblings of the same class: an unanswered question list with no answer column reads as clean when it is un-run; unlabelled prose sections cannot be contradicted by a later finding, so number them. Worked on RentOk's 3,700-line analytics verification log, Aug 2026: front matter rebuilt, 105 entry headers stripped, 51 prose passes numbered so F106 could contradict P8 by name.

- **Which file in a docs family goes stale first, and why?** The one that calls itself the source of truth. Writing a new decision somewhere it can be acted on is always cheaper than going back to update the index, so the index is the file nobody opens and the only one that keeps claiming to be current. RentOk's analytics tracker had not been touched in nine days while 33 rulings, 108 findings and 9 suggestions were written into two sibling files it contained **zero references to**, and three of its present-tense facts were false. **Test: from the index, can you reach today's state? If the pointers all run toward it and none run out of it, it is already history and should be rewritten as history.** The fix is not an update, it is a split: the index keeps what cannot go stale (rules, and dated records of what happened) and hands live state to whichever file the work is actually done from.

- **Why do the same fact and its two copies disagree?** Because it was copied rather than pointed at, and only one copy is on the path of the work. A sheet's version number sat in the sheet's own frontmatter, in a README table and in a tracker table; the workstream that bumped three sheets updated none of the copies, so both indexes were wrong and disagreed with each other as well. **Name the one artifact that owns each fact, let at most one index copy it, and stamp the copy with the date it was checked.** Three copies is not three times the redundancy, it is two chances to be wrong.

- **How do I make a rule contradictable?** Give it a number. A body of prose rules cannot be argued with, only quoted at, so a later finding that disagrees with one has nowhere to attach and the disagreement never gets recorded. RentOk's tracker carried 40 unnumbered locked rules that were the suite's constitution; the sibling verification log numbered everything (D, F, P) and could therefore record that finding 106 contradicts pass 8 by name. **Number at the claim level, not the heading level** - a heading called "Time filters" holds four separate claims and a finding needs to point at one of them. Renumbering later is the expensive version; do it when the file is being rewritten anyway.

- **Why does a handoff repo that looks complete to me read as walls to my teammates?** Because the author can open every link in it. Before any handoff, inventory every external link (`grep -rhoE 'https?://[^)" ]+' --include="*.md"`) and sort by what gates it: permission-gated (Figma, Google Docs, claude.ai artifacts), account-gated (recordings), or machine-local (`localhost`, absolute `/Users/` paths, which are simply dead for everyone else). Each surviving link then needs two things next to it: who to ask for access, and what in the repo substitutes for it so nobody is blocked from reading. A single "Access you will need" table in the README plus one inline note per dead link beats annotating all of them. Worked example: rentok-property-onboarding README "Access you will need", commit 240ad00.

- **A superseded document was replaced by a better one. Is there anything left to do with it?** Run the comparison in the reverse direction. The obvious pass asks "what does the old doc get wrong", which only produces evidence for not circulating it. The valuable pass asks "what did the old doc raise that the new one dropped", because a replacement written from better sources still loses whatever the old author noticed and the new sources never discussed. On rentok-property-onboarding this found nine real gaps in a fact-checked description, including an entire missing entity (beds) that the Figma designs were full of. Two guards: compare against every current doc, not just the newest one (items can survive in a companion doc and look missing), and write findings to a separate queue file rather than editing the fact-checked doc, since claims from the old source have not been verified. Worked example: doc 12 in that repo, commit 410be85.
- **I have a fact-checked written record of what the team decided. Is that the whole source?** No. The design file is a second source of equal standing and it is usually ahead of the writing, because designers keep moving after the meeting ends. Writing a spec from transcripts alone produces something confidently incomplete: on rentok-property-onboarding, reading the Figma against a twice-reviewed description found three places the two flatly disagreed (a step that asks a different question than the doc says, a field that moved a step later, a conversation whose two questions are in the opposite order) and eight things the designs held that no document mentioned at all, including voice input and a whole unit lifecycle. Read the file screen by screen before writing, crop and enlarge regions rather than reading a whole canvas, pull the frame inventory once and save it into the repo, and record conflicts as conflicts rather than correcting either side, since the two sources get their authority from different places. Worked example: doc 16 in that repo, commit 0ce5cc7. 2026-08-30.
- **A stakeholder tells me the business problem. Can I anchor the strategy doc on it?** Not on the first version of it. The first answer is almost always a capacity story ("we cannot serve all the leads, not enough people"), and capacity problems are boring because you can hire against them. Keep pulling and an allocation or incentive story usually appears underneath, and that one is the real spine. On RentOk the stated problem was demo bandwidth; the actual problem was that a target-carrying sales team rationally spends its hours on the biggest lead in front of it, so the small operator is de-prioritised every day by arithmetic, and the small operator is the market. Same facts, completely different product. Test for it by asking who is NOT served and why that is rational for the person not serving them. Draft one anchored on capacity and had to be rewritten whole. 2026-08-30.
- **I found something the record never mentioned. Can I write "no document mentions this"?** Grep first, and expect to be wrong. That sentence is the most quotable line in any finding, so it propagates: on rentok-property-onboarding "no document in this repo mentions a platform fee" travelled from one finding into the phase sort, into a brief, and onto two published pages before anyone checked, and the open register had in fact been asking who bears that fee since a call two days earlier. **The true claim is almost always narrower and more useful than the absence claim** — here it was that the fee is set per package rather than once for the business, and drawn as a number the manager can type, which is a design question rather than a pricing one. Same discipline as an absence claim about a design file: structure proves a thing exists and never proves it does not. Cost: five copies to correct. 2026-08-31.

## Numbers shown side by side share a unit (eazypg-marketplace, 2026-09-05)

A stat row put "226 Rooms" next to "151 Beds free now". Readers divide adjacent numbers, and 151/226 reads as two-thirds empty when the truth was 151 of 784 beds. Every pair a reader can compare is stated in one unit, and the set is built once in a helper so three surfaces cannot drift: `packages/site-kit/src/sections/proof/helpers.js` `headlineStats(totals, brandName)`, consumed by ProofBand, ProofEditorial and HeroEditorial. Same disease as the marketplace's deposit column and rent period: a figure with nothing saying what unit it is in.

## A bento closes by shape, not by a cap (eazypg-marketplace, 2026-09-05)

A `slice(0, 4)` kept a lead-plus-four bento tidy and silently hid the sixth property, the only one with a price, while the brand copy said "six residences". Layout constraints must never leak into content. `InventoryRail.jsx` `cardSpan()` grows the lead to the rows its neighbours need (up to three), widens an odd neighbour to two columns, and flows the rest in rows of three with the last widened. No hole, no full-width banner, every item shown. Also: a content block sized by aspect ratio on the mobile rail must fill the cell at `lg` (`lg:aspect-auto lg:h-full`), or a wide cell pushes its text out of view.

## Dedupe across the lists a reader sees together, not within each (eazypg-marketplace, 2026-09-05)

Three amenity lists were each deduped on their own, so "Common gym" and "Gym", "Common parking" and "Parking", "High-speed wifi" and "Wifi" each appeared twice on one screen. The unit of deduplication is what the reader sees as one list, not what the backend stores as separate arrays. `packages/site-kit/src/sections/amenities/helpers.js` `amenityGroups()` dedupes the concatenation in group order and hands each survivor back to the first group it appeared in, and every amenity variant reads it, so the rule cannot drift per variant.

## An `<input>` inside a grid pushes the column out

HTML gives an `<input>` a default `size="20"`, so its intrinsic width is twenty characters — 670px at a display font size. A grid with no `grid-template-columns` gets an implicit `auto` column whose minimum is the item's min-content, so the column sizes itself to the field and takes the document with it.

`min-width: 0` on the input does **not** fix it: that lets the *field* shrink and says nothing about the *column the field is measured into*. The fix goes on the grid: `grid-template-columns: minmax(0, 1fr)`.

Any grid containing a form control needs it. When a page scrolls sideways for no visible reason, grep for `display: grid` without `grid-template-columns`.

## Terminal states are one component, with the words as the difference

"Link expired" and "link not found" are the same moment: she decided to act and the thing she tapped cannot do it. Two screens, one component, a copy map keyed by cause. The next terminal state is then a copy entry rather than a screen.

The corollary: a terminal state still needs a route out, and the route must be the one thing that actually resolves it. Six expiry references (Meta Quest, Binance, Grab, PlayStation, Chipotle, Ubank) — five end in "OK" or "I understand", a button that acknowledges the system's problem and returns the user to nothing. Only two offer a way forward.

## A split action dock is for actions; a caption fights it for a column

A two-column dock (primary key + secondary link) is a split between two *actions*. Putting an explanatory line in it makes the line compete for a column and wrap. Give the single-action case its own modifier with one column and the caption beneath, and double the class in the selector (`.dock.dock--solo`) — one class against one class is resolved by source order, not by intent.

## Screen-reader-only text is clipped on purpose

A 1px box with `clip-path: inset(50%)` is the visually-hidden idiom, and a geometry audit will report it as clipped text on every route for ever. Exclude it by the **technique** (`clip-path` set and `clientWidth <= 1`), never by class name, so the next one is covered without anyone remembering.

## On a money surface, absence renders as absence

`const amount = Number(payment?.amount) || total` is a lie generator: `Number(null)` is `0`, which is falsy, so a missing figure silently becomes the fallback. On a receipt that printed the tenant's entire outstanding as the sum she had just paid, sealed, with a real reference.

Fixing the call site is not enough — the default at the destination swallows it. Make the value nullable and have every print site omit it. A receipt may show less than it knows; it may never show more.

## A step she can be on is a step with an address (eazypg-marketplace, 2026-09-14)
**Problem.** A step inside a screen held in component state looks identical on screen and is invisible to every render check, but it has no address. Her phone's back skips past it to whatever came before, a refresh throws away what she had done on it, and she cannot return to it or share it. On the payment page the cash step was `useState`, so the URL read `/pay` while the screen said "Pay in cash": back went to the bill rather than the amount screen, and a refresh lost the collector she had picked along with the code already sitting on his phone.
**The house's answer.** Derive the step from the query and push it shallow, so the step has an address, costs no refetch, and leaves the figure she typed and the lists already on her phone alone. `pages/_sites/payment-pages/p2/[shortId]/pay.js:210` (`const cash = q.how === 'cash'`), pushed at `goCash`.
**The tell.** The same screen reachable two ways, one with a URL and one without. That is one screen with two entrances and only one exit.

## A detail route destroys the list it was opened from (eazypg-marketplace, 2026-09-14)
**Problem.** Opening a record swaps the branch that renders the list, so the list component unmounts and every piece of state it held is gone. Coming back she gets the DEFAULT arrangement, which looks right, so no screenshot, no render check and no console ever shows it. On the payment page: read receipts, print the other seven, open one, press back, and she is on the bills tab with the list shut.
**The house's answer.** The page owns the arrangement and keeps it in the address, carried through record opens by one named list. `pages/_sites/payment-pages/p2/[shortId]/index.js` (`KEEP`, extended from preview switches to `tab` and `rows`), `components/PayPage/Receipt.jsx` (takes `tab`/`rows` as props, holds no state at all now). Arranging is a `replace`, so her back key stays about the records she opened rather than her tab taps.
**The tell.** A control whose effect disappears after a round trip you did not think of as navigation.


## Restyling a CustomTable column header (2026-09-15)

**Problem.** A redesigned list needs sentence-case grey headers on white, and
`components/Common/CustomTable/CustomTable.tsx` hardcodes all of it: the `Th` at
`:360` sets `bg="#f0f3ff"` and `color="gray.600"`, and Chakra's `Th` theme
default adds `text-transform: uppercase` at `xs` with wide tracking. `Th` is
every list in this app, so editing it is not available.

**The house's answer, in two halves.**

*Text* comes from the column's `header` render function, as a child with
explicit overrides — `textTransform` is inherited, so it must be named:
```tsx
const Head = ({ children }: { children: string }) => (
    <Text fontSize="12px" fontWeight="500" color="#696969" textTransform="none" letterSpacing="0" whiteSpace="nowrap">
        {children}
    </Text>
)
// then: header: () => <Head>Covers</Head>
```

*Background* cannot come from a child, so it needs a prop. Add an optional one
defaulted to the current literal, which makes the blast radius provably zero:
`headCellBg` on `CustomTable`, default `#f0f3ff`, spread at `:360`.

**Two dead ends, both of which look like the answer.**

- `shouldHighlightColumn={() => true}` + `columnHighlightColor="white"` does
  give a white header row using only existing props — and then destroys the
  screen, because `isColumnHighlighted` is tested BEFORE `isHighlighted` on body
  cells (`CustomTable.tsx:545`). Every cell goes white and the highlighted row's
  tint disappears. On a board whose pinned Default row IS the design, that is the
  one thing you cannot lose.
- `headerBg` reads like the prop for this and is dead: declared `:108`,
  defaulted `:158`, never used. Six consumers pass it and all six are ignored.
  See #999; do not wire it as a side effect of unrelated work, because it changes
  four modules' screens at once.

**What cannot be done this way.** A border on the header cell — for a first-column
divider that runs through the header the way the gold board's does. Set from the
`header` renderer it lands on the `<p>`, and `CustomTable` wraps header content
in a row `Flex` beside the sort arrows, so the `<p>` takes its CONTENT width: the
rule draws at the end of the word, reading as a box around the label. Either
accept the notch at the top of the rule or add a prop for it too.

## Three copies of one notice, and how to tell (2026-09-15)

**Problem.** A module shows the same warning on several screens and there is no
component for it, so each screen hand-rolls the markup. They do not stay the
same. Measured across the agreement module on one afternoon:

| | detail | editor | add flow |
|---|---|---|---|
| background | `#FFFBEB` | `#FFFBEB` | `#FFF8E8` |
| border | `#FDE68A` | `#FDE68A` | `#F0C36D` |
| icon | triangle 15px | triangle 16px | none |
| title colour | `#7B4B08` | `#7B4B08` | a token |

Nobody chose that. It is what three copies do, and no screenshot of any ONE
screen shows it — the defect only exists in the comparison.

**How to find it without luck.** Grep the shared *string* function every copy
calls (here `literalWarning(`), not the markup. Each render site is a copy:

```
grep -rn "literalWarning(" components/<module>/*.tsx
```

Then diff their colours. The same trick finds duplicated empty states, error
cards and confirmation bars.

**The house's answer.** One component in the module's kit, colours from tokens,
and the only props are the things that genuinely differ between the screens —
here `maxW` (the detail page's notice belongs to the document's 820px column,
not the page's) and an optional `action`. Everything else is fixed, so the
copies cannot come back.

**What NOT to fold in.** The same sweep turns up other hardcoded ambers that are
a DIFFERENT job. `REVIEWS_COLORS.starAmber` (#F0A429) is a mark — icon, tint,
border. `#B7791F` is ink, dark enough to read as body text; #F0A429 on white does
not clear 4.5:1. Swapping one for the other in the name of consistency is a
contrast regression. Check the hue's job before you unify it.

## Giving structure to a document you do not control (2026-09-15)

**Problem.** A screen renders customer HTML — a contract, a policy, a pasted
Word document — and it is long enough to need navigation, but it has no
headings. Measured on a real agreement: 220 `<p>`, zero `<h1>`/`<h2>`/`<h3>`.

**The house's answer.** Read the convention the document actually uses rather
than the markup it lacks. In these contracts the sections are the short lines
typed in capitals ("MEMBERSHIP AGREEMENT", "4. MEMBERSHIP FEES; PAYMENTS"), so
`documentOutline` anchors those and the rail lists them.

**Build it to refuse.** A heuristic that is confident when it is wrong is worse
than no feature. Three guards, all in
`components/Settings/AgreementTemplateLibrary/documentOutline.ts`:

- `MIN_SECTIONS` — under three, a rail is furniture.
- `MAX_SHARE` — if more than ~35% of paragraphs are capitalised the whole
  document is shouted and every line would become a heading.
- tables are excluded before anything is counted: a contract's tables are full
  of short capitalised cells that are column headings, not sections. Skipping
  this put seven pieces of furniture in an 11-section rail on the first render.

On refusal it returns `entries: []` **and the html untouched**, so the caller
renders nothing and the page is exactly what it was.

**Two things the first render taught, both cheap to repeat:**

- Sentence-casing a heading in CSS does not work. `::first-letter` capitalises
  the first CHARACTER, so "4. MEMBERSHIP FEES" becomes "4. membership fees" —
  the digit gets capitalised and the word does not. Transform the string.
- Decorating rendered HTML (marks, chips, anchors) must split on tags and only
  ever touch text runs, or a value lands inside an attribute. `swapLiteral` and
  `markLiterals` both do this; copy the shape.

## Form errors: at the field, never in a bottom toast

**Problem.** A screen with a sticky action bar validates on save and reports the
problem in a toast. Chakra's default toast position is bottom-centre, which is
exactly where the sticky bar is, so the message physically covers the button it
is telling her to press. Captured at 1440 on
`/settings/first-party-agreement`: the toast sat on top of "Also apply to other
properties".

**The house's answer.** Put the message on the field, set `isInvalid` so the
control rings, and take her to the first one. No toast for validation at all;
toasts stay for outcomes she cannot see (saved, failed), not for problems that
have a visible home.

`components/Settings/OwnerAgreementDetails/OwnerAgreementDetails.tsx`, in
`persist()`:

```ts
if (missing) {
    setShowErrors(true)
    requestAnimationFrame(() => {
        document.querySelector('[aria-invalid="true"]')?.scrollIntoView({ block: "center", behavior: "smooth" })
    })
    return false
}
```

`aria-invalid` is what Chakra's `FormControl isInvalid` already writes, so the
scroll needs no refs and no per-field wiring, and it keeps working as fields are
added or reordered.

**The precondition people miss:** `FormErrorMessage` renders nothing unless its
`FormControl` has `isInvalid`. This screen shipped for years with five of them
in the markup and `isInvalid` set on none, so six required fields shared one
toast that named none of them, and the dead markup read as working validation.
Grep for `FormErrorMessage` without a nearby `isInvalid` before trusting a form.

## Front-of-document edits, back-of-document rot

**The problem.** A ruling lands, and the person applying it rewrites the part of
each document where the ruling obviously belongs, usually the top. Every
sentence further down whose meaning depended on the old answer is left standing:
open-decision rows that say "open" about a closed question, build briefs written
on the old premise, field tables carrying the old single value, and status lines
claiming work that was not done.

**Why it multiplies.** When a suite of documents shares one shape, one missed
sweep is not one error, it is one error per document. Ten handoff sheets sharing
a six-part shape produced the same failure ten times.

**The house's answer, in order.**

1. **Write the ruling into the document that defines the shape first**, the
   inherited page and the template, before any sheet. Otherwise every sheet
   inherits the old version and the correction has to be made n times.
2. **Sweep the adjacency sentences**, the ones whose meaning is positional:
   "the next step", "two screens apart", "having just ticked", "when she
   finishes", "hands over to". A reorder invalidates every one of them and none
   of them contains the word that changed.
3. **Sweep the tables that index the prose**, which is where the rot hides:
   decision rows, field tables, work lists, small-fix lists.
4. **Then read each file end to end**, or have someone else do it. Steps 1 to 3
   are greps; only a read catches a brief that quietly asks engineering to build
   what the ruling removed.

## A heuristic that refuses correctly can still produce a broken-looking result

**Problem.** `documentOutline` builds a contents rail from a contract that has no
`<h*>` tags, by finding short capitalised lines. On a real contract it rendered
**3, 4, 5, 7, 8, 9**. Section 6 was there — as one ~200-character mixed-case
paragraph, `"6.    HOUSE RULES in addition to any rules, policies and/or
procedures ..."`, because Word ran the heading into its own body text.

Every rule behaved correctly. `MAX_HEADING_LEN` and the all-caps test both
rejected it, exactly as designed. And the output was still wrong, because a
contents list with a numbered hole in it reads as broken no matter how defensible
each omission was.

**The house's answer.** When a heuristic's output carries its own evidence of
completeness — numbered sections, a sequence, a running total — check the
OUTPUT's coherence, not just each decision. Then widen the rule for the one
unambiguous shape rather than loosening it generally:

`components/Settings/AgreementTemplateLibrary/documentOutline.ts`, `runOnHeading`:
a number, a dot, then a run of capitals, stopping at the first lowercase word.
Title-case run-ons stay rejected on purpose, because catching those needs a rule
loose enough to promote ordinary numbered clauses into the rail, and **a wrong
rail is worse than a short one**.

**How to catch it without the screenshot:** any heuristic whose result is a LIST
the user reads as exhaustive deserves a coherence assertion, not only per-item
ones. Here that is "the numbered entries have no gaps"; elsewhere it is a total
that must match, or a set that must cover.

## Given a sentence, which frame is it on?

**Problem.** Handoff sheets quote drawn copy and then drift, because nothing in
the document can be checked against the design file. `get_metadata` answers
"what is on this node"; nobody had the reverse index.

**The house's answer.** Build one flat digest per canvas, one block per
top-level frame holding its id, its name and every text layer inside it, then
grep the digests for the sentence. Scripts live in
`~/rentok-property-onboarding/tools/`: `index.py` builds a digest from a saved
metadata dump, `look.py` searches all digests, `where.py` prints the ancestor
path of a match, `verifyids.py` checks that every id a document cites still
exists.

**Nine sheets went from unfalsifiable prose to cited claims in one pass**, and
it caught a whole screen recorded as empty that is drawn and full.

**Do not use it to prove absence.** Component overrides are invisible to a name
search: a card's *RentOk ID: 1220096612B* sits on a layer named `Rent Label`.
NO MATCH means render it, not that it is missing.

## "How do we verify the reasoning?" — sort claims by what could falsify them

**Problem.** A copy audit can be driven to zero and the document can still be
wrong, because copy is a small share of what a design document asserts.
"Verify the reasoning" is not actionable as stated.

**The house's answer: stop treating a document as one body of prose and sort its
claims by what could prove each one wrong.** Four kinds, four different checks:

- **DRAWN**, what is on a screen → the design file. Frame id, then a render.
- **RULED**, what the decision-maker decided and when → the ruling record. Every
  dated citation must land on a date the record carries.
- **TODAY**, what the shipping product does → the repos. Requires a `file:line`.
- **OURS**, product reasoning → nothing mechanical. A person, or the owner.

**The value is not in the three checkable kinds. It is that the fourth becomes a
counted, visible set** instead of being mixed invisibly into everything else.
You cannot automate judgement, but you can stop judgement from hiding among
facts.

**Two sub-classes deserve their own counter.** **Negative claims** ("nothing is
drawn for this", "no screen exists") are the most dangerous, because a name
search cannot prove absence: one such claim recorded two fully drawn tabs as
empty. And **live-product claims** are the most expensive to get wrong, because
engineers act on them: one said Apple sign-in was mandatory when the app hides
Google on iOS deliberately to stay exempt.

Implementation: `~/rentok-property-onboarding/tools/claimaudit.py`.

## A borrowed list header wired halfway

`components/Common/peopleListHeader.tsx` folds its filter row away while the
table scrolls, through a ref handle the table reports into. The template library
wires it (`TemplateLibrary.tsx`: `headerRef`, `onScroll={... handleTableScroll}`).
The add flow's room picker used the same header and never wired it, so on a
phone five filter chips sat on three rows above the table for good and the first
room started near y=600 of 812.

**The house's answer, for any screen that borrows this header:**

1. Pass `ref={headerRef}` and `onScroll={(t) => headerRef.current?.handleTableScroll(t)}`
   on the table.
2. On a phone, `showFilterDrawerQuickFilters={!isNarrow}` — just the Filters
   button; every filter stays in the drawer.
3. If the title is a question, `reflowHeaderOnNarrow` + `titleWraps`, and keep
   `rightComponent` for md+; on a phone put the actions in `filterContent`.
4. Fold wide columns into the name cell below md.

Test: at 375 the first data row should start well inside the top half, and every
action the header shows on desktop should be on-screen.

- **A ruling asked about one door holds at every door doing the same job** (property onboarding, 16 Sep 2026). A question framed as "at Add Tenant" was really "whenever a person is put into a room": booking placement, room moves, bulk add, sheet upload, the assistant's suggestion. Before recording a ruling, list every entry point that does the same act and write the ruling against all of them; bulk paths get one gathered confirmation, never one prompt per row.

## A shared control that is too small: grow its reach, not its box

**Problem.** `SubPageHeader`'s back button was 40px on eight screens. Drawing
it at 44 fixed the tap finding and created a new one: every consumer puts 40px
actions in the same row, so the row gained a height mismatch
(`/property/reviews/schedules`, both widths).

**The house's answer.** Keep the drawn size, grow the hit area with
`tapArea(controlHeightPx, x)` from `components/Property/ComplaintSetup/tokens.ts`
(an invisible `::after` inset). `run_probe.py` measures that reach, so the tap
finding clears and nothing in the row moves.
`components/Property/ReviewsV1/shared.tsx`, the back `IconButton`.

**How to know which one you need:** probe one consumer of the shared control
with the change stashed and again with it applied. A new `[height]` finding
means the box grew where only the reach should have.

- **One screen, many doors: the door decides the scope (17 Sep 2026).** A picker or form reached during setup, after setup inside one property, from an all-properties list, and for a second property must say per door what is preselected, hidden, counted, and where she lands after; plus the one-property and limited-team-member cases. Precedent: the live package form asks for a property only when she has more than one, `rentokmanagerflutter lib/money/duepack/addeditpack/add_new_category2.dart:394-396`. Worked map: rentok-property-onboarding `audit/context-map.md`.

- **Handoff sheets carry history at the end, not inline (17 Sep 2026).** Inline strike-and-bold corrections made fresh readers rate sheets "slow" or "lost". Keep parts 1-7 as current truth; move struck text and check dates to a final "How this sheet changed" part; prove nothing dropped with a before/after inventory (rentok-property-onboarding `tools/inventory.py <before> <after>`, prints "0 items lost").

- **Filtering a parent by its children (2026-09-18, rental options).** When a parent (rental option) is found through its children (rooms, flats), a filter matches the parent only when ONE child satisfies every ticked value at once, and the result says how many children match. Matching on the combined set lets "AC and vacant" return an option whose only free room has no AC. The parent screen shows the combined list as "in every unit" and "in some (n of m)"; public surfaces claim only the first.

- **A brand icon set from the owner's own mark.** Problem: library icons make an owner's site read as anyone's. Answer: one grid and stroke, plus one signature taken from the brand's own mark, checked against the record before it is claimed (Vilaasa: the wordmark's yellow window, drawn from the Fortune and Elite window frames because the owner has no logo; Meridian: its spiral house mark from the owner's logo). Premium means thin and plain: a 1.4 line, thinner at large sizes so it looks the same weight, no tiles or fills, and any accent inside its shape (a floating accent reads as a stray pixel). A 1.9 line with outlined accents and pale tiles read as clip art. Render a specimen of every icon at 24 and 48 on every ground the page uses before placing any; it caught an icon whose accent read as a person. Example: rentok-site-factory/runs/vilaasapg/pages/home/directions/icons.mjs and specimen.mjs.

- **"Does it stay with her?" is measured from the middle of the page (20 Sep 2026).** Problem: whether the price and the ask follow the reader decides how a decision page feels, and reading `position: sticky` off the DOM at the top of the page answers a different question (a bar can be absent until she scrolls, and a sticky ancestor can hold something she never sees). Answer: scroll to half the document, wait for a paint, and collect every fixed or sticky box that intersects the viewport and carries text, then ask of that set whether any holds money and whether any holds the ask. `rentok-site-factory/runs/vilaasapg/site/refs/read.mjs` (the `pinned` probe); results in each `<site>/measure.json` under `viewports.<w>.pinned`. It separated the ceiling from the category cleanly: Cohabs and Inigo keep the number with her, Cove and Meridian do not, and neither do we.

## A bench route beats a mockup, and it finds things a mockup cannot

Problem: a sheet or state that no real account can reach — ten discounts, one capped, one worth
more than the payment, a 348-character note — never gets looked at, so it ships unseen.

The house's answer: a preview route behind the page's existing preview gate, with the cases built
as data and chosen from the URL rather than from a control (a modal dialog swallows pointer events,
so any switcher drawn behind it is unreachable). It renders the real component against the real
stylesheet, so a screenshot of it is evidence, not an impression.
`pages/_sites/payment-pages/p2/preview/discounts.js`, beside the existing `preview/skyline.js`.

What the first render caught that neither the code nor a hand-drawn mockup could: a translucent
"set aside" card let the tray's ribbing read through the paper; one copy string was printed against
every credit she owned whenever a big one swallowed the payment; a group heading promised the wrong
remedy; and a capped credit showed a face value we would never honour in three of its four states.
Four real faults, none visible in the diff, all visible in one screenshot.

Measure the render, do not eyeball it. The check that mattered was one line: collect the left edge
of every amount and assert the set has size one. That is the ledger property the whole design was
argued on, and it is now a number instead of a claim.

- **One decision, one threshold (20 Sep 2026).** When a panel and the control that opens it are gated on two separately written conditions, they drift and one of them ships alone. Vilaasa: the house-rules dialog rendered above 3 rules (`runs/vilaasapg/site/src/modules/living.mjs:37`) while its button rendered above 6 (`:25`), and eight of the eleven houses have exactly 6, so 8 of 11 pages shipped a fully populated dialog nothing could open. Compute the condition once, name it, and let both the trigger and the panel read that name. Worth checking as a class on any surface where content and its opener are built in different functions.

## Measure the type, do not judge it

Problem: "the letter spacing and line height look off" is true far more often than an eye can
localise, and a design review that answers it with taste produces another round.

The house's answer: a probe that reads the page's own tokens at runtime and reports every visible
text node with size, leading, tracking, tabular setting, contrast and touch-target height.
`scripts/paypage/type-probe.mjs` in eazypg-marketplace; run it against a served URL.

Two rules it encodes, both of which cost a round here:
- **Negative tracking belongs to words, not to figures.** Tabular numerals are drawn to one fixed
  advance so money lines up in a column; -0.04em at display size crowds every pair and throws that
  away. Flag `tabular && contains-digits && tracking < -0.015`.
- **Leading below 1 clips a comma.** A grouped figure has a descender, and a rule or underline
  beneath it lands on top of the descender at line-height 0.95.

And one rule about the probe itself: **flag only what is wrong.** The first version flagged every
element on the page as off-scale (it read the tokens from the wrong element) and every heading as
tight (it did not check whether the text contained digits). A checker that cries wolf is ignored,
and then the real finding underneath it is lost.

## A resting sheet must survive its content arriving late

**Problem.** A bottom sheet whose height or resting point is measured at open, over a list fetched
after mount. Two independent failures, both silent, both invisible on a bench where the data is
already there: measuring straight after `showModal()` reads the page before layout, and the opening
glide finishes honestly against the *empty* list, so when the rows land a `scroll-snap-type:
mandatory` scroller re-snaps to a different point and emits no scroll event to react to.

**The house's answer.** Measure inside a double `requestAnimationFrame`, and re-settle from the
panel's own `ResizeObserver` gated on whether the user has touched the sheet, never on "is it still
opening". `components/PayPage/Drawer.jsx` (marketplace paypage) carries all three: `touched` ref set
from pointerdown/touchstart/wheel/keydown, `settleOpen()`, and a `settle` that ends the glide only
when scrollTop is within 2px of the *current* peek.

**Also.** A sheet whose job is its relationship to something behind it takes a selector, not a
percentage: `below=".pay-stamp-fig"` means "sit under that and take what is left". A fixed share
cannot express it and breaks at a different viewport height in the other direction.

## A sticky sheet head cannot depend on the panel's gap

**Problem.** Pinning a bottom sheet's title so it survives scrolling. The obvious build is a sticky
bar for the grip with a negative bottom margin cancelling the panel's grid `gap`, and the title
sticky beneath it. That gap is not the same on every sheet — in `pay-page.css` the discount sheet
sets `gap: 0` — so the cancellation over-pulls and the title's ascenders render under the bar.

**The house's answer.** The title carries the band and the grip sits on top of it: title `position:
sticky; top: 0` with symmetric `padding-top` / negative `margin-top` (so it costs no height at
rest) and the panel's background; grip `position: sticky; top: <padding/2>` at a higher z-index.
Depends on nothing outside itself. `public/paypage/pay-page.css`, `.pay-drawer-grip` /
`.pay-drawer-panel > .pay-drawer-title`.

**Probe it by the text, not the box.** A padded sticky title's `getBoundingClientRect().top` clears
the grip while the glyphs do not; measure `rect.top + parseFloat(getComputedStyle(el).paddingTop)`
against the grip's bottom.

## An image revealed by `onLoad` never appears on a server-rendered page

**Problem.** `const [ok,setOk]=useState(false)` with `<img onLoad={()=>setOk(true)}>` and
`opacity: ok?1:0`. The `<img>` ships in the SSR HTML, the browser finishes it before React
hydrates, and the load event is gone before the handler exists — so the photo sits at opacity 0
behind its fallback on the first screen and on every reload, and appears only after a client-side
navigation, where React creates the element itself. Reported by the founder as "the DP loads only
if I go to another screen and come back".

**The house's answer.** `components/PayPage/Machine.jsx`, `Mark`: a ref on the img and
`useEffect(() => setOk(Boolean(el?.complete && el.naturalWidth > 1)), [src])` alongside the
handler. `complete` is the state the missed event would have reported; `naturalWidth > 1` keeps a
404 on its fallback. Applies to any lazily-revealed media, not just avatars.

**Probe it across all four entries**, because two of them pass: first land (SSR), client
navigation, back, hard reload. And read the *computed* opacity with ancestors multiplied — the
element has a full-size box at opacity 0, which is what hid this from my first two checks.

## A polling loop must announce that it gave up

**Problem.** A component starts in a "loading" state and leaves it only when the awaited thing
arrives. The parent polls a few times and `return`s silently on exhaustion, so the component is
never told the waiting is over and the control stays disabled for the rest of the session. Worse,
a second mount of the same component where nothing is being fetched at all starts in that same
loading state and spins with no poller behind it.

**The house's answer.** Three states, never two: ready / awaiting / none, with `awaiting` passed
IN by the parent — it is the only one that knows whether anything is still coming — and the loop
setting it false on both exits. `components/PayPage/Paid.jsx` (`awaiting` prop) and
`pages/_sites/payment-pages/p2/[shortId]/index.js` (`chase`, `hunting`).

**Then design the terminal state as a real one**, and look for it in the same file first: the cash
path here already had the right shape (a pressable key plus a true sentence), so the give-up case
reused it instead of inventing a variant.

**Check the frequency before calling it an edge case.** This one looked rare and was not: 31,519
paid bills in 90 days have no file, and six of seven receipts on the test tenant. A "loading" state
that is actually the common ending is a broken screen, not a nicety.

## Proving an outbound payload without touching production

**Problem.** A money-path fix is "forward one more field to the backend". Reading the diff is not
proof, and calling the real endpoint to check would send a real OTP or write a real payment.

**The house's answer.** Point a throwaway dev server at a local echo. A ~15-line `http.createServer`
that logs each request body and answers with the shape the route expects, then
`NEXT_PUBLIC_ENDPOINT=http://localhost:3098 npx next dev -p 3099` (Next does not override vars
already set in the shell, so this beats `.env.local`), then `fetch` the route from a small script.
The echo log is the proof, and the developer's own server on its usual port is untouched. Run both
branches — the field present and the field absent — because "sends an empty string" and "omits it"
look identical in a diff and are different to the receiver.

**Note:** in this harness `curl`/`wget` are redirected by a context hook; use `fetch` in a node
script instead.

- **A grouping key is not an entity (22 Sep 2026).** RentOk's room list groups by flat on both clients (`lib/property/room/room_provider_v3.dart:1003-1040`, `components/Property/Rooms/roomHelpers.ts:62-66`), so a flat looks present while nothing about it can be priced, let, published or filled. Before claiming a product "already has X", check whether X is a row people act on or only a header the list sorts by.

- **Enumerate states from the product's own vocabulary, not your own list (22 Sep 2026).** My first states board had twelve cases I thought of. The backend had twenty filter codes and already sends per-card status tags (`src/v1/constants/filterCodes.ts:135`, `src/v1/list_screens/rooms/helpers.ts:1383-1390`), the wiki had PROP-017 to PROP-027, and DA-08 had the occupancy definitions. Six real cases were missing, including unpaid dues and available-from. Before drawing states, pull the enum, the filter sheet and the widget list; they are the product's own answer to "what can this be".

- **A sheet that announces something must open whole.** Drawer.jsx opens a tall sheet at 62% of the screen with the grip saying "more"; for a sheet whose key is the point, pass `peek={0.9}` and keep the content short enough to fit 667px (AutopayCard.jsx LaunchSheet, 23 Sep).

- **Count distress in the unit she feels, and run it on the real record first.** Problem: "hold the promo when she has 3+ overdue bills" counted one month's rent, power and food as three and would have hidden the sheet from a tenant one cycle late, its best audience. Answer: count distinct months past due (`launchWaits`, eazypg-marketplace components/PayPage/autopay.js, end of file), then check the rule against the live test tenant's `pending_dues` before trusting the unit test. (23 Sep 2026)
