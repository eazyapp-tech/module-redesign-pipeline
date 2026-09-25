# Traps (this machine and these tools, carried across projects)

Keyed by what you were trying to do. Append one line when a trap costs time; delete when it stops being true.

| Trying to… | Trap | Do this instead |
|---|---|---|
| grep | `grep` is aliased in this shell and prints a summary instead of matches | `/usr/bin/grep` |
| print a separator in zsh | `echo =====` globs and fails | `echo ---` |
| commit with a multi-line message | nested quotes break `git commit -m` | write to a file, `git commit -F` |
| verify at desktop width in the Claude Browser pane | the "desktop" preset is **800px**, below `lg`; "verified at 1440" was verified at 800 twice | `resize_window` with 1440 by number |
| test anything gated on focus or blur in the preview pane | `document.hasFocus()` is false there; `:focus-visible` never fires | Playwright persistent profile (a real window) |
| read a count after a scripted check | scripted checks leave state behind (stacked drawers, open popovers, select mode surviving a resize) | reload between checks; assert "zero open on a fresh load" first |
| reload and check in one `javascript_tool` call | fails with "target navigated" | reload in one call, check in the next |
| test a scroll-collapse header | one scroll event can sit inside a 350ms collapse lock and read as broken | wait past the lock before the return scroll |
| see a stale chunk or hook-order error with clean source | Next cache | kill :3000, `rm -rf .next/cache/swc .next/static` |
| wait on a background agent | `sleep N` is blocked in Bash | `until <check>; do sleep 5; done` with `run_in_background`, or just let the notification arrive |
| read a subagent's output file | it is the full JSONL transcript and overflows context | never Read it; resume the agent with SendMessage and ask for the report |
| measure tap targets on a phone | a 34px chip reads right; a thumb needs 44 | the probe reports `<44`; fix with the `::after` hit-area trick or grow the control |
| trust "the code says the padding is there" | the page said 72 | the number wins; measure |
| verify a sticky column | it can slide 56px before pinning, and mask only its own height | probe: sticky x before/after pan, sticky height vs row height |
| rely on `grep -rn ... --include=*.ts` in zsh | the glob is expanded by the shell | quote it, or drop `--include` and filter with a second grep |
| run a Playwright script while the probe is running | both use the same persistent profile; the second deadlocks and the first hangs with no output | one browser on a profile at a time, or copy the profile dir |
| measure a page for the gate | a page-wide query counts the app shell (38 "0px icons", 51 "open popovers" that are the global sidebar and hidden menus) | give the surface a root id and scope every query to it, or the numbers are unusable |
| check whether two elements overlap | comparing only left/right gives a false positive for elements stacked vertically (reported a 66px "collision" that was a correct two-line layout) | intersect both axes, or read the screenshot |
| measure a tap target | the element box is not the target: `::after` insets extend it, and an `overflow:hidden` ancestor clips it | probe `elementFromPoint` above and below the centre and count how far it still returns the control |
| drive a Chakra drawer/popover in a probe | `[role=dialog]` matches every mounted-but-hidden popover on the page; the first match is usually empty | filter to the dialog that actually contains the controls, e.g. `querySelectorAll('[aria-pressed]').length > 0` |
| click a row by name in a probe | a person row's innerText starts with the avatar initial ("R\\n\\nRavi"), so `startsWith(name)` silently matches nothing and the test passes for the wrong reason | use `includes(name)`, and assert the state actually changed |
| verify a sticky header | it can be pinned and invisible, sitting behind a taller sticky sibling | assert it is on screen (y within the viewport), never just that it stopped moving |
| test scroll behaviour | programmatic `scrollTop = N` batches and can mask a fold/unfold race | drive it with real `mouse.wheel` events and a pause between them |
| drive a control in a probe | a generic selector matches the wrong one — `input[placeholder*=search]` hit the property sidebar's "Search Properties…" inside a closed drawer, not the board's own search, and the app was blamed for it | select by the exact label/placeholder, and assert the control DID something (row count changed) before judging the result |
| set a React input's value from JS | `value` setter + synthetic `input` event can leave React state untouched, so the feature never actually ran | type with a real keyboard, and prove the state changed (a count, a filtered list) before reading the outcome |
| check whether a drawer or modal opened in a probe | `offsetParent` is `null` for `position: fixed`, so every Chakra Drawer reads as closed and the assertion passes having driven nothing | filter visible overlays on `getBoundingClientRect().width > 0`, never `offsetParent` |
| verify a `::after` tap-area extension | it only counts if nothing paints over it — a later sibling with a background eats it, and `elementFromPoint` returns the topmost element | give the control `position: relative; zIndex: 1` as well, then re-measure |
| compare sticky x before and after a pan | comparing two queries BY INDEX silently pairs different elements once anything re-orders | key the measurement by the element's own text or a data attribute, and compare per element |
| pan-test sticky at a wide viewport | if the board's `minW` is under the viewport width there is no horizontal scroll, so "sticky held" is vacuously true | assert the scroller actually scrolled, or only trust the narrow width |
| count tap targets under 44 | two probes disagreed 2 vs 55 on one surface and BOTH were wrong: trusting a declared `::after` passes dead extensions; measuring with `elementFromPoint` OUTSIDE the viewport returns null, so every control right of the phone fold reads as its own height | measure reach with `elementFromPoint`, clamp x into the viewport, skip off-screen and covered-at-centre controls, credit a child of a >=44 control; the ruler loses 1px per edge, so 42 measured = 44 declared. `ui-probe.js` §7 does this now |
| grow a tap area inside a scroll box | `overflow: auto` on ONE axis clips the other axis too; the 44px extension on a chip inside a horizontally scrolling bar died at the bar's edge (33 measured) | give the scroll box vertical room (`py` + matching negative `my`) or move the control out of it |
| grow a 20px text line to 44 inside a 40px strip | it cannot; the strip clips the extension at 40 | make the control itself 44 tall with a negative margin so the strip does not grow |
| set `position` on an element that already gets it from a spread | the later prop wins silently: `position="relative"` after `{...stickyTypeCell()}` unpinned a whole sticky column on two screens, with no type error and nothing visible until a sideways pan | never re-set a CSS property a spread already sets; `position: sticky` already establishes a containing block for `::before`/`::after` |
| run a scripted check after a layout change | the real mouse is still resting where the last click left it, and 380ms later that cell's hover card opens — the next assertion reads THAT card instead of the popover it opened | `page.mouse.move(4, 4)` between navigations |

- **Why do my file:line citations point past the end of the file?** `awk`/`grep -n` over MULTIPLE files at once: `NR` is cumulative across files, so hits in the second file onward carry offsets, not line numbers. Use `FNR` (per-file) or run one file at a time. Cost a whole finding three wrong citations in the analytics build verification (F47, 2026-08-24).

- **Why did review find my "these rows add up to X" claim wrong twice in one hour?** Writing an adding-up promise from the shape of a list instead of from the actual set of states. Two separate slips in one pass: three rows claimed to sum to a total that has four parts (the fourth was a state the card deliberately excludes), and two rows called overlapping that are mutually exclusive by their own date test. **Before writing that parts add up, enumerate every state in the code and check the leftovers; before writing that two rows overlap, find one record that satisfies both.** And note that *narrowing* a false claim does not necessarily make it true: "the only card whose parts add to a whole" was corrected to "the only card whose parts add to Active tenants" and was still false, with four counterexamples in the same service (analytics Tenant, D29, 2026-08-25).

