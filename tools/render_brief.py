#!/usr/bin/env python3
"""Minimal markdown -> iPad-friendly HTML (large type, MathJax). No dependencies.
Set EDUCATION_OUT to also copy the html into a synced folder (iCloud Drive, Obsidian vault, etc.)."""
import sys, re, html, os, shutil, pathlib
src = pathlib.Path(sys.argv[1]); full_md = src.read_text()
# The default artifact is prompt-only. Answers require opening a separate file.
md = full_md.split("## Retrieval answers",1)[0]
md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s
out, i, lines = [], 0, md.splitlines()
while i < len(lines):
    l = lines[i]
    if l.startswith("```"):
        j = i+1
        while j < len(lines) and not lines[j].startswith("```"): j += 1
        out.append("<pre><code>" + html.escape("\n".join(lines[i+1:j])) + "</code></pre>"); i = j+1; continue
    if l.startswith("|") and i+1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i+1]):
        hdr = [c.strip() for c in l.strip("|").split("|")]; rows=[]; j=i+2
        while j < len(lines) and lines[j].startswith("|"):
            rows.append([c.strip() for c in lines[j].strip("|").split("|")]); j+=1
        out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in hdr) + "</tr>" +
                   "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"); i=j; continue
    m = re.match(r"^(#{1,4}) (.*)", l)
    if m: out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>"); i+=1; continue
    if re.match(r"^\s*[-*] ", l) or re.match(r"^\s*\d+\. ", l):
        tag = "ol" if re.match(r"^\s*\d+\. ", l) else "ul"; items=[]; j=i
        while j < len(lines) and (re.match(r"^\s*[-*] ", lines[j]) or re.match(r"^\s*\d+\. ", lines[j])):
            items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[j])); j+=1
        out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>"); i=j; continue
    if l.strip().startswith("<div"): out.append(l); i+=1; continue
    if l.strip() == "": i+=1; continue
    para=[]; j=i
    while j < len(lines) and lines[j].strip() and not lines[j].startswith(("#","|","```","-","*","<")) and not re.match(r"^\d+\. ", lines[j]):
        para.append(lines[j]); j+=1
    if not para: para=[l]; j=i+1
    out.append("<p>" + inline(" ".join(para)) + "</p>"); i=j
page = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(src.stem)}</title>
<script>MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)'],['$','$']],displayMath:[['\\\\[','\\\\]'],['$$','$$']]}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
<style>
:root{{--fg:#1b1b1b;--bg:#fbfaf7;--mute:#666;--rule:#ddd;--code:#efede8}}
@media (prefers-color-scheme:dark){{:root{{--fg:#e8e6e0;--bg:#141414;--mute:#999;--rule:#333;--code:#222}}}}
body{{font:21px/1.55 Georgia,'Times New Roman',serif;color:var(--fg);background:var(--bg);max-width:42em;margin:0 auto;padding:2em 1.2em 6em}}
h1{{font-size:1.5em}}h2{{font-size:1.2em;margin-top:2em;border-bottom:1px solid var(--rule);padding-bottom:.2em}}h3{{font-size:1.05em;color:var(--mute)}}
code,pre{{font:0.85em ui-monospace,Menlo,monospace;background:var(--code);border-radius:4px;padding:.1em .3em}}pre{{padding:.8em;overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:.85em;overflow-x:auto;display:block}}td,th{{border:1px solid var(--rule);padding:.4em .6em;text-align:left;vertical-align:top}}
a{{color:inherit}}
</style></head><body>{''.join(out)}</body></html>"""
dst = src.with_suffix(".prompt.html"); dst.write_text(page); print(dst)
answers = src.with_suffix(".answers.html")
if "## Retrieval answers" in full_md:
    answer_text = "## Retrieval answers" + full_md.split("## Retrieval answers",1)[1]
    escaped = html.escape(answer_text)
    answers.write_text(page.replace("</body>",f"<hr><pre>{escaped}</pre></body>")); print(answers)
if os.environ.get("EDUCATION_OUT"):
    outdir=pathlib.Path(os.environ["EDUCATION_OUT"]); outdir.mkdir(parents=True,exist_ok=True)
    shutil.copy(dst,outdir/dst.name); shutil.copy(answers,outdir/answers.name); print("copied to", outdir)
