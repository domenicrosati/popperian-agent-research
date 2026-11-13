#!/usr/bin/env python3
"""Commit the education cursor only after both validation and rendering succeed."""
import sys, subprocess
from common import *
ED=ROOT/"Education"; CTX=ED/".context"; pending=CTX/"pending_brief"
if not pending.exists(): raise SystemExit("no pending brief")
d=pending.read_text().strip(); md=ED/"briefs"/f"{d}.md"
subprocess.run(["python3",str(ROOT/"tools/check_brief.py"),str(md)],check=True)
subprocess.run(["python3",str(ROOT/"tools/render_brief.py"),str(md)],check=True)
notes=ED/"anki"/"notes.json"
if notes.exists():
    subprocess.run(["python3",str(ROOT/"tools/export_anki.py"),str(notes),str(ED/"anki"/"research.tsv")],check=True)
atomic_write(CTX/"last_brief",d+"\n"); pending.unlink(); print(f"committed brief {d}")
