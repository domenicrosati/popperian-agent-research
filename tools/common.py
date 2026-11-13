import hashlib, re, pathlib, datetime, json, os, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "SPEC.md"
TASKS = ROOT / "AgentWork" / "tasks"
REPORTS = ROOT / "Reports"
QUEUE = ROOT / "SHARED" / "QUESTIONS.md"
DIGEST_STATE = ROOT / "AgentWork" / ".last_digest"

def today(): return datetime.date.today().isoformat()
def spec_sha(): return hashlib.sha256(SPEC.read_bytes()).hexdigest()[:12]
def spec_version():
    m = re.search(r"Spec version:\s*([\w.\-]+)", SPEC.read_text())
    return m.group(1) if m else "unknown"
def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    if not m: return out
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1); out[k.strip()] = v.split("#")[0].strip()
    return out
def sha256(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()
def atomic_write(path, text):
    path = pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    try:
        with os.fdopen(fd, "w") as f: f.write(text); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def json_load(path): return json.loads(pathlib.Path(path).read_text())
def claim_ids(): return set(re.findall(r"^### (C\d+)\.", SPEC.read_text(), re.M))
def tasks():
    for d in sorted(TASKS.glob("*/")):
        f = d / "task.md"
        if f.exists(): yield d.name, frontmatter(f.read_text()), d
