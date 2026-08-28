# The Designer's Gates

**Who this is for.** The agent acting as the design lead, and the humans who work with it: product managers, engineers, anyone with product knowledge. The agent leads the design; the human guides, corrects, and decides. The goal is work that a top product designer at Airbnb, Apple, Stripe, Linear or Notion would put their name on.

**Why gates and not rules.** Every rule below already existed somewhere as prose before the session that produced this file, and it still got broken. Knowing a rule was never the gap. The gap was the moment it gets applied. So these are checks tied to a moment in the work, and global hooks fire them at that moment whether or not anyone remembered. A rule you have to recall is advice. A gate you have to pass is a standard.

Four gates, one contract, one probe. Everything else is in the skill.

**Enforcement is not automatic on install.** These gates fire because two hooks are wired into `~/.claude/settings.json` — a per-machine file a skill cannot write on its own. Set them up once with `references/hooks-setup.md`, or this file is rules again, not gates.

---

## Gate 1: Surface Ready (before the first line of code on any surface)

A surface is anything a person sees and acts on: a page, a modal, a drawer, a dock, a toolbar, a toast, a popover, an empty state, a footer. **"Small" is not an exemption.** The rejected build that produced this gate was a modal. The next one was a footer.

A surface is ready to build only when all seven are written down and the stakeholder has seen them:

| # | Question | What a passing answer looks like |
|---|---|---|
| 1 | **What IS it?** One sentence, a noun. | "An escalation ladder that plays out." Not "a modal with a list". If the sentence describes the layout instead of the thing, it is not an answer. |
| 2 | **What question did she come with?** | "Who actually gets it, and what happens if nobody picks it up?" The surface exists to answer it. Point at the element that answers it. |
| 3 | **Where is the internal precedent?** | The screen in this product that already solved the shape. Name the file. Adapt the idea, never paste the implementation. If none exists, say so explicitly. |
| 4 | **What did you pull from outside?** | Two or more real references from real products, with the single idea taken from each, in one line. Search Mobbin before designing, not after being asked. |
| 5 | **What are the two directions?** | Two genuinely different answers, rendered so they can be looked at, not described in prose. A playback cannot be judged from a still. |
| 6 | **Which one, and why?** | The lead's pick with a reason the stakeholder can disagree with. Never a neutral menu. |
| 7 | **What is wrong with the spec?** | The grid, the lock, the brief: what does it get wrong or leave out? A spec that says "three rows of chips with a time beside each" can be built perfectly and still be rejected. Say it before building. |

**Two rules that older rounds paid for.**
- **The drawing wins over the prose.** The copy conflict step was built as a stack of cards while the artifact and LOCKS §7 both said "type as section, property as row". Open the drawn artifact before building, not the paragraph that summarises it. Gitignored artifacts never show in a diff, so they get forgotten.
- **Built FROM a reference? Check what the reference does today before "fixing" it.** Two real fixes (logo crop, address order) were reverted because the picker they were built from, `PropertySider`, does neither. "Improve on the reference" and "match the reference" are two different asks with two different authors. Name it as "the reference has this too, fix it there first?" before building it anywhere.

**The feeling test, before the seven.** When the stakeholder describes what they want, find the feeling under the words before answering the words. "It is a journey with moments" was said three times before it was heard as *causality, not time*. If the first restatement did not land, the second attempt should change the frame, not the wording.

**The hook.** Creating a new component file fires this gate. If the brief exists and was approved, proceed. If not, stop and write it.

---

## Gate 2: Done Probe (before the word "verified" or "done")

