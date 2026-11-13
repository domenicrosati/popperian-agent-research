#!/usr/bin/env python3
"""Append an immutable, human-supplied learning attempt: concept R/P/T result confidence note."""
import sys, json, datetime
from common import *
if len(sys.argv)<7: raise SystemExit("usage: concept reconstruct predict transfer confidence note")
event={"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"concept":sys.argv[1],
 "reconstruct":sys.argv[2],"predict":sys.argv[3],"transfer":sys.argv[4],"confidence":float(sys.argv[5]),"note":sys.argv[6]}
p=ROOT/"Education"/"understanding-events.jsonl"
with p.open("a") as f: f.write(json.dumps(event)+"\n")
print("recorded; mastery still requires later unaided transfer")
