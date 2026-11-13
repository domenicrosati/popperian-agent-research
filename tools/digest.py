#!/usr/bin/env python3
"""Evening digest: reports since last digest, blocked tasks, open questions, spec drift."""
import subprocess, datetime
from common import *
last = DIGEST_STATE.read_text().strip() if DIGEST_STATE.exists() else "1970-01-01"
print(f"# Digest {today()}  (since {last})\n")
print("## Reports")
new = [p for p in sorted(REPORTS.glob("*.md")) if p.name != "README.md" and p.name[:10] >= last]
for p in new:
    fm = frontmatter(p.read_text())
    r = subprocess.run(["python3", str(ROOT/"tools/check_report.py"), str(p)], capture_output=True, text=True)
    valid = "valid" if r.returncode == 0 else "INVALID"
    print(f"- {p.name}  status={fm.get('status')} confidence={fm.get('confidence')}  [{valid}]")
if not new: print("- none")
print("\n## Tasks")
for tid, fm, d in tasks():
    if fm.get("status") in ("blocked","running","planned"):
        flag = "  <- plan awaiting your review" if fm.get("status")=="planned" and fm.get("plan_review")=="required" else ""
        drift = "  <- SPEC changed since dispatch" if fm.get("spec_sha") != spec_sha() else ""
        print(f"- {tid}: {fm.get('status')}{flag}{drift}")
print("\n## Open questions")
subprocess.run(["python3", str(ROOT/"tools/queue.py"), "list"])
print("\n## Spec")
print(f"version {spec_version()} sha {spec_sha()}")
# Reading a digest is not acknowledgement. Advance only with tools/finalize_digest.py.
