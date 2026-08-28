#!/usr/bin/env python3
"""Gate 4 rot check: every `path` and `path:line` in the repo's design registry files must still exist.

usage: registry_rot.py <repo-root> [extra.md ...]
exit 1 if anything is dead. Paths are resolved relative to the repo root; a bare
`ComplaintSetup/tokens.ts` is also tried under components/**.
"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1]).resolve()
files = [root / "docs/design/COMPONENT-REGISTRY.md", root / "docs/design/PATTERNS.md"] + [pathlib.Path(a) for a in sys.argv[2:]]
ref = re.compile(r"`([A-Za-z0-9_./\[\]-]+\.(?:tsx?|dart|py|js|mjs|md|json))(?::(\d+)(?:-\d+)?)?`")
by_suffix = {}
for p in root.rglob("*"):
    if not p.is_file() or ".next" in p.parts or "node_modules" in p.parts or ".git" in p.parts:
        continue
    rel = p.relative_to(root).as_posix()
    parts = rel.split("/")
    for i in range(len(parts)):
        by_suffix.setdefault("/".join(parts[i:]), []).append(rel)

dead = []
for f in files:
    if not f.exists():
        continue
    for n, line in enumerate(f.read_text().splitlines(), 1):
        if "backend" in line or "~/.claude" in line or "Xxx" in line:
            continue  # another repo, the skill itself, or a placeholder
        for path, ln in ref.findall(line):
            hits = by_suffix.get(path.lstrip("./"), [])
            if not hits:
                dead.append((f.name, n, path, "missing"))
                continue
            if ln:
                target = root / hits[0]
                count = sum(1 for _ in open(target, errors="ignore"))
                if int(ln) > count:
                    dead.append((f.name, n, f"{path}:{ln}", f"only {count} lines"))
if dead:
    print(f"registry rot: {len(dead)} dead reference(s)")
    for f, n, p, why in dead:
        print(f"  {f}:{n}  {p}  ({why})")
    sys.exit(1)
print("registry rot: 0 dead references")
