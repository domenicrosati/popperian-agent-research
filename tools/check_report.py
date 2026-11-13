#!/usr/bin/env python3
"""Strict structural and provenance validation. Passing means candidate, not verified."""
import sys, re, pathlib
from common import *
REQUIRED = ["Claims","Evidence","Critical tests","Corroborations","Criticism","Conceptual load",
 "Deviations from the task and spec","Not done","Dead ends encountered","Literature added",
 "Future suggestions","Suggested spec edits","Questions raised"]
STATES = {"candidate","reproduced","criticized","verified","refuted"}
def section(text, name):
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", text, re.M|re.S)
    return m.group(1).strip() if m else ""
def check(report):
    errs=[]; text=report.read_text(); fm=frontmatter(text)
    for k in ("task","date","spec_version","status","confidence"):
        if not fm.get(k): errs.append(f"frontmatter missing {k}")
    if fm.get("status") not in STATES: errs.append("invalid status")
    try:
        if not 0 <= float(fm.get("confidence","x")) <= 1: errs.append("confidence outside 0..1")
    except ValueError: errs.append("confidence must be numeric")
    if fm.get("spec_version") != spec_version(): errs.append("spec drift: rebase or explicitly supersede task")
    for h in REQUIRED:
        body=section(text,h)
        if not body: errs.append(f"missing or empty section: {h}")
        if "{{" in body: errs.append(f"placeholder in section: {h}")
    manifest=report.with_suffix(".manifest.json")
    if not manifest.exists(): return errs+[f"missing manifest {manifest.name}"]
    try: m=json_load(manifest)
    except Exception as e: return errs+[f"invalid manifest: {e}"]
    for k in ("schema_version","task","report","spec_version","spec_sha","state","producer","claims","evidence","reproduction","critique"):
        if k not in m: errs.append(f"manifest missing {k}")
    if m.get("task") != fm.get("task"): errs.append("task mismatch report/manifest")
    if m.get("state") != fm.get("status"): errs.append("state mismatch report/manifest")
    if m.get("spec_sha") != spec_sha(): errs.append("manifest spec_sha is stale")
    known=claim_ids()
    for c in m.get("claims",[]):
        if c.get("id") not in known: errs.append(f"unknown claim id {c.get('id')}")
        if not c.get("statement") or not c.get("evidence"): errs.append(f"claim {c.get('id')} lacks statement/evidence")
        try:
            if not 0 <= float(c.get("confidence")) <= 1: raise ValueError
        except (TypeError,ValueError): errs.append(f"claim {c.get('id')} confidence invalid")
    bypath={e.get("path"):e for e in m.get("evidence",[])}
    for e in bypath.values():
        p=ROOT/e.get("path","")
        if not p.is_file(): errs.append(f"missing evidence {e.get('path')}"); continue
        if not e.get("sha256") or sha256(p)!=e.get("sha256"): errs.append(f"unfrozen or changed evidence {e.get('path')}")
        if not e.get("kind") or not e.get("command") or not e.get("environment"): errs.append(f"incomplete provenance {e.get('path')}")
        if e.get("kind")=="experiment" and e.get("seed") in (None,""): errs.append(f"experiment lacks seed {e.get('path')}")
    for c in m.get("claims",[]):
        for p in c.get("evidence",[]):
            if p not in bypath: errs.append(f"claim references undeclared evidence {p}")
    prod=m.get("producer",{})
    if not all(prod.get(k) for k in ("agent_id","model","prompt_version","source_revision")): errs.append("producer provenance incomplete")
    if m.get("state") in {"reproduced","criticized","verified"} and not m.get("reproduction",{}).get("passed"): errs.append("state requires passed reproduction")
    if m.get("state") in {"criticized","verified"}:
        cr=m.get("critique",{}); rec=cr.get("record","")
        if cr.get("reviewer_id")==prod.get("agent_id"): errs.append("critic is not independent")
        if cr.get("verdict") not in {"ACCEPT","ACCEPT-WITH-GAPS"}: errs.append("state requires accepting critic verdict")
        if not rec or not (ROOT/rec).is_file(): errs.append("missing critic record")
    return errs
files=[pathlib.Path(a) for a in sys.argv[1:]] or sorted(REPORTS.glob("*.md"))
files=[p for p in files if p.name!="README.md"]; bad=0
for p in files:
    e=check(p); print(("FAIL " if e else "ok   ")+str(p.relative_to(ROOT)))
    for x in e: print("  -",x)
    bad += bool(e)
sys.exit(1 if bad else 0)
