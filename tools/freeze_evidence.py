#!/usr/bin/env python3
import sys, json
from common import *
p=pathlib.Path(sys.argv[1]); m=json_load(p)
for e in m.get("evidence",[]):
    f=ROOT/e["path"]
    if not f.is_file(): raise SystemExit(f"missing evidence: {e['path']}")
    e["sha256"]=sha256(f)
atomic_write(p, json.dumps(m,indent=2)+"\n"); print(p)
