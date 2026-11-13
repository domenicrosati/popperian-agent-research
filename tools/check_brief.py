#!/usr/bin/env python3
"""Enforce Education/CRITERIA.md mechanically where possible."""
import sys, re
from common import *
p = pathlib.Path(sys.argv[1]); t = p.read_text(); errs = []
fm = frontmatter(t)
for k in ("date","concept","backlog_study"):
    if k not in fm: errs.append(f"frontmatter missing {k}")
for h in ["Status","Today:","Self-test","Human lineage","Read deeper","Retrieval","Backlog","Reading","Retrieval answers"]:
    if not re.search(rf"^##+ {re.escape(h)}", t, re.M): errs.append(f"missing section {h}")
body = t.split("## Retrieval answers")[0]
words = len(re.sub(r"\|.*\|", "", body).split())
if words > 700: errs.append(f"{words} words of prose; limit 700")
if "AgentWork/" in t: errs.append("links into AgentWork/")
if re.search(r"(?i)^##+ (next steps|suggested tasks|todo|action items)", t, re.M): errs.append("contains a tasks section")
if len(re.findall(r"^## Today:", t, re.M)) != 1: errs.append("must have exactly one Today concept")
st = re.search(r"### Self-test\n(.*?)\n## ", t, re.S)
if not st or not all(k in st.group(1) for k in ("Reconstruct","Predict","Transfer")): errs.append("self-test must include Reconstruct/Predict/Transfer")
status = re.search(r"## Status\n(.*?)\n## ", t, re.S)
if status and len([l for l in status.group(1).strip().splitlines() if l.strip()]) > 5: errs.append("Status over 5 lines")
lineage = re.search(r"### Human lineage\n(.*?)(?=\n### |\n## )", t, re.S)
if lineage and not re.search(r"https?://|doi:|isbn", lineage.group(1), re.I): errs.append("Human lineage needs a stable citation or link")
deep = re.search(r"### Read deeper\n(.*?)(?=\n### |\n## )", t, re.S)
if deep and len(re.findall(r"https?://", deep.group(1))) > 3: errs.append("Read deeper has more than three links")
for path in set(re.findall(r"`((?:Reports|lean/Evidence|Education/concepts|SHARED)/[^`\s]+)`", t)):
    if not (ROOT / path).exists(): errs.append(f"dangling link {path}")
for w in ("great progress","well done","excellent work","impressive"):
    if w in t.lower(): errs.append(f"praise: '{w}'")
print(("FAIL " if errs else "ok   ") + str(p))
for e in errs: print("   -", e)
sys.exit(1 if errs else 0)
