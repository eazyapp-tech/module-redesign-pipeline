# The Designer's Gates

**Who this is for.** The agent acting as the design lead, and the humans who work with it: product managers, engineers, anyone with product knowledge. The agent leads the design; the human guides, corrects, and decides. The goal is work that a top product designer at Airbnb, Apple, Stripe, Linear or Notion would put their name on.

**Why gates and not rules.** Every rule below already existed somewhere as prose before the session that produced this file, and it still got broken. Knowing a rule was never the gap. The gap was the moment it gets applied. So these are checks tied to a moment in the work, and global hooks fire them at that moment whether or not anyone remembered. A rule you have to recall is advice. A gate you have to pass is a standard.

Five gates, one contract, one probe. Everything else is in the skill.

**The runnable form.** Copy `~/agent-config/templates/gates-module-redesign.md` into the work
as `GATES.md`. Gate 2 and Gate 4 carry a command and decide themselves; the rest stay manual
because no command can decide them. This file is the why, that ledger is the check.

**Enforcement is not automatic on install.** These gates fire because three hooks are wired into `~/.claude/settings.json` — a per-machine file a skill cannot write on its own. Set them up once with `references/hooks-setup.md`, or this file is rules again, not gates.

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
| **Every element's opacity with scripts blocked** | A scroll reveal that sets `opacity: 0` by default makes the whole page blank the moment JS does not run, and it silently does not run in a static preview. The animation opts IN (`.js .rv{opacity:0}`, script adds `.js`), never out. Fired on three published pages at once. |
| **Inline layout styles against the mobile media query** | An inline `style="grid-column:3"` beats the `@media (max-width:900px)` rule that collapses the grid, so ten margin notes would have created a phantom third column and scrolled a phone sideways. Position with a class the media query can reset; never inline. |
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

## Gate 5: State Census (before any module is called done)

Gate 1 fires when a surface is created. Gate 2 fires when you claim it works. **Neither fires for a state that already exists in the code and has never been rendered** — and that is exactly where five screens hid on the payment page: expired, not found, checking, failed, unsure. The expired one is where most arrivals actually land, the most-visited screen in the whole product. It had been built as plumbing, shipped showing a 72px strip of an asset whose full version sat unused in the same file, and then defended in prose I wrote without ever looking at the render. The stakeholder found all five by asking one question: "did you redesign the expired page thoughtfully, or did you miss any?"

**The census is mechanical, and that is the point.** "List the states you designed" returns the states you thought about, which is the same set that already got attention. The list has to come from the code, because the code is the only list that includes what you forgot.

1. **Enumerate from the branches, not from memory.** Every early return, every `if (x) return <Y/>`, every status value, every error and empty and loading path, every server-side redirect or `notFound`. In a page router read `getServerSideProps` too: a branch that never reaches the component is still a screen a person sees.
2. **Write the list down before rendering anything.** A state you can name and did not list is the one that ships unlooked-at.
3. **Force each branch and look at it.** A URL, a flag, a stubbed response, whatever reaches it. Looking is the gate — reasoning about a screen you have not seen is how a confident wrong rationale gets written. If a state cannot be reached in the harness, mark the row unreachable rather than dropping it.
4. **Judge each against the same bar as the happy path.** Does it say what is true right now, does it offer the next action in her words, does it use the assets this module already has. A terminal state with nothing to do is a dead end even when the reason it has nothing to do is a good one.

**The pass condition:** one row per branch — the state, how it was forced, the screenshot — every row filled or explicitly marked unreachable. A module with an unrendered branch is not done, however good the happy path is.

**Sizing comes before taste, not after.** The expired screen only became worth designing once someone counted the links that had ever been sent, and over 90% of them were already dead. Run the count for each state in the census before deciding which ones deserve the effort, or the rarest-looking screen keeps getting the least work while being the one most people see.

**The hook.** `~/agent-config/hooks/harvest_gate.py` raises it on any `git commit` whose staged diff carries UI, because that is when unrendered states ship. No command can decide whether it *passed*, so it also rides the handoff checklist and the pre-push list, beside Gate 2.

---

## The Working Contract (how the lead works with the stakeholder)

### 20 September 2026, the Vilaasa parity audit: an audit's job is to leave the code alone

The brief drew a boundary that is worth keeping as a habit: **audit, not
redesign, and another designer is changing layout and chrome in parallel, so do
not edit page or component files.** Findings only, plus fixes confined to data
files if a value is provably wrong. Three genuinely fixable bugs turned up (a
missing email whose absence was justified by a false comment in the source, a
dialog unreachable on 8 of 11 houses, a hardcoded two-slug list standing in for
a field), and the right move on all three was to write them down and touch
nothing. No data value was provably wrong, so nothing was changed at all. When
two people are in one tree, the audit that edits is the audit that gets blamed
for the other person's diff.

**Two of the three defects a subagent reported were wrong on checking.** The
walk of our own site reported an orphaned dialog (true, and bigger than
reported: 8 houses, not 1) and a shortlist that dies on reload (false, it
persists to sessionStorage, the walk checked localStorage). A third, an empty
WhatsApp link, I had raised myself from static HTML and withdrew after opening
it in a browser. The standing instruction to check a subagent's claims before
repeating them earned its keep three times in one session: a parity document is
read as a list of things to go and fix, so a wrong row there costs somebody a
morning.

### September 2026, the property onboarding rulings: what his hedges were worth

**"I'm still skeptical and not 100% sure. Are you?"** He asked that after being
told ten sheets were edited and verified. He had read none of them. Three
adversarial reads then found roughly a hundred and twenty defects, including the
inherited page that all ten sheets are built on teaching the opposite of a
ruling he had just given. **The hedge was the finding.** The right first move
when he hedges is to distrust the check that says nothing is wrong, before
distrusting anything else.

**Three times he corrected a recommendation and was right each time.** The chat
card stays in the conversation, because talking and tapping are the same action
and the record already said so. RK and Studio are flats with a smaller BHK
count, which closed a hole the previous correction had opened. And a deposit set
as a multiple has only one number available on the option, so it is based on the
asking price there, which was a plainer answer than the one offered him.

**He had to say "think in systems" twice in one thread**, and both times the
trigger was the same: a fix applied to the instance he named rather than to the
class. The second time it cost a full repair round.

**One instruction of his was structural and was first taken as cosmetic.** He
said a handoff sheet can have a design fixes section. Read properly that splits
every sheet's one fix list into work that follows from a ruling and changes a
screen, against slips in the file, which are different lists for different
people. Taken as "add a heading", it produced duplicate lists that immediately
drifted apart.

Mined from what the stakeholder repeated, in their words where it helps. This section is a harvest target, not background: Gate 4 question 5 writes here.

**Read the project's working record first, if one exists** (`~/.claude/docs/working-records/`, private to the operator and not in this repo). This section is the rule list. That record is the evidence: which sequence of moves produced agreement across a four-day project and which produced its worst turns, plus how to read which rung of his register you are on. Two moves caused every rejection in that project, and they are both about process rather than taste: approximating a source instead of opening it, and writing code instead of rendering a proposal.

**Lead. Do not wait.** "You are the design lead. I am just guiding you." Come with a pick and a reason. A neutral list of options makes them do the job they asked you to do.

**Their feedback is a sample, never the scope.** "You should have thought of all of this before." Every pointer is one visible instance of a pattern. Before replying: name the pattern, sweep every surface for siblings, report the count, find the internal precedent, walk the workflow at real scale. Fixing the five things they listed is step zero.

**Expand, critique, refine, then ask.** "Think on my ask, expand on it, critique it, refine it, think it further, ask clarifying questions to reach the crux, then state it back." Do this before acting on any substantial ask. State the complete picture back in one message. Then one question, the one whose answer changes the work.

**Their suggestion is an input, not an order.** "Don't just blindly follow whatever I say. I might be wrong." Check every suggestion against the code, the locked decisions, and the references. Disagree once, with reasons and a pick. The dark split button was a hint; the semantic reason it was wrong for those three actions was the job. After a ruling, never re-raise it.

**100% sure or say so.** "Only if you are 100% sure, but that would be false confidence." Before "proceed": if any of the seven Surface Ready answers is missing, you are not sure. Say which one.

**Dead space on a screen is a finding, and the measurement is the argument.** (2026-09-15, the agreement detail page.) The screen looked fine: a clean 820px document, centred, nothing broken, probe passing at 1440. Measuring it said something else — 12,611px of contract in a 688px viewport (18.3 screens) with 310px of empty ground down each side for every one of them. Two numbers, and they turn "it looks a bit empty" into a brief: she has no way to navigate what she came to read, and 620px of the width is available to fix it. Take them on any screen that feels thin: total scroll height over viewport height, and the gutter beside the content column. A screen that passes every check can still be spending half its width on nothing.

**And a reading aid must not move the thing being read.** The reading column was the one part of that page already correct. The rail takes the left gutter and a spacer holds the right, so the paper measured left 346 / centre 756 with the rail and without it — verified by hiding both in the live DOM and re-measuring, not by reasoning about the flexbox.

**Fixing the shared function is half the fix. Open every caller.** (2026-09-15, the agreement module.) `literalDetail` treated "zero receivers" and "no count given" as one branch, so an agreement nobody receives claimed its hand-typed details appeared on every agreement in the property. The function was corrected and the editor still said "every agreement" on the live screen — because `TemplateEditor.tsx:521` did `linkedTenantsCount || undefined`, re-creating the exact conflation at the call site, where it had been harmless while the function was wrong. A root-cause fix that stops at the function is a hypothesis; it is only done when every caller has been opened and read. Here that was three call sites and one of them defeated it. The tell is cheap: after the fix, load each consumer and read the sentence, rather than trusting that one edit reached them all.

**Probe the unmodified screen before you own a finding, or disown one.** (2026-09-15, the desktop agreement library.) The Done Probe came back with two findings at 375 and it is genuinely ambiguous which of them the change caused. Restoring the original files and running the same probe answered it in four minutes: the baseline was already `y=417` with FOUR sub-44 tap targets, so every tap finding was pre-existing — and the new screen was `y=456`, so 39px of the chrome finding WAS mine, from one line I had added. Without the baseline both halves go wrong in opposite directions: four targets get "fixed" in a shared component that four other modules depend on, and a real 39px regression gets waved through as "the screen has always been like this". Back the work up first (`git diff > patch` plus a copy of each changed file, verified present), then `git checkout -- components/`, probe, restore, and diff the two reports. Report a pre-existing finding, fix the delta.

**A full autonomy grant is a request for a decision, not for more options.** (2026-09-15.) "I'm going to go away for a bath. You continue... complete the redesign and show it to me. You are the expert. You own it. You lead." Handed that mid-turn, the temptation is to come back with directions to choose from, which is the one thing he cannot use while away. What made the run usable was having something to decide FROM: two measurements (18.3 screens of scroll, 310px of dead gutter each side) turned "this screen feels thin" into a brief that answers itself, and everything after was execution against it. When he leaves, measure first — the numbers make the call, so you are not substituting your taste for his while he is not there to correct it. Then build it, verify every state, and have the before/after ready for the moment he is back.

**When he says he is skeptical, the answer is a named gap, never reassurance.** (2026-09-15.) "proceed only if u are now 100% sure, satisfied & confident... i'm so skeptical now throughout", after a session in which I had told him a gate needed his hands when it did not, and shipped a screen whose unchecked states then produced six defects. The skepticism was earned and accurate, which means it is a symptom report about the process and not a mood to be managed. The move that works is the one his working record already prescribes: answer "are you sure" two ways only — yes with the evidence, or no with the name of the missing check. Here the honest answer was no, because I had never opened the editor or the add flow live and was about to redesign both. Saying that first, then closing it, cost one turn and turned up the whole real inventory — which a confident yes would have skipped straight past. Reassurance would also have been the fourth time in this project that "yes" was given on a check that had not run.

**And check your own finding before you build a plan on it.** (Same session.) I told him all three screens drew the alarm as a full-width slab. Reading the markup, the detail page's is deliberately constrained to the document's 820px column with a comment explaining why. The real defect was better and different — three copies that had drifted — but I had already said the wrong thing out loud. On a surface he is skeptical about, an inventory stated from two live screenshots and a grep is still a draft; it becomes a finding after the code is read.

**"Check the four remaining states" is not a request for confirmation.** (2026-09-15.) Four words from him, on states whose code I had not touched, and forcing them properly turned up: a count that promised "clear the search to see all 4" while the active view held 2, an operator reading axios's "Network Error" because `error.message` outranked the sentence written for that exact failure, four phantom stat tiles on a loading screen that has none (#1001), and a dead `yarn checks` hiding a real axis-maths failure (#1000). None of that is visible from reading the code, and none of it would have surfaced from confirming the states render. The states ARE where the defects live, because they are the part nobody looks at twice — so checking one means forcing it, reading every number and every sentence in it, and asking what it promises her that the next tap will not deliver.

