#!/usr/bin/env python3
"""Scaffold a task: python tools/new_task.py "title" [--skip-plan-review] [--no-critic]"""
import sys, re
from common import *
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args: sys.exit(__doc__)
title = args[0]
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
n = max([int(m.group(1)) for p in TASKS.glob("T*/") if (m:=re.match(r"T(\d+)",p.name))] or [0]) + 1
tid = f"T{n:03d}"
d = TASKS / f"{tid}-{slug}"; (d / "work").mkdir(parents=True)
(REPORTS / "evidence" / tid).mkdir(parents=True, exist_ok=True)
tmpl = (ROOT / "AGENT" / "TASK_TEMPLATE.md").read_text()
t = (tmpl.replace("{{ID}}", tid).replace("{{TITLE}}", title).replace("{{DATE}}", today())
         .replace("{{SPEC_VERSION}}", spec_version()).replace("{{SPEC_SHA}}", spec_sha())
         .replace("{{LEANID}}", tid))
if "--consequential" in sys.argv: t = t.replace("review_class: routine", "review_class: consequential")
if "--no-critic" in sys.argv: t = t.replace("critic: required", "critic: skip")
(d / "task.md").write_text(t); (d / "log.md").write_text(f"# {tid} log\n")
print(f"{d}/task.md   <- write the Goal section, then dispatch an agent with:\n"
      f"  'Read CLAUDE.md, then execute {d.relative_to(ROOT)}/task.md'")