- **Why did my "today the client computes X itself" claim turn out to be wrong?** A calculation existing in a provider, a controller or a hook is not proof the operator ever meets it. Follow the value forward to a widget that renders it, and follow the screen backward to the provider it actually uses. RentOk's refund ceiling: `refund_provider.dart` computes one and pre-fills a text controller, and it is **dead** (that provider only renders the refund-history card; the controller has zero references in the screen). The screen where the amount is typed uses a different provider that reads the server's figure. The wrong claim had already reached a change-map row and an open GitHub issue (#6573) before anyone traced the last hop. **Two greps close it: does anything outside this file read the variable, and does the screen file reference the controller at all** (money model workflow sheets, 2026-08-26).

- **Why did my doc's summary table disagree with its own detail table?** Because I wrote the scoreboard by hand while writing the rows, and the rows moved. **Count the detail table with a script and paste the result; never hand-tally a summary in the same document.** Caught twice in one session on the RentOk hint-copy audit: the intro said 21/17/40, the scoreboard said 21/19/38, and the actual 78 rows said 26/23/29. A wrong headline discredits a correct table (2026-08-26).

- **How do I audit help text, tooltips, or a glossary that ships with the product?** Treat every sentence as a claim about a query and check it against that query, never against how it reads. Shipped copy that reads well is the most trusted wrong thing in a product, because it is the only definition the user has. On RentOk's operator glossary, 26 of 78 money explanations were false, and the pattern was always the same: the sentence named what the number IS and never what it EXCLUDES or SUBTRACTS. **Two greps close most of it fast: search the whole copy layer for the words naming each thing the query subtracts (refund, discount, adjustment, write-off) and for the population words (active, old, booking); a count of zero or one across a hundred sentences is the finding.**

- **Why is my link or reference checker reporting good links as broken?** Because it indexed a narrower file set than it checks. A checker that walks `docs/**` for anchors but resolves links pointing at `ground-truth/` will call every one of those fragments missing. **Before editing anything a checker flags, confirm the target file is in the checker's index.** Cost four false "broken anchor" reports on the money-model repo and nearly four "fixes" to links that were already correct (2026-08-26).

- **Why is my SUM subtracting the same discount several times?** Because a column from the *parent* table is being subtracted inside a query whose row grain is the *child*. RentOk's home collection query joins `invoices -> payments_invoices -> payments` and subtracts `p.owner_credits` (a payment-level column) in the SELECT, so a payment settling three bills produces three rows and subtracts the whole discount three times. There is no error and no warning; the figure is just low. **Whenever a SELECT mixes columns from two grains, name the grain of the row out loud before trusting any SUM**, and look for a sibling query in the same file that already dodged it (the tile twenty lines below documented the exact problem and chose not to subtract at all). 2026-08-26, filed as #6644.
- **Why did my grep return "N matches in 0 files" and print nothing?** `grep` on this machine resolves to ugrep, which swallows output on some multi-pattern and quoted-path calls. Use `/usr/bin/grep` whenever a grep reports matches but prints none.

- **How do I re-verify a fix list against a codebase that has moved on?** Read the current code for the function each item names. Never read commit messages, and never trust a diff to tell you an item is closed. Re-verifying 96 open items on RentOk analytics (2026-08-27): three commits sounded like they fixed a named defect and none had, and two defects read as already handled because the guard sits **one layer outside the value it has to change**: `Math.abs(n(x))` where `n()` already floors negatives to zero returns zero forever, and `showChip ? null : null` is a ternary with the same answer on both branches. **Before calling such code a failed recent fix, check whether it is the original state** - both of these were original and the review entries had already described them correctly, and saying otherwise reads as a criticism of whoever committed last. Also expect the reverse direction: check whether any behaviour the owner already ruled correct has since been undone (one had), because a fix list only looks forward and nothing else is watching that.

- **Why is my markdown link checker calling a good link broken?** A naive `\[[^\]]+\]\(([^)\s]+)\)` regex stops at the first `)`, so any link destination containing balanced parentheses - `03 — Analytics Calculation Guide (Vivek).md` - reports as a missing file. CommonMark allows balanced parens in a destination, so GitHub renders it correctly and there is nothing to fix. **Confirm the target file exists on disk before editing a link a regex flagged.** If you want it unambiguous across renderers, wrap the destination in angle brackets: `[text](<path with (parens).md>)`. 2026-08-27.

- **Why does my logged-in Playwright profile still look logged out?** On RentOk Manager web the MANAGER session is a Firebase custom token (IndexedDB `firebaseLocalStorageDb`) plus redux `persist:root`. The `user_id` / `phoneNumber` keys in localStorage belong to the **tenant** branch of `pages/login-new.tsx` and are never written for a manager, so a login probe watching for them waits forever and can close the window on a session that actually succeeded. Check `persist:root` or just load the target page and look for real data. Keep the profile OUTSIDE the scratchpad (`~/.claude/pw-profiles/<app>`) — tmp is wiped and the login has to be done by a human every time. 2026-08-27.

- **Why does scrolling a page in Playwright do nothing?** An app shell with a fixed header often scrolls an INNER container, so `document.body.scrollHeight` is a constant (900 on RentOk analytics) and `window.scrollTo` is a no-op. Find the real scroller by walking elements for `scrollHeight > clientHeight` with a computed `overflow-y` of auto/scroll, stash it on `window`, and scroll that. 2026-08-27.
- **The GitHub repo looks empty, is it safe to delete?** No. `gh api repos/X` reporting `size: 0KB` and zero commits only means nothing was ever *pushed*; the local clone can hold the entire project. Find clones with `find ~ -maxdepth 4 -name .git -type d` and check `git rev-list --count HEAD` before proposing deletion. And before pushing any long-lived local repo to a **public** remote, scan every blob in history for credentials (`git rev-list --objects --all` piped through `git cat-file -p` with a key-pattern regex), not just the working tree: a token in an old commit publishes the moment you push. Flipping the remote to private first is the safe order of operations. 2026-08-29.
- **How do I route an app off direct Anthropic onto a gateway without an adapter?** Don't write one. The Anthropic SDK reads `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY` from the process env, so a bare `AsyncAnthropic()` already points wherever you tell it, and LiteLLM serves the native `/v1/messages` shape (base URL is the proxy root, the SDK appends `/v1`). Set the model name to one the proxy serves, not an Anthropic model id. Two RentOk-specific distortions before trusting the spend numbers you turned it on to get: Databricks-routed entries run ~1.4x Anthropic list, and LiteLLM does not apply cache-tier pricing on that path (it bills every prompt token at full input rate), so a cache-heavy app reads as far more expensive than it is. Give the app its own direct-Anthropic model entry and use the gateway repo's `usage-benchmark.sql`. Also: LiteLLM's OpenAI-compat translation does not round-trip thinking blocks in agentic tool-use (BerriAI/litellm#9790, closed as not planned), which is why non-Claude models are a real port for a tool-use loop, not a config swap. 2026-08-29.
- **Why did one Figma get_metadata call blow up the session?** The official Figma MCP's `get_metadata` on a big section (an annotated act canvas, a screen library) returns 0.2MB to 1.8MB of XML per node, and batching eight nodes multiplies that. The harness persists oversized results to tool-results files; do NOT read those back. Extract only the section name and depth-1 child names with a small python regex pass over the saved JSON, which turns 1.8MB into a 100-line screen list that is all an inventory doc needs. Screenshots go the other way: `get_screenshot` returns a short-lived URL plus curl line, so batch all nodes in one round, then download every PNG in a single bash command before the URLs expire. 2026-08-29.
- **Why do the HTML artifact pages look broken on GitHub?** GitHub never renders .html files, it shows their source; on a private repo there is no htmlpreview/githack workaround and Pages would make the content public on non-Enterprise plans. House fix: a README inside the artifact folder embedding a full-page PNG of each page (playwright-cli `screenshot --full-page`), plus the live claude.ai artifact link and an open-from-clone note. playwright-cli blocks `file://` URLs, so serve the folder with `python3 -m http.server` first. 2026-08-29.
- **How do I read a claude.ai artifact that was shared with me rather than published by me?** `Artifact action:read` refuses with "served to you as a public (non-member) reader". The content is still reachable: open the artifact URL with `mcp__Claude_Browser__preview_start`, list iframe srcs via `javascript_tool`, then curl the `https://<artifact-id>.frame.claudeusercontent.com/_f/<build>/` src directly and strip script/style tags for the text. Also note when diffing a repo copy against a live artifact: the live HTML carries a ~13KB frame-runtime preamble, and any page using mermaid balloons by megabytes because the renderer inlines base64 sprites, so compare visible text, never byte length. 2026-08-29.
- **The artifact HTML looks perfect on claude.ai but garbled when opened from the repo. Why?** The claude.ai runtime wraps every published page in its own `<head>` containing `<meta charset=utf8>` and renders `<pre class="mermaid">` natively, so a source file that declares neither looks fine live and breaks the moment anyone opens it standalone: every non-ASCII byte becomes mojibake (a single `·` used 98 times across two RentOk pages rendered as `Â·` throughout, reading as typos and missing spaces) and each mermaid block shows as a wall of raw source. Always put `<meta charset="utf-8">` as the first line of the source file, and add a guarded CDN mermaid loader (`setTimeout` → skip if `pre.mermaid svg` already exists → dynamic import → `run()`) which is a no-op on claude.ai and draws the diagrams anywhere else. Critically, never screenshot the local file for a preview image before doing this, or the preview ships the same defects. Verify with `document.querySelectorAll('pre.mermaid svg').length` and `innerText.match(/Â/g)`. Separately: viewers of a shared artifact link see a pinned version, so republishing does not reach them until the share is updated. 2026-08-29.
- **`Artifact` refuses my republish saying I have not viewed the live version. What actually satisfies it?** It hands you a saved copy of the live page and requires a `Read` of **every** line of that file, line 1 included, and line 1 is the ~13KB minified frame-runtime preamble. Reading lines 2 to the end is not enough and the second refusal says so. Cheapest sequence: `diff` the saved copy against your local file first to confirm nobody else changed the page, `Read` with `offset:1 limit:1` to clear the preamble, `Read` the rest, then publish. If a refusal then says the content is "identical, resent unchanged", call `Artifact action:read` on the URL once and publish again; re-Reading the handed file does not clear that second guard. Budget ~25k tokens per artifact you update this way, so batch edits to a published page into one republish instead of several. 2026-08-30.
- **The Figma MCP says the file has one page, but I know other pages exist. Which is right?** Both: `get_metadata` with no nodeId lists only the page currently open on the desktop, because the plugin has not called `loadAllPagesAsync`. Other pages are still fully reachable by node id, so a known id works while enumeration silently under-reports. Never conclude a design file is small or a canvas is missing from that listing. Ask the person with the file open to read the page names off the left panel; it costs them five seconds and there is no tooling path to it. Also useful: text content comes back in the `name` attribute of `<text>` nodes, so canvas annotations, dev notes and written reasoning can be extracted wholesale from one metadata dump without a single screenshot, which is far cheaper than reading images and catches notes too small to render legibly. 2026-08-30.
- **Why are my geometry numbers from the Claude Browser pane nonsense?** If the pane is hidden it stops compositing: `screenshot` fails with "the Browser pane is not displayed", and every measurement goes junk rather than erroring — `documentElement.clientWidth` reads **0**, so any `width > clientWidth` overflow check returns true for the whole document and reads as a page-wide layout bug that does not exist. Trust geometry only from a call where a screenshot in the same batch succeeded. Two more things about that pane: a local file outside the project folder loads as a **static snapshot** with scripts blocked and `window.scrollTo` a no-op (`scrollY` stays 0 while `body.scrollTop` takes), which is why a JS-dependent page renders blank there; and viewport emulation via `resize_window` does not apply to those snapshots, so mobile layout cannot be tested that way — assert the media query instead by reading `getComputedStyle(el).gridColumnStart` and walking `document.styleSheets` for the rule. 2026-08-31.

- Why did a research fan-out burn tokens and write nothing? general-purpose subagents spawn their own subagents. A parent told to "read N things" will delegate again, then exit before its children report, orphaning them. Give research agents an explicit "do not spawn subagents, do the work yourself" line, and check ListAgents after dispatch.

- How do I read a claude.ai artifact shared by someone else when the Artifact tool says public reader not enabled? The Browser pane is not signed in and Control_Chrome get_page_content / execute_javascript return "Chrome is not running" even while list_tabs works. Working path: open the URL in the user Chrome with Control_Chrome open_url, ask the user to select-all and copy, then computer-use request_access(clipboardRead) and read_clipboard. Chrome is read-tier so scroll and zoom-by-scroll are blocked.

- macOS shell: BSD `sed` rejects `1{/pat/d}` (use `tail -n +2` to drop a first line) and there is no `timeout` command (use the Bash tool timeout instead). Building a file from a failed `sed` overwrote content once; always build to a temp file and check word counts before replacing.
- `claude -p` launched from inside a Claude Code session can fail with "OAuth session expired"; verify instruction wiring from the docs or a fresh interactive session, not a nested one-shot.

## run_probe.py: python Playwright wants its own headless shell (2026-09-05)

`python3 run_probe.py` failed with "Executable doesn't exist at .../chromium_headless_shell-1155/.../headless_shell" although node's Playwright had chromium-1208 and 1228 installed. The python package pins a different build and its headless shell was never downloaded. Fastest fix without a download: pass `--headed`, which uses the full `chromium-1155` that was present. Otherwise `python3 -m playwright install chromium`.

## Next reads the last of a duplicated key in .env.local (2026-09-05)

`.env.local` declared `NEXT_PUBLIC_ENDPOINT` twice; the lower `http://localhost:3000` won and every brand site 404'd, looking like a backend or SDK fault. Next prints only "Environments: .env.local", nothing about repeated keys. When a request from inside Next goes somewhere the same call from plain node does not, print the env var from inside the running server first.

## Plain-Node ESM tests need the .js extension on cross-folder imports (2026-09-05)

`import { x } from '../inventory/helpers'` resolves under webpack and fails under `node file.test.mjs` with ERR_MODULE_NOT_FOUND. The site-kit helpers are tested by plain Node, so any helper that imports another helper writes the `.js`. Same-folder `./helpers` had never been hit because nothing crossed folders before.
| measure page overflow under mobile emulation | `window.innerWidth` **inflates to contain a horizontal overflow** — it read 738 in a 390px window, so `scrollWidth > innerWidth` compared the overflow with itself and could never fire. An audit ran clean across four properties and five widths while every screen scrolled 348px sideways | take the viewport from `document.documentElement.clientWidth/clientHeight`. The tell is a constant ratio between the two numbers (810/430 and 738/390 are both ~1.89); two tools showing the same ratio is the bug, not the instrument |
| prove a production-only gate by loading the page | a production build may not serve the dev hostname at all (this app's middleware strips `.localhost:PORT` only in its dev branch), and `next build` corrupts `.next` if the dev server is live | stop the dev server, build, then grep the emitted `.next/static` and `.next/server` for a string only the gated code contains. An undefined `NEXT_PUBLIC_*` leaves a runtime lookup the minifier cannot fold, so the code can ship unreachable — absence of the string proves elimination, presence does not prove reachability |
| run a scripted file edit inside a Bash heredoc | a hook can block the whole command before the interpreter starts, so the edit never runs and there is no error — the shell prints nothing and it reads as success | after any scripted edit, `grep` the file for the new text. Never treat "no error" as "it changed" |
| gate a push on a scan in one command | `scan && push` proceeds when the scan's own regex errors, and an inline `|| echo "clean"` prints clean on failure | run the scan as its own call, read its verdict, then push. A scan that cannot fail is worse than none because its green line is used as evidence |
| review money code adversarially | `/thermos` is reserved for explicit user invocation and cannot be called by the model or reconstructed | dispatch the available review agents in parallel, and add a different model family: `codex exec --skip-git-repo-check -c model_reasoning_effort=high "<prompt>"` from the worktree. Tell each to assume at least one bug exists |
| screenshot a component whose image source is set in an effect | the SSR HTML contains no `<img src>`, so an HTML probe reports the art missing while the render shows it | assert on the screenshot for art, on the HTML for text and structure |

## A live hook can block the very command that would fix it

Moving a hook's script and repointing `settings.json` afterwards locks Bash out: the hook errors on
every command, including the one that would correct the path. Repoint `settings.json` FIRST, then
move the file. If already stuck, edit `settings.json` with the Edit tool, which does not pass
through the Bash matcher.

## A back control that tests a framework internal can be dead from the day it is written (2026-09-14)
Next's pages router in 13.5 writes `{url, as, options, __N, key}` into `history.state`. **There is no `idx`.** So the common `window.history.state?.idx > 0` test for "is there a step behind us" is false on every screen forever, and a back control built on it silently never steps back. On pay.rentok.com's `/p2` it had been dead since the day it was written and nothing showed, because the fallback lands on the same screen the step back would have.
Check it in one line before trusting it, in a real browser on the real page: `await p.evaluate(() => window.history.state)`. If you see `key` and no `idx`, the test is dead.
**The obvious replacement is also wrong, and it was written into this file before it was caught.** Capturing `window.history.length` at module scope and comparing answers a DIFFERENT question: has the history grown since this document loaded, not is the entry behind us ours. The two agree until she steps back. Open the screen directly from a kept link, go one step deeper, come back, and the count is still high while the entry behind her is whatever sent her the link, so the control takes her out of the site. Measured, not reasoned: `scripts/paypage/journey.mjs` in eazypg-marketplace, the section "a kept link straight to the amount screen, then into cash and back".
What actually works is re-implementing `idx`: stamp each entry with its own depth after a push of ours, read it back off `history.state`, and treat an unstamped entry as zero. Anything we did not create reads as not ours, so it fails safe by construction rather than by the count happening to be right. `components/PayPage/Machine.jsx`, `depth()` / `noteStep()` / `hasStep()`. Stamp after a push only: a replace stands in for the entry it overwrites and inherits that entry's depth.

## A hostname can contain the path you are matching (2026-09-14)
The payment page is served from `pay.localhost:3012`, so a Playwright `waitForURL(/\/pay/)` or any regex testing a full URL for `/pay` matches **every** page on that server, including the bill. It resolves instantly, the script races ahead of a navigation still in flight, and reports a failure that is not there. Cost a false "the fix does not work" on a fix that did.
Match the route, never the host: `/\/p2\/[^/]+\/pay(\?|$)/`, or test `location.pathname` rather than `href`.

## Editing next.config.js kills a running `next dev` (2026-09-14)
Separate from "`next build` corrupts `.next` if dev is live". The dev server watches the config and reloads it, so a config edited to add a temporary `distDir` takes the server down the moment it is saved, and a syntax error in that edit takes it down silently: the next request answers nothing and the failure looks like the code. If a build has to run beside a dev server, expect to restart dev afterwards and verify it answers 200 before trusting any check you run next.

## A sweep over many states rate-limits the production API, and a slow state looks like a broken one (2026-09-14)
Walking all fifteen payment-page bench links back to back drew `429` from `apiv2.rentok.com`, and the state that happened to land in the throttle rendered late. A loop with a fixed `waitForTimeout` then reported it as "tapping Pay does nothing", which is a false P1 on a money path. Re-run on its own it navigated in one second.
Two habits: wait on the thing (`waitForURL`, `waitForLoadState`) rather than on a clock, and **re-run any single failing state alone before writing it up.** A state that fails in a sweep and passes alone is the sweep's fault, not the page's.

## A restore chained after a long command may never run, and leaves broken code in the tree (2026-09-14)
Breaking code on purpose to prove a check catches it is the right habit, and the restore is the dangerous half. `sed -i '' 's/GOOD/BROKEN/' file && node long-check.mjs; cp backup file` looks safe. In this harness a command over 120s is moved to the background, and the restore did not take: the file still carried `// BROKEN ON PURPOSE` afterwards, and the notification said the command completed with exit 0.
**Verify the restore, never assume it.** Grep the tree for the marker as its own step: `grep -rn 'BROKEN ON PURPOSE' <paths>` should print nothing before you commit. Better, put a unique marker in every deliberate break precisely so one grep finds all of them, and never chain the restore behind the check.

## A synthetic tap can fail to land while the page is perfectly fine (2026-09-14)
Checking that a whole card was tappable, `page.mouse.click(x, y)` and `page.touchscreen.tap(x, y)` both did nothing at points where `document.elementFromPoint(x, y)` returned the right control AND clicking that control opened the record. Three rounds were spent suspecting the CSS, which was correct the whole time. `locator.click()` works; raw coordinates did not.
For a question about REACH, ask the question hit-testing actually asks, in the page: what is under this point, and does that thing do the job. `elementFromPoint` at the corners and the centre, resolved with `closest()` to name which control was hit, answers it without depending on synthetic input landing at all.


## `lsof -ti:<port>` does not tell you who owns a port (2026-09-15)
It lists every process holding a handle on that port, including client
connections. On 2026-09-09 it returned a Claude Desktop helper pid first for
3007, which was read as "this port is not ours", and a redundant second dev
server was started on another port. The handoff then recorded that wrong fact
for a future session to trust.
Use instead, and read the cwd, not the pid:
```
for pid in $(pgrep -f "next dev"); do
  echo "$pid $(lsof -a -p $pid -d cwd -Fn | grep '^n' | sed 's/^n//')"
done
```
Run here 2026-09-15: it correctly named 3007 as this worktree's own server.

## Chakra `noOfLines` truncation is invisible to a scrollWidth check (2026-09-15)
`noOfLines` compiles to `-webkit-line-clamp`, which clips at the line box, so
`scrollWidth === clientWidth` even while the text renders with an ellipsis. A
probe asking `el.scrollWidth > el.clientWidth` returns false on a visibly
truncated name. Measure the box width against the rendered string instead, and
vary the label, not just the viewport: two Agreement names differing only in a
trailing `_1` both render as "Default Proper…" below about 1024px.

## Capturing a logged-in app to PNG files, without moving credentials (2026-09-15)
The Claude browser pane holds the login but its screenshot returns an image to
the conversation, not a file, and exporting the pane's `authToken` to seed
Playwright is blocked as credential materialization. It should be.
The working route is the chrome-devtools MCP: its Chrome carries the user's own
profile, so it is already logged in, and `take_screenshot` accepts `filePath`.
Two constraints found here:
  - `filePath` must sit inside a configured workspace root. The session
    scratchpad under /private/tmp is NOT one. A directory inside the primary
    repo works.
  - `resize_page` has a floor near 500px. For 375 use
    `emulate` with viewport "375x812x2,mobile,touch", then reload; innerWidth
    then reports 375 rather than 500.

## Figma upload_assets: the first URL of a batch fails (2026-09-15)
Across two batches (14 and 6 assets), the POST to the FIRST submitUrl returned
an empty body while every other URL in the same batch succeeded. Re-requesting
a single upload URL and re-POSTing that one file worked both times. Budget one
retry per batch rather than treating it as a bad file.
Sizing note: uploaded images are placed in uniform 400x300 frames regardless of
their real dimensions. Resize each frame to the image's true aspect ratio
afterwards with `use_figma`; FIT and FILL then agree and the letterboxing goes.

## Killing the MCP's Chrome to free its profile: what actually happens (2026-09-15)
**CORRECTED the same day. The first version of this entry was wrong in its
conclusion and would have cost a future session a whole gate.**

What I first concluded: the app's JWT is a session cookie, so killing that
Chrome logs the app out permanently and only a person can log back in.

What is actually true: **the login comes back on its own.** Firebase keeps its
refresh token in localStorage, which survives the process, so the app
re-authenticates itself on the next load. The `/login-new` page I saw straight
after the kill was the app mid-refresh, not a dead session — I read a transient
state as a permanent one and declared a gate unrunnable on the strength of it.
The probe then passed on the very next attempt with a longer wait.

The chrome-devtools MCP refuses to attach when a Chrome from a previous session
still holds `~/.cache/chrome-devtools-mcp/chrome-profile`: "The browser is
already running for ... Use --isolated". Killing that Chrome does free the
profile and the MCP relaunches happily. **But this app's JWT is a session
cookie, so the login dies with the process.** That leftover Chrome is usually
the only authed browser on the machine, and once it is gone only a person can
log back in. Entering his credentials is prohibited, so the screen becomes
unprobeable for the rest of the session.

Order the work so that browser is stopped at most once, and never before the
probe:
  1. If the MCP cannot attach, kill the holder ONCE, early.
  2. Do the whole live pass through the MCP.
  3. Run `run_probe.py` LAST, and expect it to need the profile that the MCP is
     holding — so plan for a `--headed` run where he logs in, rather than
     stopping the MCP's Chrome a second time.

Two recoveries that look obvious and both fail:
  - **Copying the profile does not carry the login.** Chrome encrypts its
    cookie store with a Keychain key scoped to the original profile path, so the
    copy lands on `/login-new`. (1.7GB copied for nothing.)
  - **Playwright's bundled Chromium cannot read Google Chrome's cookies**
    either, same reason. `run_probe.py` now takes `--channel chrome` so it can
    launch the installed Chrome against a real profile; that flag is correct and
    verified to launch, but it cannot revive a dead session cookie.

**`--wait` is the whole difference, and 6 is not enough.** The re-auth has to
finish before the probe navigates, and `warm()` only waits `--wait` seconds on
"/". At `--wait 6` the probe reached the login page and reported its buttons; at
`--wait 12`, same profile, same command, it reached the screen. This exact line
produced real numbers here, headless, with nobody logging in:
```
python3 ~/.claude/skills/module-redesign-pipeline/scripts/run_probe.py \
  --url http://localhost:3007/settings/agreement-templates \
  --profile ~/.cache/chrome-devtools-mcp/chrome-profile --channel chrome \
  --widths 375,1440 --wait 12
```
`--channel chrome` is still required: Playwright's bundled Chromium cannot
decrypt cookies Google Chrome wrote (Keychain key, scoped to the browser), and
neither can a COPY of the profile — a copy lands on the login page no matter
what, so do not spend 1.7GB finding that out again.

**The tell that a probe ran against the wrong page rather than passing:** its
findings name controls you did not build. "Login with WhatsApp 37px", "Send OTP
40" is the login screen, and `first content row y: None` at BOTH widths means it
never reached the list. A PASS at 1440 there is a PASS on the login page — which
is the dangerous half, because half of a login-page run looks like success.
Read `first content row y` before you read the verdict.

So: killing that Chrome is recoverable and not the disaster the first version of
this entry claimed. Still prefer not to — the live pass is easier through a
browser that is already warm — but if it happens, wait longer, do not conclude
the screen is unprobeable, and never tell him a gate needs his hands until a
long-wait run has actually failed.

## A dev server can hold the port and still answer nothing (2026-09-15)
`curl` to localhost:3007 returned `000` while `lsof -ti:3007` listed three pids.
The server was up and compiling; it answered 200 about 40s later. A failed curl
plus a held port means "still building", not "down" — do not kill it and start a
second one, which then logs "Port 3007 is already in use" and exits, leaving the
first one to finish anyway.

## Forcing loading and error states from the page, with no source change (2026-09-15)
Both states are otherwise nearly unphotographable: the real call resolves in a
few hundred ms, and network throttling did not help — at "Slow 3G" the list
still came back before a 700ms sample and `document.querySelectorAll(
'.chakra-skeleton').length` read 0.

Patch XHR in the page instead, then remount the screen with Next's router.
Verified here: 46 skeletons and `aria-busy` for the loading state, and the real
in-place error for the failure.

```js
// loading: the call never answers
const open = XMLHttpRequest.prototype.open, send = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open = function (m, u, ...r) { this.__u = String(u||''); return open.call(this, m, u, ...r) };
XMLHttpRequest.prototype.send = function (...a) {
  if (this.__u.includes('agreementTemplate/list')) return;            // stall
  return send.apply(this, a);
};
// error: swap the stall for a dispatched failure
//   setTimeout(() => this.dispatchEvent(new ProgressEvent('error')), 100); return;
window.next.router.push('/home');                 // unmount
await new Promise(r => setTimeout(r, 900));
window.next.router.push('/settings/agreement-templates');  // remount, fetch again
```
Two things to know. The screen must actually UNMOUNT, so route away and back — a
reload re-runs the page's own JS and wipes the patch before the fetch. And the
patch does not always survive a second remount in the same page; if the state
does not appear, reload, re-patch, and push again rather than assuming the code
changed.

## A local backend checkout is not the backend (2026-09-15)

`~/rentok-backend` was **917 commits behind** its remote while I read it as
truth. Three GitHub issues were filed off it with line numbers and conclusions
from a tree that predated two model changes. Two survived re-verification; one
was substantially wrong and had to be rewritten on the issue.

Two facts that made it silent:

1. **The default branch is `master`, not `main`.** `git fetch origin main` fails
   with "couldn't find remote ref main" and a distracted reader takes that as a
   network problem rather than a naming one. `git symbolic-ref
   refs/remotes/origin/HEAD` answers it.
2. Nothing about a stale checkout looks stale. The code reads fine, the greps
   return hits, and the hits are real — just old.

**Before reading any backend repo as the source of truth, run this and read the
number.** Verified here, output was `917`:

```bash
cd ~/rentok-backend && git fetch origin master --quiet && git rev-list --count HEAD..origin/master
```

Non-zero means read through `git show origin/master:<path>` and `git grep
<term> origin/master -- 'src/*'`, not through the working tree.

**What actually exposed it** is worth copying: the frontend dev server talks to
the production API, so calling a real endpoint from the page returned a field
(`is_property_first_party`) that existed nowhere in the local source. A response
field with no definition in the tree you are reading is the tell. When a live
response and a local grep disagree, the live response is right.

## `left: 50%` + `translateX(-50%)` halves an absolutely positioned box (2026-09-15)

A floating dock centred this way shipped clipped on every phone and looked
perfect on every desktop.

An absolutely positioned, shrink-to-fit box with `left: 50%` and **no `right`**
gets an available width of `containing block − left`, i.e. **half**. The
transform moves it back visually; it cannot give the width back.

Measured on `ReadinessDock` at 375: parent 375, pill capped at **188**, the
headline rendered "Two…" while the action button kept its full 93px. At 1440 the
half is 720px, wider than the content, so nothing ever clipped and four rounds of
desktop-first looking never saw it.

```tsx
// wrong: centred, and silently half-width
position="absolute" left="50%" sx={{ transform: "translate(-50%, 0)" }}

// right: centred by layout, full available width, no transform to fight
position="absolute" left="0" right="0" mx="auto" w="fit-content"
```

It also retires the framer-motion trap that lives next door: with no horizontal
transform to preserve, a `y` animation has nothing to destroy.

**How to catch it without knowing the rule:** measure the pill's width against
its parent's at 375, not just its centre. A centred-but-wrong box still reports a
correct centre, which is why a centring check passes while the box is half size.

## A scrollWidth test cannot see a line clamp (2026-09-15)

`scrollWidth > clientWidth` is the usual "is this text truncated" probe. It is
blind to `-webkit-line-clamp` / Chakra's `noOfLines`, which clamps by LINE BOX
and never grows scrollWidth.

Cost here: a measurement reported `clipped: false` for a headline the screenshot
plainly rendered as "Two people are named as…", and I nearly took the measurement
over the picture.

For clamped text, either compare `el.scrollHeight` against `el.clientHeight`, or
take the screenshot and look. When a numeric probe and a screenshot disagree
about text, **the screenshot is right** — the probe is measuring the wrong axis.

## A check file can print "ok" and still fail (2026-09-15)

`console.log("<file>: ok")` sitting mid-file, with assertions appended after it,
means the file prints its success line and THEN throws. Every `| tail -1` and
`| grep ": ok"` reports success while the exit code is 1.

Verified here: `first-party.check.ts` printed `first-party.check.ts: ok` with
`exit=1`. `yarn checks` catches it (it tests exit codes); ad-hoc greps do not.

Two rules. The success log is the **last statement** in the file. And a check is
verified by `echo "exit=$?"`, never by grepping its output — this is the same
lesson as "a check that typechecks may never run", one layer down: a check that
RUNS can still lie about whether it passed.

## A link checker is not a verification, and editing by replacement damages prose

**The trap, September 2026, the property onboarding suite.** Ten documents were
edited to a set of rulings, `python3 tools/check.py` passed, and the work was
reported as verified. That script checks that relative links resolve and that
frontmatter blocks close. **It cannot see a sentence that contradicts the ruling
two paragraphs above it**, and three adversarial reads then found about a
hundred and twenty such sentences.

Two rules. **Name what a check actually covers when you cite it**: "links and
frontmatter pass" is true, "verified" is not. And **a document edited by
targeted string replacement has to be read afterwards**, because replacement
produces damage a grep never finds: a doubled clause where the old sentence was
not fully matched, a dangling "so", and worst, an editorial note dropped inside
a quoted UI string, which destroys the only record of the drawn copy. All three
happened here in one pass.

## A document that cites no frame drifts, and every amendment makes it worse

**Found 16 September 2026, property onboarding, sheet 8.**

A handoff sheet described a screen that is not in the design file: a
four-question create card, an app bar, a button, and a summary line that
actually belongs to a different screen. The screens had been read correctly
once, months earlier. Then the sheet was amended nine times, and **every
amendment was written against the sheet's own prose** because the sheet carried
no node ids. Prose copied from prose drifts, and nothing in the loop can catch
it: a link checker passes, a readability pass passes, a reviewer reading the
document finds it internally consistent.

**The rule:** any document describing a design carries the frame id inline at
each screen it describes. Not in an appendix, not in a map document. Inline,
where the claim is made. The cost is a few characters and it converts an
unfalsifiable paragraph into a one-call check.

**The tell that you are about to make this mistake:** you can describe the
screen fluently and you have not opened it this session. Fluency about a screen
is memory of the document, not of the drawing.

## A read-only harness names the WRITES, not the verb (2026-09-16)

Blocking "all non-GET to the API" to sweep a screen safely refused **485 calls**
in one page load, including `property/refreshToken`,
`property/fetchAllPropertiesForWeb` and `property/getHomeDashboard`. This app
does most of its reading over POST. The screenshots from that pass were of a
crippled app and had to be thrown away.

Block a named list instead, taken from the module's own endpoint map. In this
repo that is `components/Settings/AgreementTemplateLibrary/constants.ts`:

```js
const WRITES = ['/agreementTemplate/create','/agreementTemplate/delete',
  '/agreementTemplate/set-default','/agreementTemplate/commit-policy',
  '/agreementTemplate/update-with-clone-check','/agreementTemplate/detach-tenant',
  '/agreementTemplate/fork-and-link-room','/tenant/editTenantAgreement']
const isWrite = u => WRITES.some(w => u.includes(w)) && !u.includes('delete-impact')
```

Note the exclusion: `delete-impact` is a READ whose name contains `delete`, and a
substring block on "delete" silently empties the delete dialog you were trying to
photograph — so the dialog looks broken and the bug is in the harness.

Verified: with the named list, the same sweep reported `blocked: 0` and every
dialog rendered its real data.

Then assert it: print `window.__BLOCKED__` at the end of every run. A sweep that
cannot say how many writes it stopped has not proved it stopped any.

## Pulling the stakeholder's words from Claude Code transcripts drops his replies

**Found 16 September 2026.** Two filters that look reasonable threw away the
messages most likely to carry a ruling:

- A reply typed under a quoted passage is stored with a leading
  `<!-- attach -->` marker. Any "skip messages starting with `<`" filter, meant
  to drop system text, drops every one of these.
- A reply under a quote contains `> ` lines, so a "skip pasted text" filter
  drops it too.

Both are how he answers a recommendation, so both are where his rulings are.
**Strip the marker, drop only the quoted lines, keep his own words.** Mid-turn
messages also appear a second time as `queue-operation` records; dedupe on
content. Verified by grepping the raw `.jsonl` for a phrase known to be his and
confirming the filtered file contains it. `tools/hiswords.py` in
`~/rentok-property-onboarding` carries the fix.

**The general check: before trusting any filtered corpus, grep it for one
sentence you know is in the raw source.**

## Running the formatter on a file that was never formatted (2026-09-16)

`npx prettier --write` on two component files turned a ~200-line change into a
~700-line diff, because neither file had ever been formatted to the repo's
`.prettierrc.json`. The real edits would have been buried in a PR under
whitespace.

Check first, and only format a file that is already clean:

```bash
git show HEAD:path/to/File.tsx | npx prettier --stdin-filepath x.tsx --check >/dev/null 2>&1; echo $?
```

Non-zero means the committed file is not prettier-clean: do not run `--write`
on it. If a hand edit left a stray brace, fix that line by hand. Verified here:
exit 1 on `TemplateEditor.tsx` at HEAD.

Recovery if it already happened: `git diff -w --stat` shows the real size;
`git checkout -- <file>` and re-apply only the intended edits.

## A detector's "overlap" under a sticky footer is not a defect by itself (2026-09-16)

An overlap check that flags any row under a sticky bar will fire on every
scrolled list with a translucent footer — that is what sticky is for. The
question that matters is whether the LAST row can be scrolled clear. Scroll
every container to the bottom (repeat, so paginated rows load) and compare the
last row's bottom with the bar's top. On the add flow: 110 rooms loaded, last
row bottom == bar top at both widths. Not a defect.

- **A field's fate needs both ends traced** (property onboarding, 17 Sep 2026). The backend sign-up had no email field, which read as "a typed email is dropped"; the app actually writes the typed email into the Firebase account, and a skipped one becomes a made-up `user<phone>@eazypg.in` that the backend then stores and emails. Trace app and backend before stating what happens to anything a user types.

## A broken check on main blocks every check after it (2026-09-17)

`yarn checks` runs `for f in ...; do node "$f" || exit 1; done`. One stale
import in `docs/analytics-redesign/barFamily.check.ts` (a function removed from
`components/Analytics/constants.ts`) made main's checks exit at the first file
for everyone, so the four after it never ran.

Before trusting a green or red `yarn checks`, run the loop yourself and print
each exit code:

```bash
for f in docs/analytics-redesign/*.check.ts; do node --experimental-strip-types "$f" >/dev/null 2>&1; echo "$(basename $f) exit=$?"; done
```

Fix it where it lives: a clean worktree from `origin/main` and its own PR
(here #1010), not inside an unrelated feature PR.

- **demo_leads is not a bookings table** (RentOk production, 17 Sep 2026). Sign-up writes a row with source `manager_signup` for nearly every property (25k rows), so a join to demo_leads says everyone booked a demo. Count bookings with `source = 'Manager App'` (the app form) or the website sources; verified with `SELECT source, count(*) FROM demo_leads GROUP BY 1`.

- **Editing a table row by number hits the first table with that number** (property onboarding, 17 Sep 2026). `s.index("| 5 | **")` on sheet 4 matched the checklist steps table, not part 5's decisions, and overwrote step 5 and 6 with rulings; it went unnoticed for a day. Match on the row's own text, or slice to the section first (`a=s.index("## 5. Open decisions")`), and diff the file after every scripted edit: `git diff -U0 -- "<sheet>" | grep "^[+-]" | cut -c1-120`.

- **A heading-bounded text replace hits the first match.** Handoffs repeat headings per round ("## Next action" three times). `s.index(heading)` cut 706 lines of rounds 1 to 9 and it was pushed, because the staged stat (723 deletions for a name swap) was printed and not read. Use `rindex` for the latest section, and compare the stat to the intent before every push. (2026-09-17)
- **A personal-data scrub that searches for ID-shaped numbers misses names.** The first pass removed Aadhaar, email and phone; tenant names stayed in 12 files and in the PR body. Search the names seen on screen too, and scrub the PR description as well as the repo. (2026-09-17)

- **A local checkout is not the product** (RentOk, 17 Sep 2026). `~/rentok-backend` master was 962 commits (two months) behind `origin/master`; a whole day of "today the backend does X" checks, by eleven agents, ran against it, and three headline claims were wrong (Rio, the flat entity and Apple sign-in were all merged). Before any today-claim: `git fetch origin && git rev-list --count master..origin/master` must print 0, or verify in a worktree at `origin/master` (`git worktree add ~/<repo>-master origin/master`) and pin the SHA in the document. The manager app's `origin/master` may not be its mainline either; check `git for-each-ref --sort=-committerdate refs/remotes/origin | head`.

- **"(owner, date)" in a commit or code comment is not a ruling.** Engineering commits on 17 Sep 2026 cited an owner decision for dropping a ruled step and hardcoding a key; the ruling record is the only source for what was decided.

- **A frame name is not its purpose (17 Sep 2026).** Frame 634:78919 was named "Rental Option Details" and read as an assign screen from its node list; a screenshot shows a read-only Linked Units tab. Screenshot a frame (`get_screenshot`) before writing what it does, and before raising "where does this open from" search the sheet for the ruled path first.

- **Figma MCP "tool call limit" is per minute, not per day (17 Sep 2026).** Parallel screenshot agents hit it within seconds; retrying after a short pause worked for every frame. Run at most two or three screenshot agents at once and tell them to retry before writing CANNOT OPEN.
- **Layer names and drawn labels disagree, and the design file moves (17 Sep 2026).** A 209-frame render found 54 wrong descriptions written from layer names or a two-week-old metadata dump (labels "09" drawn as "04", "eviction settings" frames that are unit settings, design fixes already drawn). Describe a frame only from a render made the same day.
- **A Playwright route regex built inside a generated Python string loses its escaping.** `get\\b` became a literal backslash and matched nothing, so the "error" shot showed the healthy page. Anchor with `$` instead, and look at every forced-state shot before trusting it. (2026-09-17)

- **Narrowing a decision leaves stale copies (17 Sep 2026).** E5 was narrowed to "owner only" in two sheets; four others still said "owner or an Admin" until an integrity read found them. When a decision changes, grep every sheet and reference for its old wording in the same turn.

- **Check the issue claim against every billing path before relying on it (17 Sep 2026).** I filed 6989 as "every recurring package reprices" from one path (`dues.ts` finalAdd); assigned packages already bill from the copied `tenant_packages.payable_amount` (`tenantPackages.ts:198`). A money claim needs every path that bills that thing traced, not the first one found.

- **zsh: `grep -r --include=*.md` fails with "no matches found" (17 Sep 2026).** The unquoted glob is expanded by zsh first, so the command exits and any chained replace silently does nothing. Quote it (`--include="*.md"`) or pass directories, and re-grep for the placeholder after replacing.

- **RentOk production: `room` and `tenant` use `"createdAt"` (camelCase), `property` uses `created_at`; `property.is_verified` is always 0; business verification lives in `business_detail.verification_status = 1`; bills are `invoices.property_fk_id` (17 Sep 2026).** Joining payments and invoices in one EXISTS query times out (504); query them separately.
- **A Chakra toast in this app renders twice** (two toast managers are mounted), so `get_by_role("button", name="Undo").first` targets the hidden copy and times out. Use `.last`, or check `elementFromPoint`. In a live-save script, a failed Undo click leaves the real write in place: restore the state before retrying. (2026-09-17)
- **List thunks write into shared Redux lists.** Dispatching `fetchRoomsV2Thunk` or `filterTenantsThunk` for a side lookup replaced the Rooms and Tenants pages' data. For lookups, call `roomsV2Api.fetchRooms` / `api.post` directly. (2026-09-17)
- **A shallow `router.replace` with `router.pathname` on a host-rewritten brand site writes the internal route into the address bar** (`/_sites/vilaasapg-review-test?...`), and Back then lands on a broken page. Pass the visible path as the second argument: `router.replace({ pathname: router.pathname, query }, `${window.location.pathname}?${visible}`, { shallow: true })`, with `site` removed from the visible query. Seen and fixed 18 Sep 2026, `components/brands/vilaasapg/art/Shortlist.jsx` on `factory/vilaasapg`.
- **Wikimedia Commons thumbnails only exist at its standard widths.** `.../thumb/<h>/<File>/1600px-<File>` answered 400 on 18 Sep 2026; `1280px-` and `1920px-` answered 200. Ask the API for `iiurlwidth` and use the width it returns, or use 1280 and 1920 in a `srcset`.
- A count drawn beside a filter must read the filtered rows. Vilaasa 18 Sep: the door said 8 singles free and the visit picker said 6 free while the answer said 2; both read the whole house. Test every figure in a filtered state, not the default.
- An author `display` rule (img{display:block}, .x{display:grid}) beats the UA [hidden] rule, so hidden elements still draw. Put [hidden]{display:none!important} in every prototype and page base. Vilaasa 18 Sep: the no-photo fallback sat under the door photo.
- A page that shows counts ships with a number audit: every figure recomputed from the data independently of the page code, asserted against innerText (lowercased, CSS uppercases), and run once against a deliberately broken build to prove it fails. Vilaasa 18 Sep: three count faults in one day (door, picker, rules list compared to 0) passed every other gate. Example: rentok-site-factory/runs/vilaasapg/pages/home/directions/audit-numbers.mjs.
- Fontshare's css endpoint (api.fontshare.com/v2/css?f[]=a&f[]=b) returned only the first family on 18 Sep 2026; the second face silently fell back and every capture showed the fallback. One <link> per family, and confirm with [...document.fonts].filter(f=>f.status==='loaded') on the page as built.
- Floating chrome (a search dock, a sticky CTA) shows only in the sections it serves and never stacks with another fixed bar on a phone. Vilaasa 18 Sep: a dock visible from the hero to the footer covered card titles, the map and headings on every screen, and on a 390px phone sat on top of the call bar (about 140px of fixed chrome). No check caught it; a scroll walk at 1440 and 390 did. Walk the page screen by screen before calling it done.
- One photograph, one place per page. The hero, the room-type cards, feature bands and every card's lead must be different photographs; a gallery may hold the rest. Vilaasa 18 Sep: one room appeared three times (hero, single card, Elite card) and four more twice; a fresh-eye review ranked it the top weakness and no check had looked. Assert it: collect every visible-at-rest img src and compare the count with the set.
- Piping a checker into grep (node check.mjs | grep Verdict) keeps the pipeline's exit at 0, so a && chain commits past a FAIL. Vilaasa 18 Sep, 8a308fe went in with card-check failing R11. Gate on the checker's own exit (node check.mjs >log && ...), then grep the log.
- Recraft vector SVGs draw holes as background-coloured shapes painted on top; recoloured or placed on a dark ground they fill in or show as blobs. Clean with rentok-site-factory/research/tools/icon-recipe/clean.mjs (real holes, one 24-unit grid, currentColor), then svgo via npx. For a matching set use Recraft's styles model with the first icon as the style reference.
- **A fixed bar inside a blurred sticky header is trapped by it.** `backdrop-filter` (like `transform` and `filter`) makes the parent the containing block for `position: fixed` children, so a "fixed to the viewport" bar renders off-screen (Vilaasa list shortlist bar at y -28 on a phone, 19 Sep 2026). Put fixed bars outside any filtered or transformed ancestor, then measure `getBoundingClientRect()` against `innerHeight`.
- **card-check mislocates cards that hold a second house link.** A "nearest house" link inside a card makes the climb stop at the inner link and report missing facts. Run `node tools/card-check.mjs <url> --cards=".hcard__link"` (the brand's card link selector); ran here, 11 of 11, exit 0.
- **A generated picture can come back as two or three joined panels.** gemini-3-pro-image returned a triptych and a two-panel "poster" for the Vilaasa home hero (20 Sep 2026); at thumbnail size the seam hid, at hero size it split the frame. Look at every pick at the size it will be shown before placing it, and ask for "one continuous photograph" in the prompt.
- **`git add -A <folder>` takes a parallel agent's new files too.** Vilaasa, 20 Sep 2026: two commits swept another agent's `area*.mjs` and `amenities*.mjs` into mine (undone with `git reset --soft HEAD~1` and `git restore --staged`). When agents share a tree, stage only the paths you changed, then read `git diff --cached --name-only` before committing.

- **A planted audit run can ship the plant.** A build that also runs its own audit with `PLANT=1` wrote the page with the wrong count; the next screenshot showed "3 of 11" gyms. A planted run must never write output (`runs/vilaasapg/site/src/pages/amenities-build.mjs`: `if (!process.env.PLANT) writeFileSync(...)`), and the clean run goes last. (20 Sep 2026)

- **Stripping tags before splitting sentences merges a page into run-ons.** A claim audit over built HTML flagged "See all 11 houses" plus a whole nav as one sentence naming a gym. Turn closing block and inline tags (p, h*, li, a, button, span, b) into ". " before stripping, then split. (Vilaasa claim-audit.mjs, 20 Sep; seen failing, then passing, with PLANT caught.)

- **A closed `<details>` still reports client rects in headless Chrome.** A visibility test built on `getClientRects().length && offsetParent` picked a button inside a closed disclosure and the click timed out; Playwright's own `locator.isVisible()` is the truth about clickability. Keyboard tab order does skip them, so the page was fine and the checker was wrong. (Vilaasa dialog-check.mjs, 20 Sep.)
- **One bare `data-` attribute used as two names silently writes to the wrong element.** `[data-done]` was the filter sheet's buttons and the visit's confirmation line; `$("[data-done]")` on the list page wrote the confirmation into a button and the done screen looked empty. Scope the read (`#visit-box [data-done]`) or rename. (Vilaasa houses-client.js, 20 Sep.)

- **A `pgrep -f "node foo.mjs"` wait loop matches the shell that is waiting.** Two "run after the current pass finishes" jobs each hung forever because their own command line contained the pattern they were grepping for (Vilaasa refs, 20 Sep 2026; ~15 minutes lost, cleared with `pkill -f "while pgrep -f"`). Wait on a marker the work itself writes (`until [ -f out/done ]`, or `grep -q DONE job.log`), never on a process name you also typed.
- **A probe that runs at scroll 0 cannot see a bar that only appears on scroll.** Inigo's foot bar carries the house name and its price and is the answer to "does the price stay with her"; read at the top of the page it does not exist, so the page measured as naming its price once and dropping it. Scroll to half the document height, wait a paint tick, then collect `position: fixed|sticky` elements that intersect the viewport (`runs/vilaasapg/site/refs/read.mjs`, the `pinned` probe). Ran here: Inigo and Cohabs came back true, Cove, Meridian and ours false.

- **YouTube media fetches 403, but the storyboard sheets do not.** `yt-dlp -f bv[height<=240]` on YouTube returned `HTTP Error 403: Forbidden` on 11 of 14 videos in one run (Vilaasa hero-film search, 20 Sep 2026), so "download it and make a contact sheet" is not a reliable way to look at a film. The metadata JSON you already have carries a `sb0`/`sb1`/`sb2` format whose `fragments[].url` point at `i.ytimg.com`, and those plain `curl` fine. Each fragment is a grid of frames spanning the whole film, so two of them is a free whole-film contact sheet with no download at all: `yt-dlp -J --skip-download <url> > m.json`, then pull `formats[] | select(.format_id|startswith("sb")) | .fragments[].url` and curl the first and middle one. Ran here on 11 films, 33 sheets, all 200.
- **Pexels search pages block curl; the download endpoint does not.** `curl https://www.pexels.com/search/videos/<q>/` returns 403 with any header set I tried, and so does Pixabay's search. But `curl -L -A '<a desktop Chrome UA>' -H 'Referer: https://www.pexels.com/' https://www.pexels.com/download/video/<id>/` 302s straight to `videos.pexels.com/video-files/...mp4` and downloads (verified on 26 clips, 20 Sep 2026). So: find ids in a real browser (the pane's `javascript_tool`, reading `a[href^="/video/"]` hrefs), then fetch the files with curl. Do not waste time hunting for an API key.
- **zsh eats `$prev[` as an array subscript inside a filtergraph string.** Building an ffmpeg `xfade` chain with `fc="$fc$prev[$j:v]xfade=..."` dies with `bad math expression: ':' without '?'`, because zsh parses `prev[...]` as a subscript, not as a literal bracket. Brace every variable that is followed by `[`: `"${fc}${prev}[${j}:v]xfade=..."`. (Vilaasa hero cut, 20 Sep 2026.)
- **A single `maxrate` cannot carry both a still aerial and a moving night street.** Eight-shot 1440x900 loop at `-maxrate 620k` looked clean on seven shots and turned to visible blocks on the one handheld night street, because low light plus fast lateral motion is the most expensive thing h264 encodes. Sample frames from the *encoded* file against the master at the hardest shot, never from the master alone. Fixes that worked together: raise the ceiling (620k to 830k, 2.6 MB to 3.6 MB), widen `bufsize` to about 3x maxrate so the hard shot can borrow bits from the easy ones, push `hqdn3d` up (`3:2:5:5`), and slow the shot itself (`setpts=(1/0.75)*PTS`). (Vilaasa hero cut, 20 Sep 2026.)
- **The Browser pane screenshots a playing `<video>` as black.** `readyState` 4, `paused` false, `currentTime` advancing, `error` null, and the frame still captures black (Vilaasa refs/hero.html, 20 Sep 2026). The pane is still the right tool for the page around the video (layout, type, scrim, overflow, that the element loaded), but it cannot verify a frame. Verify footage from the file with `ffmpeg -vf "fps=N/DUR,tile=..."` and say so, rather than reporting a black screenshot as a defect or a pass.

## A fresh git worktree fails its own tests before you change anything

`git worktree add` gives you the tracked files and nothing else: no `node_modules`, no `.env.local`.
`node --test` then dies with `ERR_MODULE_NOT_FOUND: Cannot find package 'axios'` on a file you have
not touched, which reads exactly like a regression you just caused. Link and copy before you believe
a red test in a new worktree:

```
ln -s "/path/to/main/checkout/node_modules" node_modules
cp "/path/to/main/checkout/.env.local" .env.local
```

Run once here: `npm run paypage:test` went 55/56 red to 62/62 green with no code change between them.

## node's ESM resolver does not guess the extension that Next resolves for you

`import { scrub } from '../components/PayPage/scrub'` compiles under Next and throws
`ERR_MODULE_NOT_FOUND` the moment a `node --test` file imports that module transitively. Any module
that a `.test.mjs` can reach needs the `.js` on its relative imports. Cost: one red test that looked
like the worktree trap above and was not.

- **A global full-bleed image rule can turn a positioned hero video into a flow item.** `.band--photo > *:not(.band__img) { position: relative }` made the home hero `<video>` a grid item, so the hero grew past the viewport and the headline fell below the fold with its arrival animation unplayed. Give every full-bleed medium the same class the rule exempts, and check the hero height against innerHeight, not by eye. (Vilaasa home.mjs, 20 Sep.)

## A component file whose name differs only in case from a module beside it renders as undefined

`components/PayPage/Slip.jsx` next to `components/PayPage/slip.js`: on macOS's case-insensitive
disk `import Slip from './Slip'` resolves to the LOGIC module, which exports no default, so React
renders `undefined` and throws "Element type is invalid: expected a string ... but got: undefined"
— naming no file, no line, and no import. It looks like a broken export in whatever you last
touched.

Third occurrence in this repo: `BedPlan.jsx` beside `bedPlan.mjs`, `Handover.jsx` deliberately not
named `Collect.jsx` beside `collect.js`, and now `Paper.jsx` beside `slip.js`. **Give the view and
its logic module different words, not different cases.**

Also: `git mv` on an untracked file fails with "not under version control" and, chained with `&&`,
silently skips everything after it. Use plain `mv` for a file you have not committed yet.

- **Why does my HTML audit report defects that are not on the page?** Stripping tags with a regex to read a page as text ignores `hidden`, so every mounted-but-closed dialog, template and fallback reads as page content. On the Vilaasa audit this produced three false findings in one session: an empty WhatsApp link and an empty Google Maps link that are runtime placeholders filled when their dialog opens, and a "Not updated today" chip that is a fallback which never fires while the data carries availability. Static extraction tells you what is in the document, never what is on the screen: confirm anything that looks broken in a real browser before writing it down. Related but different from the `[hidden]` rendering trap above, which is about CSS `display` beating the UA rule. (2026-09-20)
- **Grep both web storages before reporting lost work.** A walk of the Vilaasa site reported the shortlist as dying on reload, having checked `localStorage` only; the code writes `sessionStorage` (`rentok-site-factory/runs/vilaasapg/site/houses-client.js:191`), so it survives a reload and is lost only when the tab closes. Different severity, different verdict. Search `localStorage|sessionStorage|indexedDB` together, always. (2026-09-20)

## Three widths that are not the width of the text

All three cost a round on one figure, and all three look like a CSS spacing bug:
- **`size` on an input** defaults to 20 characters and reserves that much; in a CSS grid the track
  takes the largest item, so a hidden measuring twin in the same cell is ignored and the field is
  twenty characters wide. Set `size={1}` when a twin is doing the measuring.
- **`ch`** is the width of a zero, so a figure containing commas is narrower than its character
  count, and a right-aligned field spends the difference as a gap on its left.
- **A flex container blockifies a bare text node** and drops the whitespace beside it, so
  `or <b>pay in cash</b>` renders as "orpay in cash". Wrap the label in one element.

## A state machine with three states and styles for two

`.is-day` and `.is-night` had rules; `.is-golden` (16:00 to 19:00, from `Skyline.jsx` `lightAt`)
had none, so the default applied and the property's name sat white on a pale sky at 1.87:1 for
three hours a day. Enumerating the missed state fixes today and leaves the next state to reopen it.
**Invert the default instead**: make the safe value the default and let only the exceptional state
override. Check with `grep -c '\.is-<state>' the stylesheet` for every state the component can emit.

## Overflow on a phone is almost always one of three arithmetic faults, not a design choice

Chased all three in one screen. Check them in this order before touching any spacing:
1. **A grid item's minimum is its content.** `display: grid` without `grid-template-columns:
   minmax(0, 1fr)`, and items without `min-width: 0`, cannot shrink below their longest
   unbreakable run. One 168-character name produced 132px of sideways scroll at 320. This repo has
   now paid for it four times; the pair is the fix, and both halves are needed.
2. **A stylesheet may not be border-box.** Grep it: `grep -c 'box-sizing: border-box' file.css`.
   If the answer is 0 or 1, `width: 100%` on anything with padding overflows by that padding.
3. **A nested bar insets twice.** A container with a percentage margin inside another with the
   same percentage padding.

Find the culprit instead of guessing: in the page, take the first element whose
`getBoundingClientRect().right` exceeds `documentElement.clientWidth`, and print its class.

## A full-page screenshot draws a sticky element where it sits at the top of the scroll

A key that is correctly pinned to the bottom of the viewport appears floating in the middle of a
`fullPage: true` capture, overlapping whatever is at that scroll position. It looks exactly like a
z-index bug. Verify with a viewport screenshot, or measure: read the element's
`getBoundingClientRect().bottom` before and after `window.scrollTo`, and if both equal the
viewport height it is sticking.

- **A generic `data-` attribute will collide with a page's own.** A new place-search component bound to `[data-place]`, which the home page already used for its area doors, so the shared script threw on the first door and every later binding died. Namespace a component attribute (`data-place-search`) and check `document.querySelectorAll` counts before shipping. (Vilaasa, 20 Sep.)

## A `getBoundingClientRect` on a closed `<dialog>` returns all zeros, and reads as a real layout

Four `<dialog>` elements on one page and `document.querySelector('dialog.pay-drawer')` returns the
first one, which is closed. Its rect is `{0,0,0,0}`, which arrives in a measurement table as
plausible numbers — `panelTop: 0` read as "the sheet opened full" and sent me rewriting working
code. Assert `d.open` in the probe before trusting any rect, and select the sheet by its own
modifier class, never by the shared one.

## A later rule in the same stylesheet silently replaces `margin-top: auto`

`.pay-commit { margin-top: auto }` is what pushes a footer to the foot of a flex column.
`.pay-act-commit`, a modifier applied on the same element, set `margin-top: 34px` 1,800 lines
later and won — so the keys stopped being pushed down and stood mid-screen with 335px of empty
ground under them, on a screen that fits without scrolling so nothing looked broken. Clearance
above a pushed element belongs in `padding-top`, never `margin-top`. Probe for it:
`innerHeight - lastControl.getBoundingClientRect().bottom` on any page where
`scrollHeight <= innerHeight`; over ~80px means it is floating, not sitting.

## A scripted CSS delete that walks back to "the comment above" eats its neighbours

Removing `.pay-disc-head` with `i = index('.pay-disc-head {')`, then `rindex('/*', 0, i)` to take
its comment, silently swallowed `.pay-disclist` and `.pay-disclist + .pay-disclist`, which sat
between the comment and the rule. The chits lost their 9px gap and stood flush as one block.
`grep -c pay-disc-head` returned 0 and looked like proof. **A removal is verified by what remains,
not by the absence of the thing removed**: `git diff -U0` the file and read every deleted line, or
grep for the neighbours by name. Fourth scripted-edit miss in this repo — see
`verify-every-scripted-edit-landed` in the auto memory, which covers no-match edits; this is the
over-match direction.

## A second `next dev` in the same project blanks the first one

Starting `npx next dev -p 3099` in a checkout that already had `next dev -p 3014` running made the
running server serve a 200 whose client chunks all 404 —
`_next/static/chunks/{main,pages/_app,react-refresh}.js` — because both processes write the same
`.next`. The page comes back blank with the DOM present and every box 0×0, which reads exactly like
a CSS or render bug you just introduced, and sends you debugging your own diff. Existing memory
covers `next build` against a live dev server; this is the same collision between two dev servers.

**Use a separate build dir**, not just a separate port: `NEXT_DIST_DIR=.next-echo npx next dev -p 3099`
(or `distDir` in a throwaway config). **Recovery:** kill both, `rm -rf .next`, restart the original
on its own port — and restart it, because leaving someone's dev server broken is worse than the
test you ran.

## 21 Sep 2026, measuring for the Autopay spec

**`invoices.due_type` is a name string, not a foreign key.** Joining it to `duetype.id` needs a
`::text` cast to run at all and then matches nothing, so the query returns zero rows and reads like
"there are no late fines". The real filter is on the text:
`lower(i.due_type::text) like '%fine%'`, and production holds at least fifteen spellings of it,
led by "Automatic Late Fine" at 2.05 million rows. The backend's own debit query does the same
thing (`src/services/autoPay/autopayV2.ts:814-817` matches `i.due_type` against a name string).
Ran both forms against Metabase database 2 on 21 Sep 2026: the id join returned 0, the text match
returned 91,795 tenants.

**The same question measured two ways differs by 75%.** "Tenants fined in the last 12 months" is
91,795 across everyone who has ever been a tenant, and 52,550 restricted to current tenants
(`tenant.status = 1`), which is 12.6% of them. Neither is wrong. A number in a document without its
definition beside it will be re-derived differently by the next person and read as a contradiction.
Same for "tenants sent a payment link in 90 days": 278,960 all tenants, 205,166 current ones.

**`autopay_transaction` failures hide in two statuses.** `status = 'failed'` gives 593 debit
failures; `status = 'cancelled'` holds another 113, and every one of those 113 carries
`subscription is not active`, which is the same defect. A count filtered to `failed` alone
understated "debits raised against a dead mandate" by more than three times.

## Verifying a scripted edit in prose: grep the shortest token, because prose wraps

`grep -n "ON CONFLICT ("` reported one occurrence and looked like a complete verification. There
were two: the second had the paren wrapped onto the following line, so the pattern could not match
and the perl substitution had silently skipped it. Greping the bare token `ON CONFLICT` found four
lines and exposed it.

In a hard-wrapped markdown file, any pattern longer than a few words can straddle a line break.
Verify with the shortest distinctive token, then read the hits. Pairs with the existing rule that a
no-match sed looks exactly like a successful one.

## The branch you are committing a note to may not contain the files it cites

22 Sep 2026: a handoff citing `components/PayPage/autopay.js:24` was about to be committed to
`feat/brand-site-system`, which is 321 commits behind `origin/main` and carries no `components/`
PayPage tree at all. The references were read on `origin/main` and are correct there, and
unopenable where the file would have landed.

Before committing any note that carries `file:line`, run both:

```
git branch --show-current && git rev-list --count HEAD..origin/main
git ls-tree -r --name-only HEAD -- <the path you cited> | head -3
```

An empty second answer means either the note goes on another branch or every reference in it names
the branch it was read on. Both commands were run here and produced the numbers above.

## Grep a hard-wrapped document with a short token, or you get a confident wrong answer

22 Sep 2026, second time in this repo. A close-out check for the phrase "Checked against rulings R1
to R63" across five hard-wrapped markdown files reported one stamped and four not. The real answer
was two and three: in two files the phrase straddled a line break, so a line-oriented grep could not
see it.

A check that under-reports looks exactly like a check that found a real gap, and the "fix" then
edits files that were already correct.

For any phrase longer than about four words in wrapped prose, collapse the whitespace first:

```
python3 -c "import re,glob;[print(f, 'R1 to R63' in re.sub(r'\s+',' ',open(f).read())) for f in sorted(glob.glob('surfaces/*.md'))]"
```

Run here, and it corrected the line-grep's answer on two of five files.

## A shared HTML prototype can be an empty page (23 Sep 2026)

Kamal's `RentOk-Payment-Page.html` is 697 KB and its page body is one line:
`<div class="pay-page" id="app"></div>`. Every screen, every word of tenant-facing copy and every
rule is built in JavaScript at runtime. **Strip the tags and you get nothing**, and nothing does not
look like an error, it looks like a page with little in it. Two checks of that artifact had gone by
the launch room's *description* of the prototype instead of the prototype, and a conflict with a
ruling sat in a screen nobody had read.

Check before trusting any text extraction from a shared HTML file:

```bash
python3 - <<'PY'
import re
t=open('FILE.html',encoding='utf-8',errors='replace').read()
body=re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S|re.I)
print('file',len(t),'| after removing script and style',len(body))
PY
```

If the second number is a few hundred bytes against a file of hundreds of KB, the content is in the
script and the text extraction is lying. Read the script instead: strip base64 blobs first
(`re.sub(r"[A-Za-z0-9+/]{60,}={0,2}",' ',s)`, or font data drowns every search), then pull the view
functions and their string literals. The constants at the top of such a prototype are often the
most useful thing in it: this one opened with `DEBIT_CAP = 15000`, `PART_CAP = 1999` and
`SESSION_SECS = 15 * 60`, each one a decision that had been argued about elsewhere for days.

## A script in the scratchpad cannot import the repo's packages (23 Sep 2026)

`node $SCRATCHPAD/shoot.mjs` failed with `ERR_MODULE_NOT_FOUND: playwright` although the repo has it:
ESM resolves bare imports from the **script file's** directory, not the shell's cwd. Copy the script
into the repo tree, run it there, delete it: `cp $S/shoot.mjs ./.shoot.mjs && node .shoot.mjs; rm .shoot.mjs`.

## `invoices.due_date` is a naive timestamp: `AT TIME ZONE` shifts it the wrong way (23 Sep 2026)

`extract(day from due_date at time zone 'Asia/Kolkata')` said 70.9% of tenants pay rent on the 25th
or later and 6,943 on the 1st. The column is `timestamp without time zone` holding IST midnight as
18:30 of the previous day, and `AT TIME ZONE` on a naive value treats it as IST and converts to UTC,
subtracting 5:30 instead of adding it. `extract(day from due_date + interval '5 hours 30 minutes')`
gives 67% on the 1st and 4.5% on the 25th or later. **When a distribution looks absurd, suspect the
time zone before the data.** The backend's own month filter uses plain dates and still links 98.9% of
bills to the right month, so do not conclude the engine is broken from the storage alone: count what
it actually linked.

## NeoSapien transcripts: trust `is_user`, not the speaker labels, and not the summary (23 Sep 2026)

The same sentence routinely appears under two or three speaker labels, and each segment repeats its
own phrases, so a raw read looks like everyone agreeing with everyone. What held up on a 133-minute
recording: the `is_user` field marks the recorder's owner (Sanchay) reliably; everyone else is
attributed by content. The summary gave the length as 78 minutes and listed "AI tools" as a meeting
topic when those were Sanchay dictating to an agent. Read the transcript; collapse the echo first:
`get_memory_transcript` saves JSON; for each segment, repeatedly replace any run of 3 to 40 words
immediately followed by itself with a single copy. That took 133k characters down to 114k with nothing
lost, and made the thread readable.

- **router.replace({ query }) on a host-rewritten Next page** writes the internal /_sites/... path into her address bar. Pass the public URL as the second argument (the bill page `go` helper does). Found 23 Sep on the autopay tick.

- **Bulk-deleting CSS rules by regex** can take a rule's closing */ and leave its /* opener, which silently comments out everything after it until the next */. After any scripted removal, compare the counts of /* and */ (pay-page.css, 23 Sep).

- **Key3D ignores a synthetic element.click()**: a scripted walk that clicks the 3D key reads as stuck when the product is fine. Tap it with the browser tool by ref or coordinate (23 Sep, autopay walk).
- **Reloading the local bill repeatedly hits the backend 429 rate limit.** Space walks out, use a second tab, never reload the tab he is using.

- **A failing `<source>` never reaches React's `onError` (23 Sep 2026).** Two 404 sources left a `<video>` at networkState 3 with `play()` pending, the poster stuck and React's onError silent, both on the element and on the `<source>`. Listen natively on the last `<source>` (`addEventListener('error', …)`), check `networkState === NETWORK_NO_SOURCE`, and add a start timeout. Seen live in eazypg-marketplace components/PayPage/AutopayCard.jsx LaunchSheet.

- **A picture that lives only inside a `<video>` can render as an empty box (23 Sep 2026).** The founder's element capture of "You're set" showed a blank navy stage where the coins should be, while the live pane played fine: DOM-redrawing captures, in-app browsers and battery saver often paint video as nothing. Rule: every film sits over a still of its own frame (`.pay-stage-film`, `.pay-launch-film` in eazypg-marketplace pay-page.css), and the video is removed on `ended` so the final frame is a plain image. Test by hiding the video with CSS mid-play: the screen must still say what it means.

## The payment page's Drawer stays mounted, so a CSS entrance animation on its contents plays at page load
`components/PayPage/Drawer.jsx` opens a `<dialog>` with `showModal()` and never unmounts it. A keyframe with a delay on anything inside runs when the page loads, behind the closed dialog, and is over before she opens it. Gate the moment on state set by an effect on `open`: `data-play="wait"` hides the moving parts while the sheet rises, `"go"` plays them, `"rest"` shows everything (reduced motion, closed). The launch sheet does this (AutopayCard.jsx LaunchSheet, pay-page.css `.pay-launch-stage[data-play]`).

## A white-ground film on a white sheet shows a box, and multiply cannot fix it
Generated renders (MiniMax, GPT Image) have a studio floor that drifts from 253 down to about 244 near the bottom. On a #FFF sheet that edge reads as a grey rectangle. `mix-blend-mode: multiply` does nothing here, because white multiplied by grey is still grey. Lift it in the encode instead: `curves=all=0/0 0.5/0.51 0.935/1 1/1` in the ffmpeg `-vf` for the film, its poster and its still, then sample the corners at 255 (eazypg-marketplace 68daa177, public/paypage/story).

## The Drawer's dialog calls onClose a second time after you close it yourself
`d.close()` in Drawer.jsx fires the dialog's own `close` event, which calls `onClose` again. An onClose that writes state (localStorage, router.replace) runs twice. The second run can overwrite a pick saved by the first, or cancel a `router.push` that is still in flight. Return early when already closed (SaveStory.jsx `close`: `if (!open) return`).
- **run_probe.py `--wait` is in seconds, not milliseconds** (24 Sep 2026). `--wait 3000` waits 50 minutes per page, which looks like a hung browser. Use `--wait 3`.
- **A query-only `router.replace({ query })` on a host-rewritten route exposes the internal path** (payment page, 24 Sep 2026). It resolves against the page's internal route, so the address bar showed `/_sites/payment-pages/p2/<code>?frame=&pick=&sheet=`. Pass the public address as the second argument: `dropParams(router, keys)` in `components/PayPage/Machine.jsx` does this, following the pay bar's tick in Receipt.jsx. It was found by clicking the key and reading `page.url()`, not by a screenshot.
- **The Done Probe's peer-height rule is quieted by stretching a trailing link** (24 Sep 2026). "Controls in one row at different heights" was written for toolbars; on a label-plus-link row, `align-self: stretch` makes it pass whether or not the row looks right. Look at the render first: the real fault (#1071) was the checkbox floating beside the word "month", which the number never named.
- **`!(x < MIN)` is false when x is null** (24 Sep 2026). `null < 300` is true in JavaScript, so a guard meant for "once a limit is known" silenced the recharge's ₹300 note before any limit existed. Write `x != null && x < MIN`, and test the null case.
- **npci.org.in refuses scripted downloads** (24 Sep 2026). curl and the fetch tool get Akamai "Access Denied" or 403. The route that works: fetch the Internet Archive copy (`https://web.archive.org/web/2026id_/<url>`), then open the live file in the Browser pane and check its SHA-256 with `crypto.subtle.digest` against the copy. Rendering a PDF page with no poppler or PyMuPDF installed: split the page out with pypdf, then `sips -s format png -Z 1600 page.pdf --out page.png`.
- **A render baked on white passes on every white sheet** (24 Sep 2026). `autopay-calendar.webp` was opaque RGB; it looked right on the white sheets and showed a white square on the waiting screen's grey, which the Done Probe passed. Check an image's mode before reusing it (`python3 -c "from PIL import Image; print(Image.open(f).mode)"`: RGB has no transparency); the `-clear` twin was RGBA. Opening screens in the Browser pane found it, not the probe.
- **Lifting a logo from a PDF with PyMuPDF** (24 Sep 2026). `set_cropbox` + `get_svg_image` only frames the view; the SVG still carries the whole page (121 KB of other text). Remove the rest with redaction boxes around the mark (`PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED` also drops the page's ground), but a text span is removed if its box touches a redaction box, and a span's box is taller than its letters: widen the kept area to the span's bbox (`get_text('dict')`) or the word vanishes. Check the export by rendering it, not by its fills.
- **A wrapper class ending in "-foot" puts its text under the footer rule** (24 Sep 2026). `footer-text.mjs` reads every `dialog[open] [class*="-foot"]` as a sheet's foot, so a sentence inside `.pay-look-foot` failed it. That was right: the sentence belonged above the key, not beside it. Keep sentences out of foot wrappers; a foot holds only keys.
- **A query-only `router.replace` in Next asks the server again** (payment page, 24 Sep 2026). Every autopay choice waited on getServerSideProps, 0.37 s locally and a backend call per tap. On a page that reads its state from the address, replace shallowly with the internal route as href and the public address as `as` (`sameRoute`, components/PayPage/Machine.jsx, pay-autopay worktree); a plain string href with `shallow` fails under the host rewrite.
- **A bare class inside a row loses to the row's element rule** (payment page, 24 Sep 2026). `.pay-flow-choices span` (0,1,1) turned both a blue "Change" link and a blue pen chip grey, twice in one hour. Scope a new child class under its row (`.pay-flow-choices .pay-flow-edit`) and sample the rendered colour, not the token.
- **A route-driven sheet closes twice** (payment page, 24 Sep 2026). A confirm moves the address on, the sheet's state goes false, Drawer calls `dialog.close()`, and the dialog's close event runs onClose, which navigated back and dropped the confirm's `did=` news. Guard it with the current render's state: `onClose={() => sheet && closeSheet()}`.
- **`-foot` in a class name means footer to the checks** (payment page, 24 Sep 2026). footer-text.mjs reads every `[class*="-foot"]` inside an open dialog as a sheet foot, so a card's closing line named `pay-flow-plan-foot` failed once it sat inside a sheet. Name content lines `-note`.
- **An entrance with `animation-fill-mode: both` pins the transform** (payment page, 24 Sep 2026). The bill's autopay card rose with `both`, and the held end frame beat every `:active` transform, so the card could not be pressed. Use `backwards` for entrances.
- **A pressed-state audit must press, not parse** (payment page, 24 Sep 2026). Splitting CSSOM selectors on commas breaks inside `:where(a, b)`, and a static check read a working press rule as missing. Scroll the element to the centre, check `elementFromPoint` hits it, mouse down, and read the computed transform or opacity.
- **A pinned footer over a control's reach is a scroll position, not a small target** (payment page, 25 Sep 2026). The Done Probe read a bill Pay key flush on the pinned footer as 38px; at every phone height a different key sat on the edge, and scrolled clear the same key read 45. The probe skipped a pinned layer over the centre but not over the edge, so its reach walk now looks through sticky and fixed layers that do not hold the control. Proved against the bug: with the key's reach switched off it still flags all four keys at 33. Before filing a probe tap finding, scroll the control clear and measure again.
- **A production build ignores `pay.localhost`** (payment page, 25 Sep 2026). middleware.js strips `.localhost:<port>` only when NODE_ENV is not production, so `next start` behind a tunnel answered every page with a 404. A tunnel to a production build must present a production host: `cloudflared tunnel --url http://localhost:3013 --http-host-header pay.rentok.com` (scripts/paypage/demo-serve.sh). The label never leaves the Mac.
- **A JSON import breaks the node test runner** (payment page, 25 Sep 2026). webpack takes `import x from './a.json'`; `node --test` refuses it without `with { type: 'json' }`, and three unrelated tests failed because they import a module that imports one. Write fixtures as `.js` modules (`export default {...}`).
- **Compare reduced motion at the same moment** (payment page, 25 Sep 2026). A launch check read the reduced-motion page at 1.2s and the normal one at 6s and called 11 states "reduced motion shows less". Timed side by side, content arrived at the same 1.3s either way: the data, not the motion.
- **"Press the main key" must press the open sheet's key** (payment page, 25 Sep 2026). With a sheet open, the first `.pay-3dkey` in the document can be the covered key on the screen underneath; the click never lands and the check reports a silent key. Look inside `dialog[open]` first.
