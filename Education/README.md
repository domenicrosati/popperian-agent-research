# Education

Owned by the understanding loop. An education agent runs on a schedule (`make morning`, or the cron/launchd files in `tools/schedule/`), reads what the discovery loop produced, and writes one short brief per day for the human to read away from the computer.

- `CRITERIA.md`      human-edited rules for what a brief may contain. The only steering input.
- `AGENT.md`         the education agent's charter.
- `BRIEF_TEMPLATE.md` fixed shape of a brief; enforced by `tools/check_brief.py`.
- `backlog.md`       B: validated-but-not-assimilated findings with proposed tiers. Agent proposes, human confirms by editing SPEC.
- `concepts/`        one explanatory spine per concept the human is studying. Agent drafts, human edits after reconstructing.
- `briefs/`          `YYYY-MM-DD.md` + `.html` (iPad-readable, large type, MathJax).
- `.context/`        the packet `tools/education.py` assembles for the agent. Disposable.

Nothing in here is evidence and nothing in here may create tasks, decisions, or spec changes. It exists to build the human's understanding and for no other purpose.
