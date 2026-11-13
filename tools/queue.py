#!/usr/bin/env python3
"""Question queue.
  python tools/queue.py add <task-id> "question"      (agent)
  python tools/queue.py list                            (human)
  python tools/queue.py answer <qid> "answer"           (human)
"""
import sys, re
from common import *
text = QUEUE.read_text()
cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
if cmd == "add":
    tid, q = sys.argv[2], sys.argv[3]
    ids=[int(x) for x in re.findall(r"^### Q(\d+)", text, re.M)]; n=max(ids or [0])+1
    priority = "consequential" if "--priority" in sys.argv and sys.argv[-1] == "consequential" else "batch"
    text += f"\n### Q{n:03d} [{tid}] [OPEN] [{priority}] {today()}\n**Q:** {q}\n**A:** \n"
    QUEUE.write_text(text); print(f"Q{n:03d} added; task {tid} is blocked until answered")
elif cmd == "answer":
    qid, a = sys.argv[2], sys.argv[3]
    new, k = re.subn(rf"(### {qid} \[[^\]]+\]) \[OPEN\](.*?\*\*A:\*\*) ?", rf"\1 [ANSWERED {today()}]\2 {a}", text, flags=re.S)
    if not k: sys.exit("no such open question")
    QUEUE.write_text(new); print("answered")
else:
    opens = re.findall(r"^### (Q\d+) \[([^\]]+)\] \[OPEN\] \[([^\]]+)\] (\S+)\n\*\*Q:\*\* (.+)", text, re.M)
    if not opens: print("queue empty")
    for qid, tid, priority, d, q in sorted(opens,key=lambda x:x[2]!="consequential"): print(f"{qid}  {priority}  {tid}  {d}\n   {q}\n")
