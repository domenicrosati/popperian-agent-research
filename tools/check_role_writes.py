#!/usr/bin/env python3
"""Fail if a role changed paths outside its allowlist. Run after every agent turn."""
import sys, subprocess
role=sys.argv[1] if len(sys.argv)>1 else "research"
allowed={
 "research":("AgentWork/","Reports/","lean/Evidence/","SHARED/"),
 "critic":("Reports/reviews/","Reports/reproductions/"),
 "education":("Education/briefs/","Education/concepts/","Education/backlog.md"),
}
if role not in allowed: raise SystemExit("role must be research, critic, or education")
r=subprocess.run(["git","status","--porcelain","-z"],capture_output=True,check=True)
paths=[]
for item in r.stdout.decode(errors="replace").split("\0"):
    if not item: continue
    path=item[3:]
    if " -> " in path: path=path.split(" -> ",1)[1]
    paths.append(path)
bad=[p for p in paths if not p.startswith(allowed[role])]
if bad:
    print("role boundary violation:"); print("\n".join(f"- {p}" for p in bad)); raise SystemExit(1)
print(f"{role} writes stay within role boundary")