**His DO-NOT list is doing real work, not ceremony. Read it as a map of the mistakes you are about to make.** (2026-09-15, the desktop agreement library.) His resume prompt carried four prohibitions. Building the screen walked straight into three of them within the hour, and each time the constraint was the only thing that stopped it: a dead `headerBg` prop looked like the clean way to a white header row and would have silently restyled four other modules; the locked artifact's own "copy of the Default" tag needed a field the `/list` response does not carry, and a `_1` name-suffix guess was right there; and with `tsc` clean and the screen looking correct, committing without probe numbers felt like a formality. A DO-NOT of his is not him being careful. It is him having watched that exact failure before, so when one of them starts to feel like an obstacle to a task that is otherwise finished, that is the moment it is doing its work.

**A number in a locked artifact is still a drawing until it is measured against the screen it was borrowed from.** (Same session.) The artifact specified the unset cell as 46x28 at radius 8px, and said in its own text that it was taken from Complaint Bot Setup. The real cell on that board measures 58x30 at radius 999px with `1px dashed #8B8B95` and a `#6E6E77` glyph, and those two colours were already exported tokens. The locked thing is the DECISION ("unset is a compact dashed plus, not a text button"); the pixel values in a drawing of it are the same approximation the artifact was meant to replace. Open the source screen, measure the object, import its tokens — and where the measurement and the drawing disagree, build the measurement and say so.

**Involve them on content they can see.** A rendered artifact, two directions, a pick. Framing approval is not a go. The go is on something they looked at.

**Say what you decided and why, then move.** "Let me know whatever you decide and when to move ahead." Decisions in the open, reasons attached, reversals named as reversals.

**Branch and PR hygiene is part of the design.** "Clean and hygienic PR, you know how picky the reviewers are." One workstream per branch, as ruled ("then we will raise another PR" means a new branch, not the current one). Docs ship with the code so the developers can collaborate. Commit per pass with a message that says what the pass is, and carries the probe numbers.

**"Only if you're satisfied."** That phrase appears in his asks more than once. It is not permission to skip; it is the instruction to self-certify against the seven questions and the probe, and to say which one is not met if any is.

**The hedged observation is the strongest signal in the session.** "I don't know why, but somehow it felt like there is some scroll problem. I don't know. Could be just my mistake. Could be that I did not see it, but still, there is some problem." Three times in one session he flagged something with an apology attached, and three times he was right: a 348px sideways scroll the audit called clean, five states nobody had rendered, a hero asset cropped to a strip. The hedge is not a suggestion to weigh against the code — it is a symptom report from the only person looking with fresh eyes. Suggestions get cross-checked; **symptoms get measured, and the first thing to suspect is the check that says there is nothing there.**

**"Why is this here?" is a deletion question.** "Why do we need even chips here?" was not a request to justify the chips. Every element he asks that about is one that arrived by default, and for the chips the honest answer was that they should not exist. Answer with the reason the element earns its place, or delete it. Never compose a rationale for something you have not looked at — on this page that produced a confident paragraph about a screen that had never been rendered, false the moment it was written.

**A ruling that inverts a default has to be swept, not just applied.** He reversed a production gate from off-unless-enabled to on-unless-disabled. The code changed; the PR description still described the old behaviour and came one sentence from reaching the reviewer that way. When a ruling inverts something, grep every place the old version is *described* — PR body, handoff, docs, comments, tests — not only the line that implements it. The sample-not-scope rule applies to his decisions as much as to his feedback.

**"Blocked on the backend" is not permission to ship plumbing.** The expired screen had one honest capability and no route to the rest, so it shipped as plumbing. He supplied the design himself: send her to WhatsApp with a preset message that triggers the workflow, wait on the backend for the rest. Design the one action that is not blocked, name what is waiting, and never let a good reason justify a dead end.

**The two-word turn is an expansion.** "& code" arrived as its own message after a design pass and meant the same standard now applies to the code. "& show me all the screenshots too" meant every state, not a sample. His short follow-ups widen scope; read them as "and everywhere else this applies", never as one more small item.

**What "100%" actually fails on.** Four times in one session he handed the gate over: "push it if 100% satisfied", "gotta be 100% sure, this is payment related". None of those failed on design confidence. They failed on checks that could not fail — an overflow audit measured against a number that grows with the overflow, six scripts pointed at a port serving the previous worktree, a secret scan that errored and printed "clean" — and on a fix verified at its call site instead of its destination. Before answering his "100%?", confirm the check ran, could have failed, and measured the thing you are claiming. Traps in `traps.md`.

**Systems thinking is for designing, not only for analysing.** He had to send "think in systems & workflows, 2nd & 3rd order effects" as a standalone turn, and then "think in systems always" two turns later, in a session where that is already a standing instruction. The pattern behind it: the systems lens was running during investigation and switched off during design, so a screen got built as a mechanism and only became a designed thing after he pushed. If the ask is to design something, the count, the workflow it sits in, and what happens next come first, on the first pass.

**The render is the artifact of agreement, not the plan.** "I wanna visualize first before u make changes in the code." "Either show me screenshots or show me locally for eyeballing." "Can I eyeball it? Can you open it in the browser pane?" He asked for a rendered thing before code five separate times in four days. A described plan is not what he is approving and never has been — the go is on something he looked at.

**His sharpest register means you answered a different question.** Every time that landed, the reply had been fluent and about something adjacent: he asked whether the module's *code* was better written than the live page's, and got an answer about whether it took money yet. His own instruction: "Are you getting what I'm trying to ask or not? If not, then ask a clarifying question." One clarifying question is always cheaper than a confident answer to the wrong question.

**An item he raised once and has not seen is still open, and he counts.** He asked for a chevron to be removed on 12 September, and asked again on 13 September with "I had told you to remove the chevron." He returns to pointer lists from several turns back — "what are the tasks that remain from my original pointer earlier?" — so an unresolved item does not decay. Keep the open list and report it back unprompted, including the ones you decided against and why.

**A rejected treatment is unassigned, not dead.** "I don't like the tumbler. Save this and remember that this tumbler design can be used for an electricity meter or something." He rejects a thing for one surface while filing it for another. Record those against the module he named, or the idea is lost and re-derived from scratch.

**When he cannot follow an explanation, that is the explanation's fault, and he will say so in capitals.** "TALK SIMPLY, I COULDN'T UNDERSTAND." It landed on a correct, well-evidenced answer about a hook that was not wired: the content was right and it was delivered in the vocabulary of the thing being fixed rather than in his. The repair is not fewer facts, it is the everyday sentence first ("the reminder to write down learnings never switches on") and the mechanism second, only if he asks. He is CPO, not the engineer sitting inside the system. Same rule for asking him to confirm understanding: when he says "state it back to me", the answer is what you now believe in plain words, not a restatement of the work.

**A plain go-ahead from him still carries the bar, and the bar is the check, not the code.** He approved a three-item fix list with "go ahead, build all three. Do your best, top 1%. no skimming, no shoddy work" and corrected nothing all session. That sentence is not decoration and it is not about the code reading well: the thing that would have earned the complaint was three green assertions from a check that had never once seen the bug it was written for. Run every new check against the broken version first, one fix at a time, and confirm it fails for the right reason. Twice in the same session a measurement of mine was faked by my own instrumentation, once by a regex that matched the hostname and once by history left behind by an earlier step. **When a check disagrees with itself between runs, suspect the check before the code.**

**Resuming after a compaction, the durability comes before the work.** He asked for it directly: "we had auto-compacted it, so I do not want you to lose all the context. Figure out a way to ensure you are not missing anything." The answer that satisfied him was not care, it was structure: enumerate the whole surface into a file BEFORE judging any of it, leave the check in the repo as a runnable script rather than as a result in chat, and sync the finished record to the vault the same turn. A finding that lives only in the conversation does not survive the next compaction.

**"U satisfied 100%?" is an instruction to go back and look, never a question to answer yes.** He asks it after the work is reported, pushed and apparently finished. It landed on this session at a point where everything was green: sixteen checks passing, each run against its own bug, committed and pushed. Answering yes would have shipped three defects, two of them introduced by the fix itself in the same hour, including a back control that took her out of the site and an effect on the money path that had never once executed. The right response is an actual re-audit with the answer stated as a list of what is not verified, and the two questions that find things are: **which line of this change has never been executed, and what question is my guard really answering.** Same family as the hedge rule, and sharper, because here he is asking outright and the temptation to reassure is strongest when the checks are green. The same applies to "are you sure", "confident?", and "100%?" on a document or a claim.

**When a standing rule blocks a check, say what it blocks. He will usually lift it.** Mid-turn, unprompted: "You can send the OTP as well. That is not a problem if that is required for you to test it systematically and thoroughly. As long as there is no real payment made." The no-real-OTPs rule existed to protect real collectors, and it was quietly costing the cash road its only end-to-end walk. He lifted the part that blocked thoroughness and kept the part that mattered, which is how he treats most constraints. So name the check you are skipping and why, rather than skipping it silently and reporting the rest as complete: a gap he does not know about is the one thing he cannot rule on.

**His bug reports are use, not testing, and that is the axis no scripted walk covers.** Thirty-one browser assertions and a sweep over every state passed, and he found a real defect in under a minute: open a receipt, press back, land on the bills instead of the receipts. Scripts walk transitions; he arrives at a screen **for a reason** and then does the next thing that reason implies. He went to History because that is where you check whether a payment landed, and the bug only exists for someone who went there on purpose. So when a scripted pass is green, the remaining bugs are the ones only purposeful use finds: name what somebody would come to each screen TO DO, do that, and then do the next thing. And read his report as a cause, never an instance, because his "think in systems" arrived in the same breath and was right: one report, one architectural cause, two live instances.

**Verify a reviewer's finding and you usually find it is half of one.** Every one of nimit-jn's eight on the payment page was real, and three were not the whole shape. "The receipt is initialised once and never retries" — the reacting half was already right, and the missing half was that nothing ever asked a second time; fixing the named half would have added a duplicate effect beside a working one, which I wrote before noticing. "The refusal reason is discarded" — carrying it through changes nothing while the translator answers "try once more" to every reason it does not recognise, including an invoice already settled, which is the worst advice available on a cash screen. So take a finding as a symptom the same way his own are taken: confirm it in the code, then ask what else has to be true for the fix to actually reach her. The reviewer found the visible half; the other half is yours to find.

**When you do not know what something should do, go and see what it does today.** His standing instruction, given as a repeatable behaviour rather than an answer to one question: *"For anything that you are confused about, you can always check what happens right now and take that as your first preference, or as a starting point, or as a recommendation, and then get it confirmed from me along with your recommendations."* The live product is the decision that has already been made, and a redesign that silently departs from it is a decision nobody took. So the shape is always: what happens now, what I would change and why, and the question that needs his word. It also stops the other failure, which is asking him to re-decide something the product already answers. The corollary bit twice on the payment page: **verify that today's behaviour is actually reachable before carrying it over.** A parity gap can be a gap to dead code — `redirect_url` on the live payment page reads a field the backend has never sent, so the branch has been false since it was written, and the honest answer was that there was nothing to carry.

**Never the same loop twice.** "We are getting into the same loop again and again for incremental fixes." A round that matches the feedback item for item is a loop. A round that comes back with the pattern, the count, and the fix for the unreported siblings is not.

---

- **His ruling on one component is about that component.** Vilaasa, 20 Sep 2026 (D54): he picked a house card (D53); the brief extended it to room types, area headers and the map popup, and he said "you have used one component for everything, which is also confusing". One kind of thing, one look: a house, a place, a room option and a map summary each get their own form from the same tokens. Before applying a ruling beyond the object he named, say so and ask.
- **Too much at once is the cause under his notes; fix it as a check, and keep the check small.** Vilaasa, 19 Sep 2026 (D51): eight notes (sections that should be sheets, subtexts, a tall header, cramped pages, persona chips) were one cause, cognitive load. He asked for them as checks that fail, then scaled that down within the hour: "don't overengineer it", add rules to the existing page-lint, no new tool, no gate changes. A new checker or a doc set is the over-build he means; six rules in `tools/page-lint.mjs` with one fixture was enough.

**A comparison waits for the whole set.** Same day: the ranked "where ours
loses" was written while one of eight readings was still running, and it counted
Cove with our floor as keeping no price. The late row showed Cove pins
"available, SGD 1,450 / month" on its room page. The claim was confident,
published, and wrong in the direction that flattered the argument, which is the
direction a partial set always fails in. Do not write the comparative sentence
until every member of the set has reported; if a result is still running, say so
and leave the sentence unwritten rather than provisional.

### 20 September 2026, the reference board: a brief's fallback is not a substitute for the live page

The task named a fallback for our own floor, "if the live host does not answer,
use the captures in `tools/calibration/cal-out/final/meridian/`". Those four
files are the **home** page at two widths; the task asked for Meridian's **house**
page, which is not in them. The live address was already written down in the
folder the work was happening in, `runs/vilaasapg/site/refs/notes.md` from the
19 September pass: `meridianstays-review-test.rentok.com/properties/signet`,
which answered 200 first try. **Read the prior notes in the folder you are
working in before accepting a brief's fallback**, and check that the fallback
actually holds the surface being asked for rather than a page from the same
site. A fallback taken on trust would have put a home page in a column of house
pages and nobody reading the board would have seen why it looked wrong.


