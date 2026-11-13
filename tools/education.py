#!/usr/bin/env python3
"""Assemble the education agent's packet and print the dispatch command.  make morning"""
import re, subprocess
from common import *
ED = ROOT / "Education"; CTX = ED / ".context"; CTX.mkdir(exist_ok=True)
state = CTX / "last_brief"
pending = CTX / "pending_brief"
last = state.read_text().strip() if state.exists() else "1970-01-01"

spec = SPEC.read_text()
claims = re.findall(r"### (C\d+)\.\s*(.*?)\n(.*?)(?=\n### |\n## |\Z)", spec, re.S)
dep = {}
for cid, title, body in claims:
    for d in re.findall(r"Depends on:.*", body):
        for x in re.findall(r"C\d+", d): dep[x] = dep.get(x, 0) + 1
lines = ["# Packet", f"since: {last}", f"spec version: {spec_version()}", "", "## Claims (status / understanding links / tier / fan-out)"]
eligible = 0
for cid, title, body in claims:
    g = lambda k: (re.search(rf"{k}:\s*([^\n<]+)", body) or [None, "?"])[1].strip()
    lines.append(f"- {cid} {title.strip()} | status={g('Status')} | understanding={g('Understanding concept links')} | tier={g('Tier')} | fan_out={dep.get(cid,0)}")
hc = re.search(r"Hard core.*?\n(.*?)\nProtective belt", spec, re.S)
lines += ["", "## Hard core", hc.group(1) if hc else "(none)", "", "## Validated reports since last brief"]
for p in sorted(REPORTS.glob("*.md")):
    if p.name == "README.md" or p.name[:10] < last: continue
    manifest = p.with_suffix(".manifest.json")
    if not manifest.exists() or json_load(manifest).get("state") != "verified":
        lines.append(f"- {p.name}: not independently verified, do not teach from it"); continue
    r = subprocess.run(["python3", str(ROOT/"tools/check_report.py"), str(p)], capture_output=True, text=True)
    if r.returncode != 0: lines.append(f"- {p.name}: FAILED validation, do not teach from it"); continue
    eligible += 1
    t = p.read_text(); fm = frontmatter(t)
    cl = re.search(r"## Claims\n(.*?)\n## ", t, re.S); load = re.search(r"## Conceptual load\n(.*?)\n## ", t, re.S)
    lines += [f"### {p.name}  status={fm.get('status')} confidence={fm.get('confidence')}",
              "Claims:", cl.group(1).strip() if cl else "", "Conceptual load:", load.group(1).strip() if load else ""]
lines += ["", "## Recent briefs (for spacing retrieval)"]
for b in sorted((ED/"briefs").glob("*.md"))[-30:]:
    lines.append(f"- {b.name}: concept={frontmatter(b.read_text()).get('concept','?')}")
lines += ["", "## Demonstrated understanding ledger", (ED/"UNDERSTANDING.md").read_text()]
(CTX / "packet.md").write_text("\n".join(lines) + "\n")
print(f"packet written: Education/.context/packet.md\n"
      f"dispatch: 'Read Education/AGENT.md and produce today's brief ({today()}).'\n"
      f"after it runs: python3 tools/check_brief.py Education/briefs/{today()}.md && python3 tools/render_brief.py Education/briefs/{today()}.md")
if eligible:
    atomic_write(pending, today()+"\n")
else:
    if pending.exists(): pending.unlink()
    print("no independently verified finding requires a brief; remain quiet")
