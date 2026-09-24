#!/usr/bin/env python3
"""run_probe.py: the Done Probe as one command (gates.md, Gate 2).

Runs ui-probe.js against a live page at several widths in a REAL browser
window (Playwright persistent context), so focus, blur, :focus-visible and
sticky all behave the way they do for a person. The Claude Browser preview
pane cannot do that: document.hasFocus() is false there and "desktop" is
800px.

    python3 ~/.claude/skills/module-redesign-pipeline/scripts/run_probe.py \
        --url http://localhost:3000/property/complaints/setup \
        --profile "$SCRATCHPAD/pw-profile" \
        --widths 375,1440 \
        [--first-row '[role="row"]'] [--wait 3] [--json] [--headed]

--profile is the persistent profile that already holds a login (see the
feedback_playwright-persistent-profile memory). The page is warmed on "/"
first and then soft-navigated with Next's client router, so Redux stays warm
and plan colours render correctly; a hard goto resets the store.

Exit code 1 if any width has findings, so it can gate a commit.
"""
import argparse
import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = open(os.path.join(HERE, "ui-probe.js"), encoding="utf-8").read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--profile", default=None)
    ap.add_argument("--widths", default="375,1440")
    ap.add_argument("--first-row", default=None)
    ap.add_argument("--wait", type=float, default=3.0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--headed", action="store_true")
    # Playwright's bundled Chromium cannot decrypt cookies written by Google
    # Chrome (they are encrypted with a Keychain key scoped to that browser), so
    # a profile authed in real Chrome probes the LOGIN page instead of the screen.
    # `--channel chrome` launches the installed Chrome against the same profile.
    ap.add_argument("--channel", default=None)
    a = ap.parse_args()

    widths = [int(w) for w in a.widths.split(",")]
    from urllib.parse import urlsplit

    urls = [u.strip() for u in a.url.split(",") if u.strip()]
    origin = "{0.scheme}://{0.netloc}".format(urlsplit(urls[0]))

    out = {}
    failed = False
    with sync_playwright() as p:
        if a.profile:
            ctx = p.chromium.launch_persistent_context(a.profile, headless=not a.headed, viewport={"width": widths[0], "height": 900}, **({"channel": a.channel} if a.channel else {}))
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
        else:
            browser = p.chromium.launch(headless=not a.headed)
            ctx = browser.new_context(viewport={"width": widths[0], "height": 900})
            page = ctx.new_page()

        # Warm the app once so client-side stores (plan colours, property) load.
        page.goto(origin + "/", wait_until="load")
        page.wait_for_timeout(int(a.wait * 1000))
        # Session cookies do not survive a persistent-context restart, so a headed run
        # waits (up to 10 min) for a person to log in before probing.
        if a.headed:
            for _ in range(300):
                if page.locator("text=Login with").count() == 0:
                    break
                page.wait_for_timeout(2000)
            page.wait_for_timeout(int(a.wait * 1000))

        for url in urls:
          path = url[len(origin):] or "/"
          for w in widths:
              h = 812 if w < 768 else 900
              page.set_viewport_size({"width": w, "height": h})
              # Soft navigation keeps Redux warm; fall back to a hard goto.
              navigated = page.evaluate(
                  "(u) => { try { if (window.next && window.next.router) { window.next.router.push(u); return true } } catch (e) {} return false }",
                  path,
              )
              if not navigated or page.url.rstrip("/") != url.rstrip("/"):
                  page.goto(url, wait_until="load")
              page.wait_for_timeout(int(a.wait * 1000))
              opts = {"firstRow": a.first_row} if a.first_row else {}
              report = page.evaluate("({src, opts}) => { (0, eval)(src); return uiProbe(opts) }", {"src": PROBE, "opts": opts})
              out[w] = report
              failed = failed or not report["pass"]
              if not a.json:
                  print(f"\n== {url} {report['summary']} ==")
                  print(f"first content row y: {report['firstRowY']}")
                  for row in report["controlRows"]:
                      mark = "  <-- " if (row["centreSpread"] > 2 or row["heightSpread"] > 2) else "      "
                      print(mark + " | ".join(f"{i['t'] or '(no label)'} {i['h']}px@{i['cy']}" for i in row["items"]))
                  for s in report["sticky"]:
                      extra = f", h {s['h']}/{s['rowH']}" if "rowH" in s else ""
                      print(f"sticky {s['t']}: x {s['before']} -> {s['after']}{extra}")
                  for pv in report["popovers"]:
                      print(f"popover {pv['t']}: portaled={pv['portaled']} gutter={pv['gutter']}")
                  if report["findings"]:
                      print("findings:")
                      for f in report["findings"]:
                          print(f"  [{f['kind']}] {f['detail']}")
        ctx.close()

    if a.json:
        print(json.dumps(out, indent=2))
    # success-only token, so a gate's EXPECT cannot match a failing run
    print("DONE-PROBE: FAIL" if failed else "DONE-PROBE: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
