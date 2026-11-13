#!/usr/bin/env python3
"""Validate source-grounded mathematical notes and export Anki TSV; no external writes."""
import argparse
import csv
import html
import io
import json
from pathlib import Path

KINDS = {"definition", "theorem", "lemma", "technique", "identity", "decomposition", "rate", "conceptual"}

def export(notes):
    if not isinstance(notes, list):
        raise ValueError("notes must be an array")
    seen, prompts = set(), set()
    out = io.StringIO()
    out.write("#separator:Tab\n#html:true\n#notetype:Research Math\n#tags column:6\n")
    writer = csv.writer(out, delimiter="\t", lineterminator="\n")
    for n in notes:
        for k in ("id", "concept", "front", "back", "source_title", "source_url", "source_location", "discovery_link"):
            if not isinstance(n.get(k), str) or not n[k].strip():
                raise ValueError(f"missing {k}")
        prompt = " ".join(n["front"].casefold().split())
        if n["id"] in seen or prompt in prompts:
            raise ValueError("duplicate ID or prompt")
        if n.get("kind") not in KINDS or n.get("source_verified") is not True:
            raise ValueError("invalid kind or unchecked source")
        if not n["source_url"].startswith(("https://", "http://")):
            raise ValueError("source URL required")
        tags = n.get("tags", [])
        if not isinstance(tags, list) or any(not isinstance(t, str) or not t or any(c.isspace() for c in t) for t in tags):
            raise ValueError("tags must be whitespace-free strings")
        seen.add(n["id"]); prompts.add(prompt)
        def esc(s):
            return html.escape(s, quote=True).replace("\n", "<br>")
        source = '<a href="' + esc(n["source_url"]) + '">' + esc(n["source_title"]) + "</a> — " + esc(n["source_location"])
        writer.writerow([n["id"], esc(n["front"]), esc(n["back"]), source, esc(n["discovery_link"]), " ".join(tags)])
    return out.getvalue()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notes", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = export(json.loads(args.notes.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(f"exported {args.output}")

if __name__ == "__main__":
    main()
