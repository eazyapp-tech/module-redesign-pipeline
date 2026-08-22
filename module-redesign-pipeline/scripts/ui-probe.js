// ui-probe.js — the Done Probe (gates.md, Gate 2).
//
// Runs INSIDE a page and returns a JSON report. Use it from the Claude Browser
// `javascript_tool`, a Playwright `page.evaluate`, or DevTools. It prints
// numbers; you judge them. Run at 375 and at an explicit 1440.
//
//   javascript_tool:  <paste this file>  then  `uiProbe()`
//   playwright:       await page.evaluate(fs.readFileSync('ui-probe.js','utf8')); await page.evaluate(() => uiProbe())
//
// Options (all optional):
//   uiProbe({ firstRow: '[role="row"]', toolbar: '[data-toolbar]', pan: 300 })
//
// Pass conditions, per gates.md: controls in a row share one centre (±2px),
// sticky x unchanged after the pan, every popover portaled with ≥8px gutter,
// no icon at 0px, flex peers within 2px, no horizontal overflow, first-row y
// stated and judged, and zero cards open after a programmatic focus.

function uiProbe(opts) {
  opts = opts || {}
  var vw = window.innerWidth, vh = window.innerHeight
  var r = function (el) { return el.getBoundingClientRect() }
  var round = Math.round
  var visible = function (el) {
    var q = r(el), cs = getComputedStyle(el)
    return q.width > 0 && q.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0'
  }
  var label = function (el) { return (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24) }
  var report = { viewport: { w: vw, h: vh }, findings: [] }
  var flag = function (kind, detail) { report.findings.push({ kind: kind, detail: detail }) }

  // 1. First content row's y. Heuristic selectors; pass your own for accuracy.
  var rowSel = opts.firstRow || '[role="row"]:not([aria-rowindex="1"]), tbody tr, [data-row], li[data-index]'
  var rows = [].slice.call(document.querySelectorAll(rowSel)).filter(visible)
  // skip header-ish rows: the first one whose top is below any columnheader
  var hdr = document.querySelector('[role="columnheader"], thead')
  var hdrBottom = hdr ? r(hdr).bottom : 0
  var first = rows.find(function (el) { return r(el).top >= hdrBottom })
  report.firstRowY = first ? round(r(first).top) : null
  if (report.firstRowY !== null && vw < 768 && report.firstRowY > vh * 0.4) {
    flag('chrome', 'first content row at y=' + report.firstRowY + ' of ' + vh + ' on a phone: more than 40% of the screen is chrome')
  }

  // 2. Toolbar rows: every group of ≥2 interactive siblings laid out horizontally.
  var interactive = 'button, [role="button"], [role="group"], [role="tab"], a[href], input, select'
  var parents = new Set()
  document.querySelectorAll(interactive).forEach(function (el) { if (visible(el) && el.parentElement) parents.add(el.parentElement) })
  report.controlRows = []
  parents.forEach(function (p) {
    var kids = [].slice.call(p.children).filter(function (k) { return visible(k) && (k.matches(interactive) || k.querySelector(interactive)) })
    if (kids.length < 2) return
    var cs = getComputedStyle(p)
    var horizontal = (cs.display.indexOf('flex') >= 0 && cs.flexDirection.indexOf('row') === 0) || cs.display.indexOf('grid') >= 0
    if (!horizontal) return
    var items = kids.map(function (k) { var q = r(k); return { t: label(k), h: round(q.height), cy: round(q.top + q.height / 2), w: round(q.width) } })
    var centres = items.map(function (i) { return i.cy }), heights = items.map(function (i) { return i.h })
    var spread = Math.max.apply(null, centres) - Math.min.apply(null, centres)
    var hSpread = Math.max.apply(null, heights) - Math.min.apply(null, heights)
    var row = { items: items, centreSpread: spread, heightSpread: hSpread }
    report.controlRows.push(row)
    if (spread > 2) flag('centre', 'controls in one row on different centre lines (spread ' + spread + 'px): ' + items.map(function (i) { return i.t + '@' + i.cy }).join(', '))
    if (hSpread > 2) flag('height', 'controls in one row at different heights (spread ' + hSpread + 'px): ' + items.map(function (i) { return i.t + ':' + i.h }).join(', '))
    // flex peers: only judge when the parent actually distributes width
    var peers = kids.filter(function (k) { return /^(1|1 1 0|1 1 0%|1 1 auto)/.test(getComputedStyle(k).flex) })
    if (peers.length >= 2) {
      var ws = peers.map(function (k) { return round(r(k).width) })
      var wSpread = Math.max.apply(null, ws) - Math.min.apply(null, ws)
      if (wSpread > 2) flag('flex', 'flex peers resolved to different widths (' + ws.join('/') + '): ' + peers.map(label).join(', ') + ' — is the container content-width? is one wrapped in a second flex level?')
    }
  })

  // 3. Sticky drift: pan every horizontal scroller and compare sticky x.
  report.sticky = []
  var scrollers = [].slice.call(document.querySelectorAll('*')).filter(function (el) {
    var cs = getComputedStyle(el)
    return /(auto|scroll)/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + 10 && visible(el)
  })
  scrollers.forEach(function (sc) {
    var stickies = [].slice.call(sc.querySelectorAll('*')).filter(function (el) {
      var cs = getComputedStyle(el); return cs.position === 'sticky' && cs.left !== 'auto' && visible(el)
    }).slice(0, 12)
    if (!stickies.length) return
    var before = stickies.map(function (el) { return round(r(el).left) })
    var prev = sc.scrollLeft
    sc.scrollLeft = Math.min(opts.pan || 300, sc.scrollWidth - sc.clientWidth)
    var after = stickies.map(function (el) { return round(r(el).left) })
    sc.scrollLeft = prev
    stickies.forEach(function (el, i) {
      var item = { t: label(el) || el.getAttribute('role') || el.tagName, before: before[i], after: after[i] }
      // A sticky cell is an opaque mask; if it is shorter than its row, the
      // scrolled cells show through above and below it.
      // Against the TALLEST SIBLING, not the row box: the row's own padding is
      // not a gap, a taller cell beside the sticky one is.
      var row = el.parentElement
      if (row) {
        var tallest = 0
        ;[].slice.call(row.children).forEach(function (k) { if (k !== el && visible(k)) tallest = Math.max(tallest, r(k).height) })
        item.h = round(r(el).height); item.rowH = round(tallest)
        if (tallest - r(el).height > 2) flag('sticky', 'sticky cell shorter than a sibling cell (' + item.h + ' vs ' + item.rowH + 'px): ' + item.t + ' — content scrolls through the gap above/below it')
      }
      report.sticky.push(item)
      if (before[i] !== after[i]) flag('sticky', 'sticky cell slid ' + (before[i] - after[i]) + 'px on a sideways pan: ' + item.t + ' (' + before[i] + ' → ' + after[i] + '). It pins at `left`, not at its resting x.')
    })
  })

  // 4. Popovers / cards: portaled, inside the viewport, gutter.
  var cardSel = '.chakra-popover__content, [role="tooltip"], [data-popper-placement], [role="dialog"]:not(.chakra-modal__content)'
  report.popovers = [].slice.call(document.querySelectorAll(cardSel)).filter(visible).map(function (el) {
    var q = r(el)
    var portaled = !!el.closest('.chakra-portal, [data-portal], body > div:last-child')
    var gutter = round(Math.min(q.left, vw - q.right, q.top, vh - q.bottom))
    var item = { t: label(el), portaled: portaled, left: round(q.left), right: round(q.right), gutter: gutter, inside: q.left >= 0 && q.right <= vw && q.top >= 0 && q.bottom <= vh }
    if (!portaled) flag('popover', 'card rendered inline, not portaled: ' + item.t + ' — it will be clipped by and scroll with its container')
    if (!item.inside) flag('popover', 'card outside the viewport: ' + item.t + ' (' + item.left + '..' + item.right + ' of ' + vw + ')')
    else if (gutter < 8) flag('popover', 'card flush to the screen edge (gutter ' + gutter + 'px): ' + item.t)
    return item
  })

  // 5. Icons at 0px inside controls.
  report.zeroIcons = []
  document.querySelectorAll(interactive).forEach(function (b) {
    if (!visible(b)) return
    b.querySelectorAll('svg').forEach(function (s) {
      var q = r(s); if (q.width < 1 || q.height < 1) { report.zeroIcons.push(label(b)); }
    })
  })
  if (report.zeroIcons.length) flag('icon', 'icons rendering at 0px inside: ' + report.zeroIcons.join(', ') + ' — a flex child with minW:0 shrank it away')

  // 6. Horizontal overflow.
  report.overflowX = document.documentElement.scrollWidth > document.documentElement.clientWidth
  if (report.overflowX) flag('overflow', 'page scrolls sideways (' + document.documentElement.scrollWidth + ' > ' + document.documentElement.clientWidth + ')')

  // 7. Tap targets on a phone.
  if (vw < 768) {
    var small = []
    document.querySelectorAll('button, a[href], input, [role="button"], [role="checkbox"]').forEach(function (el) {
      if (!visible(el)) return
      var q = r(el)
      // honour a pseudo-element hit extension: check the computed ::after inset
      var after = getComputedStyle(el, '::after')
      var extended = after && after.content !== 'none' && after.position === 'absolute'
      if (!extended && (q.width < 44 || q.height < 44)) small.push(label(el) + ' ' + round(q.width) + 'x' + round(q.height))
    })
    report.smallTapTargets = small.length
    if (small.length) flag('tap', small.length + ' tap targets under 44px on a phone, e.g. ' + small.slice(0, 5).join('; '))
  }

  // 8. Programmatic focus must not open a card.
  var focusables = [].slice.call(document.querySelectorAll('[tabindex="0"], [tabindex="-1"], button')).filter(visible).slice(0, 6)
  var openBefore = document.querySelectorAll(cardSel).length
  var active = document.activeElement
  focusables.forEach(function (el) { try { el.focus({ preventScroll: true }) } catch (e) {} })
  var openAfter = [].slice.call(document.querySelectorAll(cardSel)).filter(visible).length
  if (active && active.focus) { try { active.focus({ preventScroll: true }) } catch (e) {} } else if (document.activeElement) { document.activeElement.blur() }
  report.cardsAfterProgrammaticFocus = openAfter
  if (openAfter > openBefore) flag('focus', (openAfter - openBefore) + ' card(s) opened on a programmatic focus — open on :focus-visible only')

  report.pass = report.findings.length === 0
  report.summary = report.pass ? 'PASS at ' + vw + 'x' + vh : report.findings.length + ' finding(s) at ' + vw + 'x' + vh
  return report
}

if (typeof module !== 'undefined') module.exports = uiProbe