## The Taste Bar (what "top 1%" means, checkably)

**Current data is not the limitation, it is only the current reality.** His words, about team-member photos that 4% of records have: "Sooner or later users will have their own DP." Design the surface the full data deserves and make the degraded case beautiful in its own right — a considered initial, not a grey circle. Designing down to today's coverage bakes the gap in permanently and guarantees a redesign the moment the data lands. The inverse trap is equally his rule: **a case that affects one user still gets designed.** "All the practical real-life cases thought through properly, even if it is used for one particular user. No shoddy work." Sizing decides what you do *first*, never what you skip.

**A metaphor has a boundary, and past it the metaphor stops meaning anything.** The payment page's paper-and-machine language was pushed onto every surface until he said: "You do not need to force-fit everything into the printer paper UI. It will lose its meaning. It has already lost its meaning." Then he had to say it a second time. A design system earns its meaning by being the answer to a particular question; applied to a screen that asks a different question it reads as a costume. Name what the metaphor stands for, and when a surface falls outside it, extend the system rather than stretch the skin.

**Never make her confirm a decision she has already made.** She tapped Pay on one specific bill, and the next screen asked her which bills and how much. "That's a stupid workflow." If the tap carried the answer, carry it forward and land her on the next real decision. Every screen that only re-states what she just chose is a screen that exists because the flow was assembled from components instead of walked as a job.

**Open the source he named, always, before writing anything.** He supplies Figma nodes with exact ids, live screenshots, mood boards, competitor references, real numbers. Roughly fifteen Figma links in four days, and the most repeated craft rejection of the project was reproducing the shape of one instead of extracting from it: "Why did you not use the exact Figma asset from Figma itself?" A rendered object in a design file is one tool call away and always beats a hand-drawn approximation. His word for the failure is **skimming**, and it is detectable from outside, which is why he catches it every time. When you cannot tell which node he means, ask. He offers material unprompted and never treats the request as a burden.

**Put the code beside the mockup before calling it built.** An approved design can be lost in the port: "Why are you not designing with taste? The artifact looks better than what you have designed." The design was right and the implementation dropped it, which reads to him as a taste failure rather than a fidelity failure. A round that follows an approved render is done when the two are placed side by side and the difference is nil.

**Every step she can be on has an address, and our back agrees with her phone's back.** A step held in component state looks right in every screenshot and cannot be returned to, refreshed or shared; a back control built as a plain link records a NEW entry, so her own back button walks her forward into the screen she just left. Both were live on the payment page and neither was visible to a render check. Two questions per screen, asked out loud: what is this screen's URL, and if she presses the phone's back here, where does she land. A screen that cannot answer the first is not finished.

**Only the address survives leaving a screen, and what does not survive looks exactly like the default.** A detail route usually REPLACES the screen it opened from rather than covering it, so every choice she made there is destroyed: which tab she was reading, what she had expanded, what she had filtered. She comes back to the default arrangement, which looks correct, so nothing reports it. Two questions per screen she can arrange: what did she change about how she is looking at this, and is any of it in the URL. Whatever is not, put it there, in one list the page owns, so the next arrangement someone adds inherits it instead of repeating the bug.

**A guard fails safe by construction, or it is not a guard.** The test behind a back control, a permission, a rate limit, a de-duplication key: write it so that the unknown case and the case you did not think of both land on the safe side, rather than so that it is correct about the situations you listed. The difference shows up as a proxy that agrees with the real question almost always: "has the history grown" for "is the step behind us ours" was right on every path walked and wrong on the one that ejected her from the site. Ask what the guard does when it is wrong, and if the answer is not "the same thing it did before we built it", rewrite it.

**The sentence and the control under it must recommend the same thing.** When a message is softened because we are not certain, the action beside it has to move too, or the screen argues with itself in front of her. The payment page said "please check before paying again" and put a **Try again** key directly underneath, because the copy was rewritten to be honest and the flag choosing the action was left alone. On a money path that is an invitation to pay twice. Whenever you change what a screen SAYS about certainty, re-read what it OFFERS in the same breath, and treat the pair as one edit.

**A card that looks like one object behaves like one.** If a row or card opens something, the reach of that action is the whole card, not the words inside it. Anything else on the card that has its own job sits above that reach and keeps it. The wrong version is invisible in every screenshot, because the half that does nothing looks exactly like the half that works: the payment page's bills had a button around the title and the dates, so a thumb on the amount, the date or the empty middle did nothing at all. The control still wraps only the words, for the screen reader and the focus ring; the reach is stretched over the card by a pseudo element, which is how a card gets one primary action without nesting one control inside another.

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

Five questions, three tests, one script. Did this stretch produce a rule, a reusable, a pattern, a trap, **or a working note**? Each is one line in the right file or "none". The fifth is the one that gets skipped: the first four all ask what the code taught you, so none of them can notice that nothing was written down about how the work went with him. Saved only if a fresh session would spend more than five minutes re-deriving it, it is stable, it is not already recorded, and, when it prescribes a command, that command has been run here once and its output seen. Then `scripts/registry_rot.py` on the repo. Full text: `references/harvest.md`.

**The hook.** `~/agent-config/hooks/harvest_gate.py` on `PreToolUse` / `Bash`: any `git commit` fires it.

---

- **An open item says the answer "gets read off the Figma / the API / the logs". Is that a status?** No, it is an unfinished task with a source attached, and it will sit there for weeks because it reads like a decision that is merely pending. Go and read the source the moment you meet the sentence. On rentok-property-onboarding an item had said since 28 August that the onboarding checklist's step names, grouping and count "get read off the Figma, not invented"; nobody opened the file, and when someone finally did, all nine steps were there with names, descriptions, videos and buttons. Sweep every document for that construction before writing anything downstream of it, and when you close one, say what the source settled AND what it left open, since a drawing answers the "what" and almost never the "why".

## Environment traps

Moved to `references/traps.md`, keyed by what you were trying to do. Append there.

## Rule, added 2026-09-15: open the bar screens before you draw

Gate 1 (Surface Ready) asks for "the internal precedent". That has been read as
naming a screen. It is not. **Open the screens named in
`~/agent-config/bars/<profile>.md` live, at the target width, and look at them
before any design judgement or any drawing.** A description in a doc, a memory
entry, or a screenshot you took last week does not count.

Cost of skipping it, 2026-09-15: two design directions for the agreement
library rejected, the second as "looks forced & shitty, not top 1%". Both were
generic SaaS tables drawn from memory. The screen that already solved the exact
problem, Complaint Bot Setup's tinted catch-all row with an 11px subtitle, was
one route away the whole time and was opened only after he pushed twice.

The check is one command, and it was run here:
```
# dev server already up on the module's worktree port
open /property/complaints/setup, /home, /property/bed-availability at 1440
```

## Rule, added 2026-09-15: a status pill must go silent when the screen does not know

Any chip, pill or badge that states what is true right now ("Live on WhatsApp",
"On every agreement", "Needs setup 3") is a claim, and a claim needs a reading.
Render it only when the screen has actually read the answer. Not while loading,
and **not after a failed load** — a screen whose fetch errored does not know
whether the thing is set up, and showing the not-set-up variant by default turns
a network failure into a confident lie about the operator's data.

Caught on `/settings/first-party-agreement`: the error state drew "Not set up"
in amber beside "Could not load your first party". Two sentences on one screen,
one saying it failed to read and the other reporting what it read.

```tsx
titleTrailing={isLoading || loadError ? undefined : statusPill}
```

The test at Gate 5 (State Census): force the error state and read every word on
the screen, not just the error block. The lie is usually in the chrome that
renders regardless of state.

## Working note, added 2026-09-15: his ruling is the shape, not the mechanism

I put a question to him as A/B with a pick: is the property-level first party a
fallback (A) or still the main place (B)? He ruled **A — "go ahead and redesign
it"**.

Mid-build the mechanism behind the question turned out to be wrong: the backend
checkout was 917 commits stale, and the override that A assumed was per-room had
moved to per-tenant, with the property party promoted to a first-class pseudo
row in every picker. **The ruling survived unchanged.** What he had decided was
the screen's standing — default, overridable — and that was still true. What
changed was the plumbing under it, which was never his to rule on.

So: when a discovery invalidates the mechanism you described, **check whether it
invalidates the decision before going back to him.** Re-asking a question he has
already answered, because a detail underneath it moved, spends his turn to buy
nothing. Correct the record, say what changed in one line, and keep building.

The converse is the real failure and it is the one to watch: if the discovery
had flipped the standing — if the property party had turned out to be genuinely
dead — continuing under A because he said "go ahead" would have been building
the wrong screen with his authorisation as cover.