Nothing is done on a claim. It is done on numbers, taken on a real page, at two widths: **375 and an explicit 1440.** (The preview pane's "desktop" preset is 800px, which is below the `lg` breakpoint. Twice in one session "verified at 1440" was verified at 800. Set the width by number.)

Run `scripts/ui-probe.js` (see below) and paste its output into the commit message. The probe reports:

| Number | Why it exists |
|---|---|
| **First content row's y on the phone** | Half the screen was chrome before she saw a single row (y=419 of 812) and nobody measured it. One number would have caught five findings. |
| **Height and centre line of every control in a toolbar row** | Two controls in one row measured 34px and 28px on centres of 184 and 187, with the title on a third centre at 189. Nobody could name it; everybody felt it. |
| **Sticky cells' x before and after a sideways pan** | A sticky column slid 56px before pinning, then sat on top of the tick column. |
| **Sticky cells' height against their row's height** | A sticky Type cell masked only its own 24px of single-line content; the People cell beside it wrapped to two lines and showed through above and below it. Found by the stakeholder on his own phone: "what the heck is this?" |
| **Every open popover: portaled, inside the viewport, gutter** | Cards rendered inside the scroller were clipped by it; on a phone one sat flush at 375 of 375. |
| **Icon widths inside buttons** | Every icon in a tray rendered at 0px. `minW: 0` lets a flex child shrink to nothing and the SVGs go first. |
| **Flex siblings that resolved to different widths** | `flex: 1` on every action inside a content-width container does nothing. Three peers came out 57, 37 and 65px. |
| **Horizontal page overflow** | The page body must never scroll sideways. |
| **Tap targets under 44px on the phone** | A 34px chip reads right; a thumb needs 44. |
| **Open popovers after a programmatic focus** | A card that opens when code moves focus reads as the page acting on its own. |

**A real device beats the pane.** The bug above survived a verification pass in the preview pane and was found on a phone. For anything with sticky, focus, or touch in it, the Playwright persistent profile (a real window) is the floor, and a screenshot from an actual phone is the bar.

**The pass condition** is not "the numbers exist". It is: every control in a row shares one centre, every sticky x is unchanged after the pan, every popover is portaled with a gutter of 8px or more, no icon is 0px, flex peers differ by 2px or less, no overflow, and the first row's y on the phone is stated and judged.

### The behaviour half (the probe cannot see this)

A screen whose primary action silently destroyed data passed this gate on
geometry: centres aligned, sticky held, no overflow. The numbers were all true
and the screen was broken. **Before "verified", drive the surface, do not only
measure it.** Every control the user can press, pressed, and the state checked
after:

- Does a picker that holds many things actually hold many? Open it, add two,
  confirm both are there and the first was not replaced.
- Does every button have a handler that changes state? A control whose `onClick`
  only fires a toast is a lie.
- Does every count on screen match what the screen is showing? Derive counts from
  the rendered rows; a number read from a response while the rows come from
  somewhere else will disagree eventually.
- Does the empty / error / end state offer the next action?

**Two probe traps that make this pass for the wrong reason.** `[role=dialog]`
matches every mounted-but-hidden popover, and the first match is usually empty —
filter to the one that contains the controls. And a row's `innerText` starts with
its avatar initial, so `startsWith(name)` matches nothing and the assertion
passes having clicked nothing. Always assert the state *changed*, never just that
the call did not throw.

**The hook.** A `git commit` whose staged diff touches a UI component fires this gate.

---

## Gate 3: Shared Primitive (before editing anything two components read)

Tokens, primitives, shared headers, layout helpers, theme constants. "Why do you fix one thing and then mess up another?" happened three times in one session, and each time the shape was the same: a change to something shared, with its readers never re-read and the result never re-measured.

Before the edit:
1. **Grep the consumers.** Every file that imports it. Read how each one uses the thing you are about to change.
2. **One concern per function.** A helper that positions must not also pad; the padding was silently overridden by a later prop and the text sat on the board's edge. Position and padding became two functions and the bug became impossible.
3. **Ask what else reads this value.** If a second prop on the same element can set the same CSS property, one of them will win silently.

3b. **Match the house's scroll architecture exactly.** "No other screen has an end-to-end table with a side margin." Page root `h=100% overflow=hidden`, one inner scroller, sticky header and sticky first row inside it: the same skeleton Rooms, Timeline and Tasks use. A module that invents its own scroll container breaks sticky, the dock, and the phone fold at once.

After the edit:
4. **Re-run the probe on at least one consumer per kind.** A shared header fix was spot-checked on the page with the fullest configuration, not the page being worked on.

**The hook.** Editing a file whose path matches a token, primitive, or shared-component location fires this gate.

---

## The Working Contract (how the lead works with the stakeholder)

Mined from what the stakeholder repeated, in their words where it helps.

**Lead. Do not wait.** "You are the design lead. I am just guiding you." Come with a pick and a reason. A neutral list of options makes them do the job they asked you to do.

**Their feedback is a sample, never the scope.** "You should have thought of all of this before." Every pointer is one visible instance of a pattern. Before replying: name the pattern, sweep every surface for siblings, report the count, find the internal precedent, walk the workflow at real scale. Fixing the five things they listed is step zero.

**Expand, critique, refine, then ask.** "Think on my ask, expand on it, critique it, refine it, think it further, ask clarifying questions to reach the crux, then state it back." Do this before acting on any substantial ask. State the complete picture back in one message. Then one question, the one whose answer changes the work.

**Their suggestion is an input, not an order.** "Don't just blindly follow whatever I say. I might be wrong." Check every suggestion against the code, the locked decisions, and the references. Disagree once, with reasons and a pick. The dark split button was a hint; the semantic reason it was wrong for those three actions was the job. After a ruling, never re-raise it.

**100% sure or say so.** "Only if you are 100% sure, but that would be false confidence." Before "proceed": if any of the seven Surface Ready answers is missing, you are not sure. Say which one.

**Involve them on content they can see.** A rendered artifact, two directions, a pick. Framing approval is not a go. The go is on something they looked at.

**Say what you decided and why, then move.** "Let me know whatever you decide and when to move ahead." Decisions in the open, reasons attached, reversals named as reversals.

**Branch and PR hygiene is part of the design.** "Clean and hygienic PR, you know how picky the reviewers are." One workstream per branch, as ruled ("then we will raise another PR" means a new branch, not the current one). Docs ship with the code so the developers can collaborate. Commit per pass with a message that says what the pass is, and carries the probe numbers.

**"Only if you're satisfied."** That phrase appears in his asks more than once. It is not permission to skip; it is the instruction to self-certify against the seven questions and the probe, and to say which one is not met if any is.

**Never the same loop twice.** "We are getting into the same loop again and again for incremental fixes." A round that matches the feedback item for item is a loop. A round that comes back with the pattern, the count, and the fix for the unreported siblings is not.

---

## The Taste Bar (what "top 1%" means, checkably)

**Group with space, never with lines.** Hairline dividers between actions turn a floating control into a spreadsheet toolbar.

**One idiom per question.** Two controls that both mean "pick one of these" look the same, at the same height, on the same centre. Five hand-rolled copies of one control in one module is the most common slop.

**Two weights, not three.** A filled primary and quiet secondaries. A third weight is a third answer to "how does a control look here".

**Nothing welded.** A square-cornered fill inside a rounded container is a slab. A pill inside a tray sits in it with air around it.

**Derive, never hand-set.** `PAD = (H - ITEM) / 2`. Icons in `em` off one responsive token. If five paddings are typed by hand, one is arbitrary and nobody knows which.

**Every element, every viewport.** "Each element deserves attention. Each viewport deserves attention. Everything deserves attention." The phone is not a smaller desktop: chrome folds (status to a dot, search to an icon, toolbar away on scroll, back on a scroll up), labels drop under icons, the first row's y is measured.

**The house grammar is a floor, not a lid.** "We already have such patterns in our other list screens. Follow them, then make it better." Find the existing pattern first. Raise it, donate the raised version back, register it. Never a ninth picker.

**Copy is design.** Labels say what happens in the user's words. "Done" on a control that closes is "Close". "Looks good" on a look-only surface is consent-shaped and wrong. "Unnamed types" is the spec's word; "types with nobody" is hers. Indian English: "6 hrs", never "6h".

**No dead ends.** Every terminal state offers the next action in place. An empty state that only announces a hole sends her somewhere else to fill it and loses the story she was reading. The fix opens over the surface, and the surface updates when she comes back.

**Honest affordance.** A dash on a tappable cell says it is not tappable. A quiet "+" is an open door; a dashed seat is a hole. Draw the difference, do not erase it.

**Motion is content or it is noise.** A wait that drains in linear time is elapsing time. A rung that arrives on an ease-out curve is entering. Skip is mandatory on anything that plays; she will open it many times.

---

## The Code Bar (what "top 1%" code means here)

"Keep the codebase clean, modular, hygienic, reusable." "Find and fix it properly, once and for all, everywhere."

- **Fix at the seam, not at the call site.** A popover contract lives in tokens and is spread onto every popover; it is not six edits. A sticky rule lives in one helper the header and the rows both read, so they cannot drift.
- **Extract on the third copy, and sweep for the fourth.** The segmented control existed in four files and the view chips were a fifth idiom for the same question. One component, one height per size.
- **Delete the second door.** "Copy to an area…" opened the same picker on a tab one tap inside it. Two doors to one room is a bug, not a feature.
- **Dead code is a lie.** A `runId` whose comment described the leak it was meant to stop, and stopped nothing. `flex: 1` in a content-width container. If it cannot fire, remove it or make it fire.
- **One runnable check per non-trivial rule.** A pure function with a `.check.ts` beside it, asserting the cases that were wrong once. Eleven assertions caught the empty-seat bug and the stacked-hours bug before a browser did.
- **Measure, do not eyeball.** Reading the code said the padding was there. The page said 72. The number wins.
- **tsc 0, lint 0/0, checks pass, probe pasted.** That is the definition of done. Not one of the four.

---

## Gate 4: Harvest (at every commit, and at handoff)

Four questions, three tests, one script. Did this stretch produce a rule, a reusable, a pattern, a trap? Each is one line in the right file or "none". Saved only if a fresh session would spend more than five minutes re-deriving it, it is stable, and it is not already recorded. Then `scripts/registry_rot.py` on the repo. Full text: `references/harvest.md`.

**The hook.** Any `git commit` fires it.

---

## Environment traps

Moved to `references/traps.md`, keyed by what you were trying to do. Append there.
