# The expansion rule, worked

The five steps in SKILL.md are easy to nod at and hard to actually run. This is what running them looks like, taken from a real round on the Complaint Bot Setup module (Aug 2026), where the first pass failed the rule and the stakeholder called it out.

## What went wrong first

The audit produced 30 findings and read as thorough. It was still a failure, because every finding was a defect in something already built. Not one asked what the module could not do. The stakeholder read it and replied: "I think there are still a lot more issues, and I just don't understand why you take everything I say and limit yourself to that."

He was right. The audit measured column alignment with select mode off and no subtypes expanded, so it missed that expanding a subtype misaligns every column on the row. It catalogued the flat property picker as "needs a select-all" and never asked what a property list should be grouped by. It never once asked what she has to do twenty times.

## Step 1. Name the pattern

Take each pointer and write the class of mistake, not the instance.

| What was pointed at | The pattern behind it |
|---|---|
| "Selected team member rows overlap" | No spacing rule for adjacent filled states, anywhere in the module |
| "The copy picker is a flat list of 47" | The app encodes a domain model (area, group) that this UI ignores |
| "Toasts should show the person's photo" | People and places are named without their identity, in several surfaces |
| "No Select All checkbox" | The selection model is half-built, not one missing control |
| "Expanding subtypes breaks alignment" | Layout was verified in one state, not across state toggles |
| "The title is vanilla" | The room never says what it controls or that it is live |

If your restatement is the same sentence with different words, you have not found the pattern yet.

## Step 2. Sweep for siblings

The pattern is the search query. Run it across the whole module and count.

- Spacing rule for filled states: found the drawer rows with zero gap, and the selected chips whose invisible hit areas overlap across wrapped lines. Two instances, one reported.
- Identity: found four places that name a person or property with no face. One reported.
- Selection model: no select-all, no subtype checkboxes, and because subtypes cannot be selected, the copy payload can never contain one. One reported symptom, three real gaps, one of which is a missing capability rather than a defect.
- Verified in one state only: the missing `selectMode` prop on subtype rows shifts all six columns by 36px. Found by reading the props, not by looking, because the screenshot that would show it needed two toggles switched on at once.

Report the count. "You mentioned one, there are four" is the sentence that proves the sweep happened.

## Step 3. Find the internal precedent

Never design before searching the repo. The answer is usually already shipped.

- Grouped property selection already exists in `components/Home/PropertySider.tsx`, with Property / Area / Groups tabs. Reuse the model, not the 84KB component, which is built for a different job (star one property, then Apply).
- Property identity already exists in `components/Money/PropertyStickyHeaderRow.tsx`, logo ring and all.
- The sticky footer the module hand-rolled three times already exists in `ReviewsV1/shared.tsx`.

Adapt the idea. Copying the implementation is how a codebase grows four near-identical pickers.

## Step 4. Walk the workflow, not the screen

This is the step that finds what a screen audit structurally cannot: capability gaps.

Replay the job at real scale. The persona has 47 properties and about 30 complaint types. Ask what she repeats.

- Naming one person as first responder on every type: 30 trips through a drawer. The board has selection, and selection only feeds Copy. **Bulk assign and bulk hours are missing**, and they are the largest win on the board.
- Copying to every property in one area: 47 taps in a flat list, or a handful in a grouped one.
- Answering "what does Ravi handle?": impossible, because search matches type names only.

None of these are defects. Nothing is broken. They are the reason the module feels thin, and no amount of pixel fixing reaches them.

## Step 5. Come back expanded

Present, in this order: the pattern, every instance you found, the precedent you will adapt, the capability gaps, and your recommendation as the lead. Then ask for the ruling.

The tell that you did this right: the list is visibly larger than the feedback, organised by pattern rather than by the order things were mentioned, and it contains at least one item nobody asked for.

## The measurement lesson, separately

Every alignment, overflow, and truncation check runs with the state toggles ON, in combination:

- select mode on **and** a category expanded
- a filter applied **and** a long name **and** a deep row
- at partial scroll, not only at 0% and 100%
- at the width where a flexible column hits its `minmax` floor, which is where overflow starts, and is usually a common laptop width rather than the one you tested

A grid that aligns in the default state proves nothing. The default state is the one nobody files a bug about.
