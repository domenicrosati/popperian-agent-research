#!/usr/bin/env python3
"""One small human-attention packet: consequential decisions, verified changes, learning."""
import re
from common import *
print(f"# Attention packet {today()}\n")
q=QUEUE.read_text(); items=re.findall(r"^### (Q\d+) \[([^\]]+)\] \[OPEN\] \[consequential\] (\S+)\n\*\*Q:\*\* (.+)",q,re.M)
print("## Decisions requiring you")
if not items: print("- none")
for qid,tid,d,question in items: print(f"- {qid} ({tid}): {question}")
print("\n## Newly verified")
verified=[]
for p in sorted(REPORTS.glob("*.manifest.json")):
    m=json_load(p)
    if m.get("state")=="verified": verified.append((p,m))
if not verified: print("- none")
for p,m in verified[-5:]: print(f"- {m.get('task')}: {len(m.get('claims',[]))} claim(s), {p.name}")
print("\n## Failures needing attention")
blocked=[]
for tid,fm,d in tasks():
    if fm.get("status")=="blocked": blocked.append(tid)
print("- "+", ".join(blocked) if blocked else "- none; routine failures remain with agents")
print("\n## Understanding")
pending=ROOT/"Education"/".context"/"pending_brief"
print("- a brief is pending completion" if pending.exists() else "- no unfinished brief")