**Repeated mistake, second time (see #975):** a verification script clicked a
real primary action against live data because its selector (`locator("input")
.first`) hit the app's global search box instead of the form field, so the form
stayed valid and saved. Both writes were value-identical and verified so field
by field, but that was luck, not design. The rule now: **a script that clicks a
real primary action against live data blocks the write endpoint at the XHR layer
first, every time, and asserts zero calls left the browser.** That assertion is
also the cleanest proof that client-side validation short-circuits before the
network, so it pays for itself.

### Working note, 2026-08-30, rentok-property-onboarding

**A rule being loaded is not the rule firing.** The project's own AGENTS.md said "Requirements are written from the user's need, not from what the current code does. Current data and code are reality, but never a limit." It was in context the whole session. Within an hour of reading it I checked the backend, found the structure model mostly built, and wrote "the backend already does X, so this is an addition not a rebuild" into the product concept document as its headline. He caught it and had to state the rule again by hand.

**The tell is excitement, not ignorance.** The rule does not fail when I have forgotten it. It fails when a finding feels valuable and the finding happens to be about what exists. Every fact in that section was true, which is exactly why it passed my own review: I was checking accuracy, and the failure was placement. A true fact in a spec teaches the reader to design to it.

**What to do instead.** When a check of the existing system produces something worth saying, it goes in its own document with a warning naming the one conversation it is for, and the spec never references it. Ask before writing any paragraph about current state: does this change what we want, or only what we think it costs? Only the second one is allowed, and not in the spec.

**Second half of the same session:** his model beat mine on the flat problem, and the tell was that his version made one of my rules unnecessary rather than adding one. When his reframe deletes something instead of adding to it, adopt it whole and stop defending the version that needed the extra rule.

## Rule, added 2026-09-16: never copy a sibling's number without re-probing

A header button was given `h="40px"` because the template library's header button
is 40px. The probe went from 2 tap findings to 3 on the spot. The library's 40 was
never a house value — it is an unfixed finding of its own, and copying it spread
it to a second screen in one line.

Applies to any measurement lifted from another file: heights, paddings, widths,
breakpoints. The sibling is evidence of what exists, never of what passes. Copy
the number, then run the probe before the commit, every time.

Cheap tell: if the value you are copying is below a known floor (44px tap, 4.5:1
contrast), you are copying a defect.

## Working note, added 2026-09-16: he asks "do you love it" and means it literally

Asked directly whether I loved the design. The honest answer was no, and saying
so produced three of the best rounds of the session: the paper as the hero, the
roster as people with a door, and the readiness dock.

What that establishes: **"are you satisfied / do you love it" is not a request
for reassurance, it is a request for the list.** Answering "yes, it's solid" would
have ended the work at a competent settings screen. The right shape is: no, here
is what is missing, here is my pick for the next round, want it. He then says yes
and the work gets better.

Twice he supplied the constraint I was missing rather than the fix:

- **"see the existing capability as well, don't start making something that
  doesn't even exist."** That sent me to read `AddAgreementPartyDrawer`, which
  turned out to require team members for both name fields. My screen had been
  telling her to "add the second owner on a room" without mentioning that a
  co-owner not on the team has to be created there first. Without the constraint
  that over-promise would have shipped.
- **"the placement feels a little bit odd"**, with two candidate positions. His
  hedge was right and the reason was one neither of us had said out loud: sitting
  beside the detail rows, the action read as editing only those rows, when it
  edits the signature and language too.

Pattern to keep: when he offers two placements, pick one and say WHY the other
loses. He is not asking to be given both back.

## Rule, added 2026-09-16: every section of a screen must appear in a screenshot

Four rounds of screenshots of one edit form all stopped at the same scroll
position, above the signature section. Everything below it had been wired and
never opened. He had to ask: "i havent yet seen how to upload signature during
edit."

What was hiding there was not small: a borrowed KYC component wearing its own
layout with its camera tile 790px from its label, a second solid-blue primary
competing with Save, and a sign modal with a 164px dead zone where the box was
wider than the canvas.

**Gate 5 (State Census) counts STATES. This counts SECTIONS.** Both are needed:
a screen can have every state verified and still have a third of its height that
nobody has looked at.

The habit: before calling a screen done, list its sections top to bottom, and
name the screenshot that shows each one. A section with no screenshot is not
built, it is only typed. `full_page: true` is not enough on its own — a sticky
bar overlays the bottom, and a long form still needs a scrolled capture per
section.

**Where it bites hardest: anywhere a component was borrowed from another module.**
A borrowed component keeps its own clothes until somebody looks at it next to
yours. That is the thing a screenshot catches and a prop list never will.

## Working note, added 2026-09-16: his two-word follow-ups are section audits

"i havent yet seen how to upload signature during edit" and, seconds later, "and
other modals etc & drawers etc".

Neither is a feature request. Both are him noticing that the evidence I supplied
covered less than the thing I claimed was done, and both were right. The second
one found a worse problem than the first: the shared properties drawer's "Apply
Settings" was writing the landlord's identity onto up to 48 properties with no
statement of what it replaced and no undo.

The tell to watch for in my own output: **if the screenshots I send are all of
the same region, I have verified a region and reported a screen.** When he names
one missing view, sweep for its siblings before answering — the modals, the
drawers, the scrolled-past sections — because he will name those next and he
should not have to.

### Working note, 16 September 2026, property onboarding

**What he corrected, and he was right every time.** That there is no quick add
on the conventional screens, only in Rio. That the stay terms are pickers and
the free text beside them is sample copy. That the frequency labels are a
design error and the design is already extendable, so nothing needs rebuilding.
That the Apply to dropdown opens a full screen. None of these needed a debate;
all four were checkable in the file in one call each, and in each case the file
agreed with him.

**What he had to say twice.** "Go through the rental option screen flow again,
because I think you seem a bit confused." He had said something close to this
before, about Rio. Both times the cause was the same: describing a screen from
the document instead of opening it.

**What turned out to be his call and not mine.** Whether the first version
carries every frequency or two. I had written "the frequencies are wrong in
both directions" as a finding; it is a release decision, and he made it.

**One place to push back rather than accept.** He said Bhk Type is wrong. The
file shows it is conditional and already follows the letting-levels ruling, and
what is actually wrong is the sample data. That is now a question back to him
with a recommendation, not a silent fix and not a silent agreement.

**Rule, added 16 September 2026.** Any document that describes a design carries
the frame id inline at every screen it describes, and a script checks those ids
still resolve. A design document with no ids cannot be reviewed, only re-read,
and re-reading is what lets prose drift away from the drawing across
amendments.

## Rule, added 2026-09-16: a warning belongs where the consequence is visible

An agreement module warned, on its Agreement tab, that "24 details are still
typed in by hand". The preview drawer — the screen an operator opens to check a
specific tenant's copy **before sending it** — rendered that same document
greeting a different tenant by name, and said nothing.

Both surfaces were built from the same finding. Only one of them was where the
finding becomes a person's name on a page.

The rule: when a screen predicts a problem, find every surface where that
problem becomes CONCRETE and carry the warning there too. A notice on the
overview and silence on the preview is not defence in depth, it is a warning
placed where it costs nothing to ignore.

The test to run at Gate 5: for each warning on a screen, name the surface where
its consequence is actually seen. If they are different surfaces, the warning is
in the wrong place or it is in only one of two right places.

Corollary that kept this honest: the preview shows the notice only for an
UNSIGNED tenant. A signed copy is frozen, so its literals are history rather
than a warning, and flagging them would invent an action she cannot take.

## Working note, added 2026-09-16: "verify those two overlays too"

I ended a round by listing two overlays I had not verified and why. He replied
with four words telling me to verify them. One of them contained a real defect.

The lesson is not "be thorough" — I had already been thorough enough to find and
name the gap. It is that **naming a gap is not the same as closing it, and he
will always choose closed.** An honest "not verified" is the right thing to say
and the wrong place to stop: it should be the last line of a round only when
something genuinely blocks it (a missing ruling, a write I must not make), never
when the blocker is that the selector was awkward or the data was inconvenient.

Both blockers here dissolved on a second look: the preview opened on ROW CLICK
rather than a button, which the source said plainly, and detach needed a linked
tenant that no template had — reachable by stubbing the list response instead of
pinning a real tenant, which would have been a write.

When the honest report is "I could not reach it", the next move is to read the
source for the trigger and stub the data, not to hand him the gap.

**Rule, added 16 September 2026, the companion to the frame-id rule.** Every
piece of drawn copy a document quotes is checked against the file, and the
count of unchecked quotes is a number the document can report. A sheet that
cannot say how many of its quotes have been verified is not finished, it is
unmeasured. `tools/quoteaudit.py` in the property-onboarding repo is the
implementation: quotes found in the structure pass, quotes that are overrides
are confirmed by render and listed with their frame and date.

**Working note, the second half of 16 September.** He answered a completed
sweep with five words: *"only if u are now 100% satisfied."* Saying yes would
have been the cheap move and would have been wrong. Turning it into a
measurement found six sheets carrying claims about screens that have since been
redrawn, including two design fixes asking for work the designer had already
done. **The lesson is not "check more". It is that his one-line challenge is
worth converting into a number before answering it**, because the number is
what finds the things confidence cannot.

**Rule, added 16 September 2026, completing the source model.** A design suite
has four records and all four are secondary: the design file, the ruling record,
the running product plus its open branches, and the documents themselves. The
fifth thing is what the stakeholder actually wrote, in the raw transcripts.
**Check open decisions against his own words before asking him again** — a
decision sitting open that he ruled a month ago is the most annoying question
you can put to him, and it is cheap to catch.

**Working note, 16 September, second half.** He corrected me three times in one
stretch and each correction was a widening, not a narrowing. "You may use me as
per your recommendation" — bring the conflict and the pick, do not just report.
"Why don't you get it in one go?" — stop drip-feeding one search per turn when
the corpus is small enough to read whole. And "we do not need to get into how
engineering does it... code is just a reference point" — I had drifted from
product into implementation detail on a merged auth branch, which was not the
job. **The tell for that drift: I was reading a service file line by line
without being able to say which sheet sentence it would change.**

**Working note, 16 September, third round.** He said "I seem aligned, but explain
point one more simply, getting confused." The confusion was not the wording. A
rule I had written, "a blank floor price equals the asking price", quietly
contradicted his own earlier ruling that the amount is always negotiable. **When
he is confused by something he agrees with, look for a buried contradiction
before rewording.** The worked example (₹10,000 asking, ₹9,000 floor, three
tenants) was what exposed it, so write the example first and the sentence after.

## Rule, added 2026-09-16: reusing the parts is not reusing the component

A "copy to other properties" drawer was rebuilt on a second screen from the
first one's checkboxes, tab list and data hook, with its own layout around them.
The commit message said "uses the house primitives". Side by side it was a
different app: white instead of the plan gradient, pill tabs instead of the top
bar's centred strip, no group cards, smaller tiles, no addresses.

He asked "the property selector UI is so different than Complaint Bot's, or am
I wrong?" He was right, and the thing I had checked (are the imports shared?)
could never have told me.

The rule: when a sibling already has the whole surface, **use the surface**, and
add optional props for the words that differ. Parts-reuse is only right when no
sibling surface exists. The check is visual and it is cheap: open both, measure
width, radius, background and structure, and look.

Here: `CopyPropertyDrawer` gained `title`, `subtitle`, `statusFor`, all
defaulting to its original words, and the lookalike was deleted.

## Working note, added 2026-09-16: "or am I wrong?" is a request to measure

Same shape as every hedge in this thread. The answer was not an opinion about
whether the two looked alike; it was two screenshots and five measurements, and
they said he was right. Leading with "you're right" before measuring would have
been reassurance that happened to be correct.

**Working note, 16 September, the question queue.** Two recommendations he
overturned in one message, and both failures had the same root: **I reasoned
from the record's silence instead of from the running product.** I proposed
dropping "In-person" because no record mentioned visits; visits already happen
every day. I proposed hiding unpriced packages because "nothing without a price
can be billed"; the manager app already ships a Variable Amount package type,
which is exactly the answer. **Before recommending that something be removed or
blocked, check whether the product already does it today.** His "current code is
a reference point" does not mean ignore it; it means it cannot limit the design,
and it is still the cheapest evidence of what users already need.

- **Working note, property onboarding, 16 Sep 2026 (third time).** Before putting any question about a feature that already runs, open the running app for that feature and write one line of what it does today into the question. Three overturned picks in one day (visits, unpriced packages, business verification merged with agreement parties) all skipped this step and reasoned from the records' wording. The note after the first two did not change behaviour; the check has to happen before the recommendation is written, not after he objects.
- **Working note, 16 Sep 2026.** An open row's wording ("goes quiet", "idle") can hide a mechanism already ruled under another name. Sheet 4's steering question was already answered on 1 Sep as "comes back on her next action", recorded for the offer sheet only. Before asking, search the transcripts for the mechanism (the sheet, the trigger, the words said in the room), not for the row's own words, and check whether a sibling surface already carries the rule.
- **Working note, 16 Sep 2026.** He picks the option that is simpler to keep up unless the richer one buys something no existing surface already shows. Before recommending the richer option, name what it adds beyond what is already on screen (the per-step bars already showed the slow work), and put the computation where it can change without a release so the simpler pick keeps the door open.
- **Working note, 16 Sep 2026.** A recommendation to change a drawn screen must be made from a fresh render of that screen, never from the sheet's description of it. Sheet 5 called two stacked groups "sub-tabs" and missed a whole block; the pick built on that description was wrong. Render first, then write the pick.
- **Working note, 17 Sep 2026.** Before any pick that fixes where a thing lives or who may change it, check it against the domain rulings that set the shape of the data (here: one property in RentOk is often several buildings, ruling 37). He had to remind me of a ruling this suite already records in three sheets. Grep the ruling records for the domain model before writing a scope pick.
- **Working note, 17 Sep 2026.** A gap in how the product models the real world (more than one basement) is not something to "leave until an operator asks". The revamp's bar is the real building, not today's data; name the gap and put it in scope with its cost, and let him defer it if he wants.

## Rule, added 2026-09-17: count the notice languages on a module

A module can pass every per-screen check and still look bad because it speaks
several notice languages at once. The agreement module had five: Chakra's stock
blue `Alert`, an amber custom notice, a hand-built warning card with an orange
`Badge`, a coloured dot sentence, and a hand-typed amber hex. He said "alerts
etc make it look really shitty, am I wrong" and he was not.

The test: `grep -n "<Alert\b\|<Badge\|colorScheme=\"orange\"\|#[0-9A-F]\{6\}"`
across the module, list every warning or info surface, and require them to be
one primitive with tones. Here that is `LiteralNotice` in
`components/Settings/AgreementTemplateLibrary/kit.tsx` with `tone="warning" |
"info"`.

## Working note, added 2026-09-17: a leaf-only DOM check cannot see a Tag

A visibility check that only counts leaf elements reported an applied-filter
chip as missing twice. Chakra's `Tag` holds its text beside a close button, so
it is never a leaf. The screenshot showed the chip. When a check and a picture
disagree about text, read the picture, then fix the check.
- **Rule, 17 Sep 2026: a cross-document citation names the section and the row's own words, never a line number.** Sheet 27 cited `sheets/25:103` for a row that moved to 107 the same afternoon, and the stale line then argued against the sentence. Line numbers are for code in a pinned repo; documents under edit are cited as "sheet 4, part 2.3, the row for step 10".

- **Rulings stand over code (17 Sep 2026).** When merged or in-progress code differs from a stakeholder ruling, the code gets a fix issue; the ruling is not re-asked or dropped. Ask only when the ruling itself is unclear. He had to say it after three code differences were queued to him as questions.

- **"You decide" gets its own label (17 Sep 2026).** When he hands a decision over ("u the expert, figure out & decide"), record it as decided by Claude on his instruction, quoting the instruction, never as his ruling; and still check the product before deciding.

- **Delegated calls still carry his known lean (17 Sep 2026).** Handed "you decide", I picked one smallest-level price on public cards and a stricter step-4 done rule; he reversed both: accommodate every seeker (show every level), and one linked room is enough (all is the aim, not the bar). When deciding for him, prefer the option that serves more people and blocks less.

- **Check the phase line before deciding anything money-shaped (17 Sep 2026).** He had said many times that payment modes, banks, reminders, fees, late fines, discounts, GST, TDS and vendor are version two (reference 21, phase two). I decided a "fold them now" answer without reading that list and he had to repeat it. Before any decision on a money field, read the project's phase list.

- **Each form edits only its own record (17 Sep 2026).** A room's form edits the room; a rental option is edited only on its own screen. "Reached from a room" means the room links to the option, not that the room edits it. He had to correct this.

- **His lean: capture in the flow, suggest, never block (17 Sep 2026).** Asked whether a tenant needs a room with an option first, he chose room-only with an in-flow suggestion (link the closest option or create one from what she typed). Same lean as "every level priced" and "one room finishes step 4". When picking for him, prefer the path that asks in place over a prerequisite.

- **Do not recommend merging controls the live app already separates (17 Sep 2026).** I picked "one switch" over Available and Publish; he answered they are two things with two states each. A live control with its own meaning is kept unless he says otherwise.

- **Recall what was already agreed before framing a question (17 Sep 2026).** I asked "which three questions does Rio ask" when the agreed design was Rio suggesting variations outright (AC and Non-AC per unit type and sharing) for multi-select, with Add Custom. He had to restate it. Read the sheet's own step description and the ruling record before turning a dimension list into questions.

- **Rule (2026-09-17): force every load's error state before calling a screen done.** Stub the read with `page.route(re.compile(url), lambda r: r.fulfill(status=500, ...))`. In one module, three failures passed for something else: a blank editor whose Save would overwrite the agreement, "No matches" for a failed room list, and "no content" behind a raw "Bad Request" toast. A toast plus the empty state is how a failure passes for "nothing here".
- **Working note (2026-09-17): a redesign is not done until it has been diffed against production capability by capability.** He asked "is it only better, never worse?" after twelve rounds. The answer was no: across 275 capabilities, 31 were worse and 11 missing, and a production wizard had been deleted with no sign-off. Run the parity audit before calling a redesign mergeable, not when he asks. Method: one reviewer per surface reads `git show origin/main:<file>` against the branch and fills a same/better/worse/missing table with file:line on both sides; then verify every worse or missing row yourself.

- **Audit every decision reason for "because the code/record does it" (17 Sep 2026).** Five of my decisions leaned on the current screen or record shape ("as it is", "today's record holds one frequency", "merged suggestions work without Rio", narrowing E5 to what Rio's code admits). He restated: current code and data are the reality to change, never a limit. Before recording a decision, reread its "why"; a code or data reason is evidence, never the reason.

- **A delegated call that would bend one of his own rulings goes back to him (2026-09-18).** "u the expert, decide" covers questions his rulings already lean on; before closing each one, check the recommendation against every earlier ruling it touches. Onboarding sheet 4 decision 12 (open step 2 on day one) looked decidable until it met his rule that the position line names the first unfinished step.

- **Filter sheets: fewest groups, names from the live product (2026-09-18).** He merged three filter groups into one and said "do not invent a new name, we already have something similar". Before naming any filter group, read the live app's filter helpers first (for rooms, `lib/property/room/room_filter_helper.dart`: Room Facilities, Vacancy Type, Unit Type, Sharing Type) and the drawn filter sheets. Something that says what the thing IS (unit type) belongs in the chips, not the sheet.

- **Filters are a system, not a list (2026-09-18).** Any filter group whose values she can extend (amenities, highlights, services) is built from the values that exist in the current view, with counts, never a fixed list; and every "left out" reason is checked against the rulings before it ships (I dropped gender as property-level when he had ruled it onto the option the day before). House pattern for any filter panel: the tenant list brief, Obsidian `RentOk/PRDs/Tenant List Filters/14 — Whole-Screen Redesign Brief.md`.

- **Filters start from a field inventory, not a guess (2026-09-18).** He asked three times whether the rental option filters were complete; the fourth pass finally listed every data point the form, view mode, policy sheets and derived state carry, and placed each one (filter, search, sort, or left out with a reason). That pass found three missing groups and a form with no field for three identity columns. Do the inventory first, on any filter, sort or search surface.

- **A ruling is not recorded until every surface that states the old fact is swept (2026-09-18).** I put the furnishing ruling into the decision row and a design fix and called it done; he had to ask whether the sheet body carried it, then "is this how you think in systems?". The body, two sibling sheets, two briefs, the merged-work record, and sheet 9's room-to-option matching all still stated the old model. After any ruling: grep the whole docs repo for the old fact's words (e.g. `grep -rn -i -E "furnish|cooling|washroom" sheets briefs reference`), fix every current-truth hit, and report the count, before saying it is recorded.

- **A brand site speaks as the owner.** Truth rules (count, attribute, label) set what may be said, never the voice: on an owner's site the facts are "we", headlines carry a promise, not a tally. The ruled motion and material stack (Paper Shaders, GSAP) is part of the first pass. Vilaasa, 18 Sep 2026: rejected as "a directory someone else made"; the resources had been named twice.

- **"Are you satisfied?" is answered with a fresh-eye score, not relief.** Vilaasa, 18 Sep 2026: after he asked to proceed only if I loved it, a separate reviewer scored the home 5/10 against Meridian while I had just called it done. Four scored rounds took it to 8. Run the fresh-eye pass before saying satisfied, and let the reviewer name the ceiling.

- **A correction from him is a sample of a root cause; mine the record before fixing.** 18 Sep 2026 he called it whack-a-mole: I had written a charter from the four things he named. Mining 578 recorded corrections found nine root causes, and the controls that already existed had never fired on brand work (hooks matched .tsx only; truth-check never run). The fix lives in rentok-site-factory/CONTROLS.md and tools/stage-gate.mjs.

- **An action that appears on every page needs its target on every page.** "Send the address home" existed only on the house page; on nine of eleven page kinds it was swapped for a WhatsApp link or opened nothing. Put the dialog in the same module as the trigger, and let a page of many fill one shell from what she chose. (Vilaasa, 20 Sep; proved by driving the flow on a list page and a room page.)

## Rule: what a server-rendered page puts in `props` is public HTML

`getServerSideProps` serialises every byte of `props` into `__NEXT_DATA__` inside the served page.
On an unauthenticated URL that is publication, not transport. So the payload is **allowlisted**
against what the view actually reads, never denylisted: a denylist is correct until someone adds a
column, and nothing fails when it stops being correct. Check it the only way that counts, on a
served page: `curl` the URL and grep the HTML for the field names.

Found live on pay.rentok.com: a cash collector's real mobile number in `partner_phone` on a public
link, while the backend was masking that same number in the picker beside it.

## Working note, 20 Sep 2026: the hedge was right four times running

On the payment page redesign he said, in order: "the empty states feel force-fitted", "am I wrong?
I could be wrong" about discount metadata, "I'm still skeptical whether it handles the scale", and
"Nahi yaar, this does not work". Every one was correct, and each time my first answer was a design
rather than a measurement, the design was thrown away.

What the measurements found, after each hedge: a median of 7 open bills against the 5 I had drawn,
a tenant holding 10 discounts against the 4 I had asserted, 348-character discount names, and a
live PII leak. None of it was visible from a screen, which is the point: **I had audited screens,
and a screen cannot show you a payload or a distribution.** Before designing any surface that
renders stored records, diff the entity's columns against the fields the view reads, and pull the
distribution of every count the layout assumes.

Two of his calls that were his and not mine, and that I argued against once each: the machine's
metal plate stays (I proposed replacing it, and the replacement was a generic checkout), and
discounts get their own sheet (I argued for inline rows on the strength of a field count that was
wrong). After a ruling, build it; the arguing is done.

## Working note, 20 Sep 2026: "a blend of B & A" is a real instruction, not a dodge

Offered two directions with a recommendation, he answered "a blend of B & A". That is not
indecision: A's ledger column and B's paper character were both right, and the reason I had ruled B
out (a counterfoil down the left edge breaks the amount column) was a fault in my drawing of B, not
in B. Turning the perforation ninety degrees keeps both. Two outside screens had already solved it
this way, which I only found because the blend forced a second reference pull.

The lesson for the next fork: when you reject a direction, name the specific mechanism you are
rejecting, not the direction. A mechanism can be swapped; a direction gets thrown away with it.

- **A measured score cannot see the subject of a photograph.** A calm-daylight score picked two washrooms, a suitcase-strewn room and a tilted frame as house heroes out of 215 graded frames. Score for exposure, sharpness and flash to say what a frame MAY carry; choose the hero and the order by eye from contact sheets, and write the choice down (Vilaasa media/picks-graded.json, 20 Sep).
- **The stakeholder measured us against the reference and sent numbers, twice.** Sanchay ran Meridian's own calibration on our build (0 of 42 on the band line) rather than saying "it reads flat", and then ruled on the hero film himself ("no, shoot is not on, use ours"). When a craft verdict arrives as a table, the answer is the same table re-run, not prose.

## Rule: a key stops waiting at the foot of the window the moment the screen has a composition

`margin-top: auto` on a pinned action is right when the screen is one element on a ground: without
it the key floats in the middle of nothing. It becomes wrong the moment real content arrives,
because it holds the key against the bottom of the viewport and opens a measured void between the
content and the thing that acts on it — the same emptiness a redesign is usually called in to fix,
moved further down the page.

Replace it with a fixed gap and keep `position: sticky; bottom: 0`, which gives both: the key sits
with its content on a short screen and stays in reach on a long one or under a phone keyboard.
Measured here: 33% of the viewport empty before, 2% after, at both 390 and 320.

- **A band and the section inside it must not both bring their own vertical air.** Adding a ground to an existing section doubled its padding and left up to 320px of empty ground under the words at 1440; one rule (`section.band { padding-block: ... }`) beats every per-section rule and fixes the whole site at once. Measure it: for each section, content height against box height, and flag slack over a quarter (Vilaasa, 20 Sep).
- **A critic's finding is a claim to check, not an order.** Of ten faults in the 20 Sep director review, six were real and fixed by class, four were wrong (a filter bar said to clip measured scrollWidth == clientWidth; 56 of 56 windows rendered; the "every house" list is computed from each house's record and audited). Answer the wrong ones with the measurement in the process log rather than changing the page.

## Rule: rank a screen by where she is in the journey, never by what the data audit found

A field-level audit tells you everything that exists and nothing about what leads. Ranking by
completeness puts the most thorough thing first, which on an act screen is always the wrong thing:
she got here from a screen that already showed her the list, and what she needs now is the
decision, then what changes it, then, distantly, what it covers.

The test that catches it: name the screen she came from, and delete from this one anything she
already read there — or collapse it to a line. On the payment slip that turned a five-line list
into one line and moved the figure from the foot to the top.

Two smells that mean this has happened: **two heroes** (a figure at the top and another at the
bottom, so neither leads), and **the most valuable slot holding the least valuable fact** (her own
name, a reference id, a repeated total).

## Working note, 20 Sep 2026: he ranked the screen for me, in one sentence

"The hero is the amount I am paying. Second is the discounts. Third is what bills, because I have
already seen the bills on the first screen." That is the whole design, and it arrived after I had
built the screen in the opposite order and shown it to him twice.

What it should have taken: asking, before drawing, what she had just been looking at. The field
audit that preceded this was good work and it is exactly what misled me — it gave a complete
inventory and no ranking, and I shipped the inventory.

He also asked "what if there are 50 bills" about a design that already grouped them, which read as
a wrong question and was not: the grouping was invisible in the render, so from the outside the
slip looked like one line per bill. **When he doubts a mechanism that exists, the mechanism is not
legible in the artifact**, and that is a design defect even when the code is right.

## Rule: a metaphor may only appear where it is literally true

A torn edge means a document came out of a machine. Drawn on a screen where nothing has been
produced yet, it is a prop lying about state, and everything stacked under it inherits the lie.

The test, before drawing any device, texture or material: **name the moment at which this is
true.** If the answer is "it isn't, but it ties the screens together", the thing that ties the
screens together is the type, the space, the colour and the one real asset the product owns — not
a repeated prop. Chrome that is not true does not scale: twenty-two cards of it is a quilt, and at
112 it is unreadable.

And the corollary that cost this session two rounds: **a ruling is not a doctrine.** "The plate
makes sense" was permission to keep a visual world, not an instruction to put metal, paper and a
printer on every screen. When a ruling starts generating decisions on surfaces it was never given
about, go back and ask what it was actually protecting.

## Working note, 20 Sep 2026: "why are you force-fitting everything into paper"

Two rounds of work thrown away, and the cause was mine: he ruled that the plate stays, I turned
that into a rule, and the rule started designing screens. By the end there was brushed metal, a
torn receipt and a printer on a screen whose only job is to show a list of people.

What broke the loop was not more thinking. It was pulling five real payment screens — Wise, Cash
App, Splitwise, Afterpay, Shopee — and seeing that **not one of them uses a container at all.**
The reference set was available the whole time and I had been designing from a metaphor I invented
instead. When he says "industry-scale", that is a literal instruction to go and look at the
industry, not an adjective.

Note also what he had already told me and I had half-done: he said put "You are paying" in the
title and remove the label below. Cash App's heading is "Buy $1 of bitcoin". He was pointing at
the reference pattern from memory, and I kept the receipt anyway.

- **A closed list of places is never shipped: she works somewhere you have not heard of.** One component (input, suggestions, the record's known places as quick picks that fill the field on focus) and one script (debounced, rate-limited, cached, a plain not-found line) beat a 53-option form. Sanchay named this as a class after seeing one select. (Vilaasa place.mjs/place.js, 20 Sep.)
- **The stakeholder measures before he complains, and the numbers are right.** He sent "hero 846px, photographs band 1098px, rooms start at y=2000" rather than "the page feels slow to get to the point". Re-measure his numbers first (all four reproduced), then fix the class, then send the same numbers back.

## Working note, 20 Sep 2026: the paypage cash picker

**His hedge was right again, and it was measuring something specific.** "The full screen is feeling
a bit odd to me. I don't know why. I might be wrong." The screen gave 29% of itself to the only
question it asked. Measure the hedge before answering it; the number is usually the argument.

**He stopped a redesign by asking a question, not by objecting.** "Don't we already have a detailed
screen for dues detail and payment receipt detail?" We did, and it was the same component with one
prop. Read the component before proposing a direction for it, and before filing a fault against it:
two of the faults I had listed on the directions page were already fixed.

**Do not let a claim from the directions page stand once the build measures it.** I wrote "5 to 6
people at rest, about 11 pulled up" as an estimate; the build measured 3 and 8, and the 5 only
arrived after trimming the sheet head. Correct the page, do not quietly let the build differ.

**A refactor silently drops the reasoning in the code it replaces.** Moving the picker into a sheet,
I swapped `preset(list)` for `list[0]` because `rank()` already puts last month's collector first.
They are not the same: `preset` returns nobody where she has no history, so no stranger is pre-ticked
with his name on the send key. Grep what you stopped calling and read why it existed.

**A fixed-viewport probe cannot see a resize bug, and every probe I write is fixed-viewport.**
Nine Playwright measurements across four sizes all passed while the cash sheet was broken the moment
the viewport *changed* — the panel's ResizeObserver does not fire when only the window height moves,
so a peek measured at one height survived into another. He asked to eyeball it in the browser pane
and it showed up in the first screenshot. Add a resize leg to any sheet or sticky probe:
`page.setViewportSize` to a keyboard height and back, asserting the resting point both ways.

**THE PLATE IS A BACKGROUND. Third time, 20 Sep 2026.** "no plate makes sense" · "why are you
force-fitting everything into paper" · "why is the bottom sheet on that machine plate background —
they should be normal, no?" Each time I took a ruling about *one* surface's ground and built a
material system out of it, then dressed the next thing in it. **A background is where content
stands. It is not a skin that travels.** Before putting a product's signature material on a new
surface, say out loud what that surface IS: a sheet is a sheet, a picker is a picker, and only the
screen that literally produces a document gets the press.

**"Did we need to change this at all?" is a question to answer with git, not with reasoning.**
He asked it about the amount figure. `git show origin/main:<file>` showed the live treatment was
fine and the dashed rule and caption were mine, added in passing during unrelated work. Changes
that ride along with a feature are the ones nobody chose. Diff against what ships before defending
a detail.

**Open live beside the branch before answering "did we need to change this?"** Reading the old
source told me half the answer and I reported it as the whole one: I saw that live had no dashed
rule under the figure, reverted the rule, and missed that live also wraps the figure in a pressed
well — the "dial" he was actually naming. Two tabs in the browser pane showed it in one glance.
A source diff shows what a rule says; only the render shows what the screen is.

**Answer "should it be like live?" with the production split, not with taste.** He asked whether
the footer should be one CTA as it is live. Live's single key opens a road sheet; 90 days of
`payments` says 400,683 online against 13,866 cash on this page, so that sheet taxes 96.7% of
payers to serve 3.3%. The answer became "one key yes, road sheet no" and neither of us had to
argue about it. Money-path layout questions usually have a table that settles them.

**One fact, one place — and he keeps finding it in different clothes.** The six-digit screen said
the amount three times (hero figure, discount line, key). The discount sheet said one credit's
state three times (summary line, group heading, the chit's own pill). Same defect, two screens,
found by him both times. Before shipping any screen, list each fact it states and count where it
appears; more than once is the finding.

**"One fact, one place" is not absolute — repetition can BE the message.** I recommended killing the
receipt's trail because it printed one timestamp three times. He pushed back: "don't you think it's
a good trail and redundancy — it shows that everything is instant?" He was right, and the number
settles it: on the online road paid/cleared/credited genuinely are one moment, and that is 96.7% of
payments. The real defect was the FORM, not the redundancy: saying "instant" by repeating a clock
reads as a rendering fault. **Before removing a repetition, ask what it is communicating; if it is
saying something true, keep the message and change how it is said.** My "the ticks are the actual
lie" line was overreach, stated confidently, on a screen I had measured but not thought about.

**A heading derived from state that arrives in two waves will change under the reader.** Not a
cosmetic flicker: he watched a receipt say "Received with thanks", then stop saying it. The rule —
a heading that states an outcome must be derived from the outcome, never from a roll-up over parts
that can still arrive (`steps.every(done)`). Same class as any `router.query`-derived render.

**A filed issue about a screen you are rebuilding is part of that rebuild.** #970 and #971 both sat
open against the cash picker while I rebuilt it, and both were visible in screenshots I sent him —
two "Karan · Partner" rows on his own property. I rendered the list a dozen times and never
cross-checked the issue list for the screen I was in. **Before rebuilding a surface, grep the
tracker for it**; a redesign that leaves its own known bugs in place is a redesign that will be
reported again.

**Query the population before designing the fix, not after.** "Two people share a name, so show
what tells them apart" was reasonable and mostly wrong: 74 of the 76 same-name pairs share the
phone too, because they are one person entered twice. One query turned a decoration into a fold.
The shape of a fix is a claim about the data; check it the way you would check any other claim.

**Zero-sized boxes with correct text mean the environment, not the CSS.** `getBoundingClientRect()`
returning `{w:0,h:0,t:0}` on an element whose `textContent` is right, with no `display:none`
ancestor, is not a layout bug — it is the page never having hydrated. Check the console for 404s on
`_next/static/chunks/*` before reading your own diff again. I spent four probes measuring a broken
dev server and reasoning about my CSS.

**A fallback label is a claim, and an enum's default is where the lies hide.** `MODES[code] ||
['other','Other',true]` looked like graceful degradation and was asserting, on 31,735 receipts in
90 days, that money changed hands on a date when it did not. **Enumerate the live values of any
code you map** — one `GROUP BY payment_mode` over 90 days showed exactly five unmapped codes and
that two of them were not payments at all. Then read what the SOURCE system calls each one
(`getPaymentModeForActivityLog` named all five) rather than naming them yourself.

**And check what the flag downstream actually drives.** The third field was a boolean `recorded`
read by the hero line, the rail card, the trail and the timestamp. Adding a case meant widening it
to a family and deriving `recorded` from it, or three separate screens would have kept saying
"Paid to" about a bookkeeping entry.

**Sample a probe past the timeout it is racing, or it will hand you a false P1.** Checking #983 I
blocked the Cashfree SDK, waited 3,000ms and saw the key stuck on "Opening…" with no message —
which reads exactly like a dead button and is the symptom the issue described. `sdk()` waits
30 x 100ms before giving up; I had sampled at the boundary. At 7,000ms the message renders and the
key resets. **Before filing a stuck-state bug, find the timeout in the code and sample well past
it.** Third probe in this session to report something that was not there.

**A fix can arrive incidentally, and still needs verifying rather than assuming.** #983 was about
an error hidden behind the roads sheet. That sheet was deleted for unrelated reasons, so the issue
was almost certainly dead — but "the thing it described is gone" is not the same as "the tenant now
sees the message". Forcing both failure paths at three viewport heights is what actually closed it.

## 21 Sep 2026, raising the PR

**Rule.** A fixture's phone number, id or code is obviously fake or it is a leak waiting to be quoted: 9000000000, not the number you have been testing with. Caught on the paypage branch, where the fixture beside a P0 phone-leak fix carried a real staff mobile, in the leak sentinel itself.

**Working note.** "Do it only if you're 100% sure" is not encouragement, it is the list: the diff sorted three-dot against a main that has moved, a secret and real-number scan of the added lines, the tests, the lint filtered to the changed files only, a production build in a throwaway worktree because his dev server owns .next, an adversarial review in another model family because it is a money path, and every issue number checked against the code before it goes in the Closes line. Claiming an issue the branch only half fixes is the expensive error: he reads the list, and Nimit reads the files.

## 21 Sep 2026, filing the Autopay backend work

**Working note.** He asked "what about the API contract you said we'd share with Nimit first?" one
turn after I had reported the four tickets as filed and moved on to what the frontend would do. He
was right, and the gap was in my own report: writing a contract into a ticket is not sharing it, and
an unassigned ticket is a proposal in a queue. An assignee check took one command and showed
fourteen of the fifteen things filed that day had no owner. **Before saying a contract is frozen or
a ticket is delivered, run the assignee check and say who holds it.** He tracks the handshake, not
the artefact, and he notices when a step he named is quietly counted as done.

## 21 Sep 2026, the Autopay API contract

**Rule.** Before changing the vocabulary of a column, enumerate every surface that reads it, by
reading those repos, not by reasoning about them. Three different fields were called
`autopay_status`, all integers, none of them the column being changed; two Flutter apps assign raw
JSON into an `int?` so a string crashes `fromJson` and takes unrelated screens down with it, and one
web app would have written the wrong value back. A column's vocabulary is an API even when nobody
wrote it down as one.

**Working note.** Two short messages from him produced the two largest findings of the session, and
neither message said what to look for. "you got the access to the manager app & tenant app too" was
not an access note, it was: your contract is scoped to one surface. "did you go through & understood
everything in systems?" was not a request for reassurance, it was: something you asserted has not
been traced. Both times **the wrong thing was the claim I had made without following the code** (that
setting the Autopay grace period was a harmless operations change; it is also a late fine waiver,
`autopayV2.ts:864-869` into `dues.ts:117-123`). So when he asks whether it is complete, the move is
to list the surfaces and mark each one traced or not, then go and trace the assertion that is
load-bearing and unchecked. Answering with a summary of what was already done is the failure mode.

**Rule, same session.** A field in a spec with nothing in the code behind it is a trace to run, not a
detail to leave. `needs_new_approval` was a field I had written into the Autopay contract because a
screen would obviously want it. Asking what would ever set it found that `autopay.plan_amount` is
written once and never updated, that ten rent-change paths ignore the mandate, and that the debit
engine truncates the bill with `Math.min` and never returns for the rest: 60 live mandates short by
₹80,030 a month, growing on its own. Before shipping a contract, list every field the current code
could not populate, and trace each one.

**Rule, 21 Sep 2026.** Before filing an issue, list what is already filed. `gh issue list --label
<label> --state open --limit 200` takes one command. Skipping it cost five duplicates out of eight
in one session, on a backlog of 65 that an earlier session had already written. The same rule as
enumerating a surface before auditing it, applied to trackers: enumerate first, judge relevance
second.

**Working note, same day.** He gated a large mechanical task on verification: "file all of it on
Linear, only if you are 100% sure, because once it is posted the team starts working and we do not
want 'what the fuck is this, this doesn't even exist'." That gate is what caught the five duplicates
and four wrong readings, including two in tickets an earlier session had filed and nobody had
re-checked. **When he attaches a confidence condition to a bulk action, the condition is the task**,
and the bulk action is what happens afterwards. Doing the bulk action first and verifying later
would have put 65 tickets in front of five engineers with a duplicate rate of 60% on the newest
ones. Also: he answered two of my three closing questions and ignored the third (owners for the
client epics). Do not re-ask; carry it forward as unowned and say so once.

**Rule, 21 Sep 2026, and it is a register rule not a content rule.** An issue opens with (1) what is
wrong in plain words, no code or column names, then (2) who feels it, named, then (3) the evidence.
That holds in **every** tracker, not just the one where the habit was formed. I wrote 57 GitHub
issues that way and then wrote the same 57 into Linear opening with `autopay.plan_amount` and
`Math.min`, because switching tools switched register without my noticing. He caught it with "would
a human be able to read it, an engineer who has not much context of the product". The tell: if the
first sentence names a variable, a table or a function, it is written for whoever already did the
investigation.

## Rule: "too long" is a navigation complaint until you have read every line

A reviewer saying a spec is too long, or has "too much", is reporting that they could not find
what they came for. That is almost never an instruction to delete, and you cannot tell which it
is until you have read the whole source. The cheap fix is a surface table and a read-this-for-your-
ticket map at the top, about forty lines. The expensive mistake is a rewrite from headings plus
memory, which produces a document that reads better and silently drops the warnings.

The tell that you are about to make it: you are "restructuring" a file you have read maybe two
thirds of, and the parts you skipped are the ones with no interesting headings. On 21 Sep 2026 that
would have shipped an Autopay contract with the section its own author called "the important
paragraph in this document" removed, the one saying a string in `autopay_status` crashes two Flutter
apps and turns Autopay off across twenty properties.

**Before cutting a document: read it end to end, then list what the cut removes, then decide.** If
the list contains anything that prevents an outage or a money bug, the answer was navigation.

## WORKING NOTE: his confidence gate is the check, not politeness

"Only if you're 100% sure, satisfied and confident" before an outward action is not him being
cautious, it is him installing the verification step that would otherwise be skipped. On 21 Sep
2026 it was the only thing standing between a clean-looking rewrite and a pushed contract that
could have taken down the manager app. Treat that phrase as an instruction to go and re-derive the
claim from the source, and to report honestly when the answer is no. He would rather hear "I am not
sure, here is why" than get the thing he asked for.

Related: "make it like Nimit would have made it" was a **register** instruction, not a length one.
Engineer-shaped means findable, precise, and organised by what you do next. It does not mean short.
The first reading of it as "make it shorter" is the same class of mistake as writing Linear tickets
for whoever did the investigation.

## Rule: read every source that names the surface before writing a line about it

Not "enough to start". Every source that names it. On 21 and 22 Sep 2026 a manager app document was
written three times and corrected three times, and each correction came from a file that already
existed: four build tickets that each specified a section of it, a diagrams file holding a diagram
that had been drawn again from scratch, a fee map and a legal check that answered a question
escalated to the stakeholder as open, and the repo's own CLAUDE.md saying which files to start from.

Two cheap checks that would have caught all of it:

- `find <repo> -name "*.md" | head -60` before writing, not after. The sources were never hidden.
- Read the repo's own CLAUDE.md or AGENTS.md first. That one file named STATUS.md, the newest
  handoff, the feature map and a writing checker, none of which had been opened.

**The tell:** you are about to write a document whose sections have the same names as files you have
not opened.

## Rule: a second document that restates a first is worse than no document

When the specification already exists and is good, a summary of it becomes a second source that
disagrees with the first the moment either changes. The useful artifact points instead, and carries
only what the specification does not have.

Test before writing a section: can I name what this adds that the source does not already say? If
not, replace the section with a link. On 22 Sep this cut a document from 558 lines to 295 and made
it more useful, because what survived was the part that existed nowhere else.

## WORKING NOTE: he asks the confidence question when he already suspects the answer

"You satisfied and sure and confident 100%?" and "double check once more" are not requests for
reassurance. Both times on 22 Sep 2026 the honest answer was no, and both times the gap was larger
than the previous round had found. The second time, the audit of the gap was itself incomplete and
had missed the fee map, the legal check and the repo's own working rules.

Answer it by going and checking, never from memory, and report the measure rather than a verdict:
"D1 is 124 lines specifying what I wrote in 30" lands, "I think it is mostly right" does not.

Related, and his own instruction: when he says "you the expert, you tell me what to do", he means
stop presenting options. Decide, say what you are doing, and start in the same turn.

## Rule: a finished design that reaches nobody looks identical to a missing feature

An audit that reads components concludes "the screen does not exist" and an audit that reads the
ticket concludes "so build it". On the payment page, 22 Sep 2026, the whole Autopay system was
built (seven states, a sheet, a day grid, a plan that keeps covered rent out of Pay all) and reached
zero tenants for two independent reasons: a flag (`components/PayPage/autopay.js:24`) and a payload
field the backend never sends (`rentok-backend src/controllers/tenant.ts:15082`).

Before writing "does not exist", trace the one value the screen needs from the server to the render.
The difference is worth weeks: one is a build, the other is a flag and a field.

## Rule: count the mentions before naming the sources

Asked which tickets touch a surface, I named eight from memory and the session before had caught the
same habit. `grep -ci "payment page" *.md | sort -rn` named nineteen in one second, and the top hit
by a distance (E5, 25 mentions) was not on my list at all.

Any "the N things that touch X" claim gets counted, not recalled. The conversation names a symptom,
never the scope.

## WORKING NOTE: when two documents he owns disagree, that is his decision, not my synthesis

Kamal's PRD makes the UPI charge the first thing a tenant reads and orders payment methods by cost.
Sanchay's R11, N2, N6 and R63 forbid exactly that. The temptation is to pick the rulings, since they
are newer and his, and write the document as though the conflict were settled.

Wrong shape. It went in as an open question stating both positions and who holds each, with no
recommendation, because the PRD also answers the objection (it claims legal cleared the split) and
that answer is evidence I cannot weigh. A conflict between two owners is surfaced, never resolved
quietly. Recommendations are for forks inside my own scope.

- **Existing app tokens are evidence, never the design bar (22 Sep 2026).** Asked for a prototype, I rebuilt the units list on the manager app's live palette (2px pills, three greys, 12px text) and he threw it out: "looks like an intern did it in sleep". The tokens tell you what ships; the bar is the best screen the product could have. Take the brand's anchor (its blue, its vocabulary) and build a fresh small language around it: warm ground, one ink scale, one accent, real photography, money and occupancy leading the card.

## Rule: a freeze is a design constraint, not a schedule note

`rentok_tenant_package` had no commit since 26 Aug 2026 and the apps were frozen on 18 Sep. That one
fact reorganised a whole surface document: of twenty-two rows, exactly one could ship before the
launch date, and it could ship only because a screen the app already draws is filled by the server.

Before mapping any surface, ask what can change on it and when. A surface behind a freeze has two
versions, and the near one is built entirely out of what the server can say through screens that
already exist. Planning the far one into the near date is planning a release that cannot happen.

## Rule: trace the value from the server to the render, never audit the component

Two guards on the same unwritten preference key failed in opposite directions in the same app:
`!= 2` hid a banner and `!= 0` hid a profile row, both from an unset key defaulting to 0
(`rentok_tenant_package lib/utils/prefs_utils.dart:104-109`, origin/main). A component audit reads
both widgets, finds them complete, and reports the feature as built.

Across three surfaces the same shape held: more interface built than wired. The estimate that comes
out of a screen audit is a build; the real work is a payload, a flag and a saved value. It cuts both
ways, because a wire turned on today republishes wording that later rulings replaced.

## WORKING NOTE: the hook told me to write a file in the wrong repo and I obeyed it

22 Sep: a compaction hook fires "write a handoff in this repo", the working directory was a
different product's repo on an unrelated feature branch, and I wrote the handoff there, then spent a
turn deciding which branch to commit it to. His reply was "what the fuck are you doing".

The question the hook asks is never the question. A handoff belongs where the work is, and the work
was in another repo which already had one, pushed. When an automated instruction names "this repo",
"this branch" or "this file", check that it means the thing the work is about before obeying it.

## WORKING NOTE: "did you factor in all of it?" means a source was used, not read

22 Sep, his words: "did you also factor in all those 23 artifacts... I'm not sure. You tell me, let
me know." The honest answer was no. I had read his 100KB page end to end and then **used six of its
twenty-three sections** for the one surface I was writing, so every claim I made from it was true
and seventeen sections had never been checked against a ruling.

Reading a source is not the same as checking it. A source read for one purpose is unchecked for
every other purpose, and nothing in my own account of the work could tell the difference, because
"I read it in full" was true the whole time.

The fix that worked: count the parts from the artifact itself (`grep -c '<section[^>]*id='` gave
23, matching his number exactly), then build one row per part with a status column, so the unchecked
parts are visible as rows rather than as an absence. Seventeen rows produced four new open questions
and two answers to questions we already had open.

**His number was right and mine was a feeling.** When he cites a count, count it before answering.

## Rule: stamp every derived document with the rule range it was checked against

A check made on 17 Sep 2026 against rulings R1 to R18 was still being quoted on 22 Sep, by which
time there were 63 rulings. Five of its conclusions had quietly inverted, including a day rule a
later ruling replaced. Nothing on the file said which rules it had been checked against, so nothing
about it looked out of date.

Worse, the stale rule had propagated: the review, the built code and a colleague's prototype all
repeated it, which reads as three independent confirmations and is one dead ancestor. Three
artefacts agreeing is evidence only when they were derived independently.

Every derived document ends with the range it was checked against ("checked against R1 to R63, R64
pending"). A reader can then date it in one glance instead of trusting it.

## Rule: check the number the whole project is sized on, first

Every planning document for the Autopay push opened with the same sentence about the size of the
prize, and in five days nobody had measured it. Measured on 22 Sep against production, it was about
nine times larger, which inverts the provider negotiation: margin was being treated as the
constraint when the constraint was time.

The sentence that starts with "this is why we are doing this" is the one to verify first, not last.
It is usually a single query, it is quoted in every downstream document, and being wrong about it
is expensive in a way that no design error is.

## WORKING NOTE: "think in systems" means orders of effect, and he has now said it four times

22 Sep, his words: "I have already told you: always think in systems. 1. First-order effect
2. Second-order effect 3. Third-order effect. What impacts, what it does not."

The shape he wants for a finding is not the finding. It is: what moves first, what that causes, what
that in turn causes, and then, explicitly, **what it does not touch**. That last part is the one I
keep dropping, and it is the one that stops a real finding from becoming a launch blocker. Sizing
the segment above ₹15,000 mattered most for what it left alone: the other 84%, whose path must not
wait on any of it.

Findings written as a list of facts read as a list of problems. The same findings written in orders
of effect tell him what to do and what to ignore.

## WORKING NOTE: my research conclusion got filed under his ruling, and then contradicted him

22 Sep: I appended four conditions to R63 from my own research file. One of them read "no band that
rises with rent". It banned the formula, which was the real risk, and also banned tiering, which is
ordinary pricing. The over-reach then propagated into a surface document as "never size the fee from
rent", and stood against the founder's own stated intent for five hours until he said so.

Two failures, and the second is the one to fix:

- Research conclusions were written into the decision log in the voice of his ruling. That is the
  [[never-file-my-approval-claim-as-his-ruling]] habit again, in a new shape: not claiming approval,
  but attaching my reasoning to his number so the two become indistinguishable.
- **The ban was drawn wider than the evidence.** The legal source said a fee "must not be sized to
  MDR". I wrote "must not rise with rent", which is a bigger claim and is false. When a source
  forbids a mechanism, ban the mechanism, not the whole family it belongs to.

The repair that worked: strike the clause visibly under the original, dated and attributed to me,
rather than editing it away; put the replacement to him as an open question; and separate the two
things the wide ban had merged (a ladder of published prices is fine, a rate computed from the
payment is not). Same suggested number either way; the difference is provenance, and provenance is
what sits in our own screens.

**When he says "I hope you get that", he has already noticed the contradiction and is being polite
about it.** Measure it, do not explain the old rule back to him.

## Rule: a defect's blast radius is its reach times what is about to change that reach

Six open defects on RentOk's web check-in looked like low-priority polish: the surface they sit on
reaches 0.51% of properties (438 of 85,591, measured 22 Sep 2026). One deploy of the default-on
ruling takes that to every check-in, at 1,774 new tenants a day. Two of the six then block a person
who is standing in the building unable to finish moving in.

So the severity of a defect is not what it costs today. It is what it will cost on the day of the
switch that is already scheduled. **Before ranking any defect, find the flag that gates its surface
and ask what is planned for that flag.** The ship order usually inverts: the fixes are the
precondition for the switch, not parallel work beside it.

The corollary is the cheerful one. The same measurement tells you which surface is cheapest to fix:
of four surfaces, the one that needed no app release and no link migration was the one nobody had
prioritised, and it was the door every new customer walks through.

## Rule: a control that is saved and never read is a worse defect than one that is broken

Manager web has a setting, "Eligible for tenants joined since", that writes a date to the property
and an entry to the activity log. Nothing in the backend reads it (verified: every hit for
`eligibility_date` in `rentok-backend` origin/master is in the settings save path or the entity).

My first reading was that it was a wave gate breaking a no-waves ruling. The grep inverted it, and
the true version is worse in a more interesting way:

- it makes a promise to the person who sets it, and the activity log confirms the promise;
- it excludes nobody, so nobody ever notices;
- and it looks exactly like an unfinished feature, so the likeliest future is that someone wires it
  up, at which point every property that quietly saved a date gets the banned behaviour at once.

So when a control is found with no ticket behind it, the question is not "is it wrong" but "what
does it do, what does it claim to do, and what happens the day someone finishes it". The answer is
usually: rule it in and specify it, or take it off the screen. **An inert switch that looks live is
the worst of the three**, and it is invisible to every audit that only reads screens.

## Rule: close out a document set with an inventory diff across it, not a read of the newest one

Five documents written over two days, each correct when written. The close-out check across all five
found two drifts that no single document's own review could see: three were missing the ruling range
they were checked against (a convention adopted at document four), and the first document had
silently lost its record of a ruling during an unrelated edit the same evening.

Both were introduced by improving the set, which is the point: **a set of documents drifts through
its own maintenance, and the drift is only visible from above.** Before closing any multi-document
job, run one check per invariant across every file at once: the stamp, the shared ruling, the
cross-references, the file the newest one corrects.

## Rule: a research file is not where a finding gets filed (23 Sep 2026)

Three of the four things wrong around the ₹15,000 split were the same failure, not three failures.
Each had been **found and written down correctly** in `research/kamal-launch-room-check.md`, and none
of them reached an open question, a Cashfree question, a ticket or the map. One of them, "AFA and 2FA
are not enabled on our Cashfree account", is the single thing that stops high rent reaching Autopay
at all, and its own sentence in that file even said "that is not in the feature map".

Research files are where a finding is **worked out**. They are not where it is **filed**. A finding
lives only where someone acting on the work would trip over it: the ruling log, the open questions,
the map, or a ticket. Writing it well in a research file and stopping there feels like completion and
produces none.

**At the end of any check that compares somebody else's material against ours, walk the findings list
and name, per finding, the file or ticket it landed in.** A finding whose only address is the check
itself has not been filed.

## Working note: "how could you have missed it" usually means something narrower (23 Sep 2026)

Sanchay, on the split above ₹15,000: "this is also shown in all the two HTMLs I shared with you
earlier. I think so. How could you have missed it?"

The hedge was right and the accusation was not quite. The split **was** in the record: R16 rules it,
the map carries it, ticket B1 builds it, and Kamal's prototype ships it in code. Defending that would
have been the expensive move, and so would accepting the charge as stated. **What was actually wrong
was smaller, adjacent and worse:** R16's own text still carried a superseded ₹15,000 mandate limit,
the gap between parts existed in no document of ours, and the account-level blocker sat unfiled.

**When he says you missed something and the thing is demonstrably in the record, do not argue and do
not concede. Go and find what is wrong next to it**, because the reason he raised it is almost always
something he saw downstream: here, a close-out line of mine calling the high-rent tail "half the
prize", which reads as though it were not automated. His second sentence, "see what else such things
you have missed", is the expansion rule restated, and it means the close-out shipped without it.

## Rule: a new charge invalidates every "free" promise on the surface (23 Sep 2026)

Adding the Platform fee to Kamal's payment page prototype looked like one row on a bill. It was
three changes, because the page already carried two promises written when nothing was charged:
"Rent handles itself and never carries a charge", and "your rent leaves on the 5th with nothing
added". Both became false the moment a fee sat on the same screen, and neither is near the bill code.

**When a ruling introduces a charge, a fee, a limit or any new deduction, grep the whole surface for
the absolute words before touching the data:** never, nothing, no charge, free, always, any amount,
no fees. Each hit is either still true and narrower than it reads, or now false. Narrow it or fix it.

The narrowing is usually the honest sentence anyway: "never carries a charge" became "never carries a
**UPI** charge", which is both true and the actual thing being promised. And the fee's own row carries
the sentence that makes it legitimate, "same on every way you pay", because a fee identical on cash is
a price and a fee that only appears on one rail is that rail's charge under another name.

## Working note: before building to a ruling, read his newest spoken words on it (23 Sep 2026)

Last turn I recommended "rent + platform fee, limit equal to her dues, no buffer" for the Autopay setup
sheet, citing R46. Sanchay asked me to read his 22 Sep implementation call first. In it, in his own
words, the limit is a ceiling RentOk sets above her fixed dues ("15 ka set kar denge... ya 20 ka").
The "equal to her dues, no buffer" line under R46 was **my** design note ("My design details are..."),
filed beside his ruling, and I cited it back to him as if it were his.

Two habits: a line under a ruling that says "my call", "my design", "my recommendation" is mine, and
gets argued as mine, never quoted as a ruling. And before turning a ruling into a screen, check
NeoSapien for a call newer than the ruling (`search_memories` on the feature name); read the
transcript, not the summary, because the summary of this call dropped the buffer example entirely.

## Rule: a number that must match a vendor's is computed once, by whoever sends it to the vendor (23 Sep 2026)

The autopay ceiling a tenant approves on screen is the same figure the backend sends Cashfree as the
mandate maximum. Computing it in the page as well would give two implementations of one rule that
drift apart silently, and the drift is a tenant approving one number while her bank holds another.
So the backend computes it, the page displays it, and the page makes no offer when it is missing.
A review harness may stand in with the rule at today's values, marked as a sample, never on a live path.

## Rule: two numbers agreeing proves they share a cause, not that they are right (23 Sep 2026)

The setup sheet's new "yours to pay now" matched the pay bar to the rupee (₹29,993), which was the
check I designed. Both were wrong for the same reason: they came from the same `autopayPlan`, which
gave the debit an overdue older rent. Only working the figure out from the bill itself (₹35,193
owed, minus which rent the debit should take under the ruling) showed it. **After a consistency
check passes, do the sum by hand once from the source rows and the ruling.** Agreement between two
readers of one function is the function agreeing with itself.

## Working note: "are you 100% sure?" means the proposal skipped a gate (23 Sep 2026)

I proposed the autopay setup flow from the rulings and Kamal's material alone, with no outside
references, no data on where tenants drop, and no check that the approval hand-off works on iPhone.
Sanchay asked whether I was 100% sure. Closing those three gaps (Metabase funnel, Mobbin, Cashfree
docs), which took one turn, changed three things: the biggest loss is at the bank step, not the
screens I had focused on; Apple and Cash App have no benefits screen and no agreement tick; and a
31-day grid for an eight-day window is noise. **Run the Surface Ready gate's evidence steps before
proposing a flow, not after being asked about confidence.**

## Rule: two amounts on one screen must visibly add up (23 Sep 2026)

The bill's bar said "Total pending dues ₹35,193" and the autopay dock above it said "₹23,193 is still
yours to pay". Both were right and the screen read as a contradiction. Said as a split of the total,
"first one on 30 Sep, for the ₹12,000 rent; the other ₹23,193 stays yours to pay", the two figures
add up in front of her. **When a screen shows a second amount beside a total, name what separates
them, so she can do the sum herself.**

- **Working note (23 Sep, autopay tick):** he trims any word or control the screen already carries ("pending" beside a red total, "your monthly" above a terms line, a second link on one row). Before showing a row, strike what the screen says elsewhere; one control per row.

- **Working note (23 Sep, autopay setup):** a screen he has to read is a failed screen ("feels like a block of text, no one will read it"). Draw the answer (date tiles), make each choice a control that changes the picture, fold the full terms. Icons are generated in the page's own 3D family against its existing assets as references, never Lucide on a 3D page ("you got Higgsfield, Runway").

- **Working note (23 Sep, autopay stepper):** he rejected the one-screen setup ("one screen is really confusing") an hour after rejecting the text ledger. For a money commitment: one decision per screen, a visible "Step n of 4", the consequence drawn beside the choice. Count the decisions a screen holds before merging steps to cut taps.

- **Working note (23 Sep):** when he says "only if 100% sure" and names a source (the tenant-app-revamp repo), read that source in full against the finished screens before the next build. TAR-02 found six defects in screens already called done.

- **Working note (23 Sep, the Rent Coin):** he called the first coin cheap, then asked why Higgsfield was not used. For any generated media, start on the strongest tool he has named (Higgsfield: GPT Image 2.5 xhigh or Nano Banana Pro; FLUX 3 Video with start and end frames), and design the mark first: a proprietary monogram, never a font letter on a generic object.

- **Generated media gets a brief before a render (23 Sep 2026).** He stopped a coin render mid-run: "Before you rush, create a proper prompt for the animation... Refine my idea, extend my idea." For any image or film: storyboard with timings, the exact prompts, the surface it lands in, and a pick, shown as a page; render only on his go. His idea is the spine to extend, not the spec.

- **Map the whole lifecycle before the first screen (23 Sep 2026).** His words: "You are doing whack-a-mole... think in systems." For any multi-screen feature: every surface from finding out to leaving, marked built / redesign / missing, two personas walked across a year, every source prototype rendered and read for its workflows (not its look), his decisions queued with picks. Only then one screen at a time.

## Rule, added 2026-09-23: a sticky bar carries the choice, the amount and the key
The pay page's bottom bar grew to five lines (tick, terms, coin reward, total, key) and covered a quarter of a 375px screen, hiding the bill behind it; he called it clumsy on sight. A sticky bar is where she decides, so it holds the choice, the amount and the key, nothing else. Terms go to the screen the Edit link opens; a reward is stated once per screen, at the moment it is the reason to act (before the tick, not after). A single "put the coin on every surface" commit (pay page a262e35c) planted it on six surfaces, two on one screen. Before adding a line to any sticky bar, list what else on that screen already says it.

## Working note, added 2026-09-23: check who is signed in before deciding who a screen names
I read his "someone else approves" ruling as "Your autopay shows Paid from Papa's account". He corrected it within the hour: setup has no sign-in, so the system never knows who approved; only changes and spending coins sit behind an OTP. Before designing what a screen says about a person, write down which steps of the flow are anonymous and which are signed in; the answer decides what the product can truthfully name.
A sticky bar also keeps one height across its states: the pay page's tick grew 16px when a coin line wrapped, which moves the key under her thumb the moment she ticks. Measure both states' heights at 375 before calling it done.

## Working note, added 2026-09-23: a ruled capability may need no control at all
He ruled "someone else can approve" and I drew a "Someone else will approve" link under the key, then found an older share button saying the same. He had to say it twice: the parent already has the payment link and sets it up from there. Before adding a control for a ruled capability, ask whether the product's existing path already delivers it; a second button for the same outcome is a question she has to answer.


### Working note, 2026-09-24, payment-page story sheet
Two corrections in one build, and both were the same miss.
- **"You left out E-nach as a mode."** R93 ruled that all five ways are designed. I gated e-NACH on a backend link that does not exist yet, so the preview hid a ruled way. Gating on live data is right for tenants. A ruled way must still appear in the preview with a sample.
- **"What do other products show as e-NACH icon, research before creating images."** I generated two icons before looking at a single reference, and his first instinct ("bank icon, na?") was the right starting point. For any new icon or mark, pull references first: Mobbin, the official marks (NPCI brand guidelines), and gateway checkouts. Save the findings (ICON-RESEARCH.md) before any generate call.

## Rule, added 2026-09-24: a pinned footer holds only what she presses

Sanchay: no disclaimer, note, warning, alert or anything else in a footer. A pinned footer holds keys, links, controls such as the autopay tick, and the figure a key pays (a label and an amount). Every sentence becomes the page's last line, directly above the footer. Airbnb's confirm-and-pay keeps its consent line there, in the page. When a footer would have nothing to press, render no footer, and let the page say it. A disabled key says why on itself ("Enter an amount"). When the only action is to message someone, that message is the key (payment page: `components/PayPage/AskKey.jsx`). Payment-page check, run on 24 Sep and failing on the old code: `node scripts/paypage/footer-text.mjs <link code>`.

## Working note, added 2026-09-24: a sweep is shown as a list before it is built

For a rule that touches every screen, he said "show me the list before making changes". Post the full inventory first: screen, the text there today, and where it goes, with the keeps named. Then build what he approves. His follow-up on one row ("is this the same as pay in advance?") was a check that the move didn't drop an action. Answer it by tracing the branch in code, and check every other row the same way before building.

## Working note, added 2026-09-24: a figure in a proposal is checked before he approves it

My R94 option A said "UPI adds ₹48" and he approved it. Building it showed that ₹48 is the charge on her monthly rent, while the checkout's figure is whatever she pays (₹141 on ₹35,293). I stopped, said the approved text was wrong, and asked again. That was right, but it cost a round. Before any wording in an A/B carries a rupee figure, name the quantity it belongs to (per month, per payment, per transfer) and check that the surface shows that same quantity.

## Working note, added 2026-09-24: a name from the backend is data, not copy
In a copy pass I proposed dropping "Automatic" from due type names ("Automatic Late Fine" to "Late Fine") and built it when he approved the list. He reversed it: "Automatic Joining Fee" and "Joining Fee" are two different charges, and the word is what tells them apart. On the test tenant both existed, and I saw the paid summary drop from "4 more" to "3 more" and argued it was fine instead of reading it as the collision it was. **Rule:** a copy pass covers words we wrote. A name the backend sends (due type, property, room, person) is printed as sent; fixing its case is allowed, dropping or swapping words never is. When a rename makes two things read the same, that is the finding, not a side effect to explain away. Approval of a list does not make an item on it right: an item that edits data needs the data checked for collisions before it goes on the list.

## Working note, added 2026-09-24: his one example is the rule, applied to every line
He gave me a fact (coins come with every bill) and I rewrote the one line he could see was wrong into a line that repeated the obvious ("You keep your 17,000 Rent Coins, and still earn them"). He had to say it: "if nothing happens to the coin, why do you even need to show it... There is just one example. Did you take that in factor?" The same fault was in six more lines and one line was false ("No fee from RentOk" beside a ₹15 fee). **Rule:** a consequence or pitch line names only what changes or what the thing adds. A line about what stays needs a mistake it prevents, named. When he corrects one line, re-derive the principle and run it over every line of that kind before answering, not after.

## Working note, added 2026-09-24: read a rule's scope before calling it a requirement
I told him NPCI's guideline made the UPI AutoPay lockup "a requirement, not polish" on our screens, and rendered it into six. He said "I'm skeptical, might look odd". Re-reading with his doubt, the "must use" sits in the ads, posters and social pages; NPCI's own merchant checkout (p8) shows the plain UPI mark with words, which is what we already had. **Rule:** when a guideline says "must", find the section it sits in and the example it gives for our kind of screen before quoting it as binding. His aesthetic doubt was the check that caught it.
## Working note, added 2026-09-24: an icon complaint wants a better icon, not a word

**An icon complaint wants a better icon, not a word**. He said the edit pencil looked old; I swapped it for the text "Change" and he came back: "Can you not find or use a better icon". Draw icon options first (bare glyph, glyph in a tinted round button, a filled glyph, the row's own chevron) in the real rows; offer text only as one option among them.
