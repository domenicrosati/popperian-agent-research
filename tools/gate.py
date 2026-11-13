#!/usr/bin/env python3
import sys, json, datetime, re
from common import *
p=pathlib.Path(sys.argv[1]); m=json_load(p); prod=m.get("producer",{}).get("agent_id")
rep=m.get("reproduction",{}); crit=m.get("critique",{})
if not rep.get("passed") or not rep.get("reviewer_id") or rep.get("reviewer_id")==prod: raise SystemExit("independent reproduction required")
if not rep.get("record") or not (ROOT/rep["record"]).is_file(): raise SystemExit("reproduction record missing")
if crit.get("reviewer_id")==prod or crit.get("verdict") not in {"ACCEPT","ACCEPT-WITH-GAPS"}: raise SystemExit("independent accepting critique required")
if not crit.get("record") or not (ROOT/crit["record"]).is_file(): raise SystemExit("critique record missing")
m["state"]="verified"; m["verified_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
atomic_write(p,json.dumps(m,indent=2)+"\n")
report=ROOT/m["report"]; t=report.read_text(); t=re.sub(r"(?m)^status:\s*\S+", "status: verified", t, count=1); atomic_write(report,t)
print(f"verified {p}")
