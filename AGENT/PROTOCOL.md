# Task protocol

## 0. Receive
Task file: `AgentWork/tasks/<id>/task.md`. It records the spec version it was dispatched under. If `SPEC.md`'s version is now higher, stop and ask whether the task still stands.

## 1. Plan before run  (mandatory, cheap for the human to check)
Write `AgentWork/tasks/<id>/plan.md` containing:
- The goal restated in your own words (if this is hard, the task is ambiguous: ask).
- The claim(s) from SPEC this serves and their falsifiers.
- The approach, as numbered steps, each with an expected output.
- The first milestone: something checkable within ~1 hour of work. If the first milestone fails, stop.
- Stop conditions (below) specialised to this task.
- Budget: tokens / compute / wall-clock, from the task file.
Then set `status: planned` in `task.md`. Stop only when `review_class: consequential`; routine and bounded tasks proceed automatically.

## 2. Run
- Log decisions to `AgentWork/tasks/<id>/log.md` as you go (what you tried, what happened, why you changed course). Terse. This is for audit, not for the human to read routinely.
- Keep every artifact that supports a claim under `Reports/evidence/<id>/` with a stable filename; keep everything else in `AgentWork/tasks/<id>/work/`.
- Formal work goes in `lean/Evidence/<Id>.lean`. `lake build` must pass. No `sorry`, no `admit`, no unsafe axioms beyond the Mathlib defaults.
- Experiments: config as a file, seeds fixed and recorded, outputs logged, a plot produced. A result without these does not go in a report.

## 3. Autonomy and escalation
Continue autonomously while the work is reversible, within budget, and does not change the scientific target. Use the task's fallback ladder after a failed milestone. Do not ask the human to choose between technically equivalent implementation details.

Escalate via `tools/queue.py add --priority consequential` and set `status: blocked` only when:
- A new assumption materially changes the claim rather than merely enabling a diagnostic.
- Evidence challenges the hard core. Preserve and replicate it in a `foundational-challenge` task; never suppress it.
- All pre-approved fallback branches failed.
- You have found what looks like a counterexample to a claim marked `established`.
- Budget exhausted.
- You are about to narrow a claim to make a test pass (ad hoc rescue).
- An action is irreversible, externally consequential, or exceeds the task's cost threshold.
Non-consequential uncertainties go into the report and do not interrupt the human.

## 4. Self-criticism, then critic
Before writing the report, run `AGENT/CRITIC_RUBRIC.md` against your own result. A different agent/context must independently review every consequential claim from the frozen evidence bundle using `AGENT/CRITIC_TEMPLATE.md`. The producer cannot mark its own claim verified.

## 5. Report
Fill `AGENT/REPORT_TEMPLATE.md` and `AGENT/MANIFEST_TEMPLATE.json` into `Reports/<date>-<id>.md` and its sibling `.manifest.json`. Freeze cited evidence with hashes using `python tools/freeze_evidence.py <manifest>`, then run `python tools/check_report.py <report>`. A passing structural check means `candidate`, not verified. Independent reproduction and criticism advance it through `reproduced`, `criticized`, and finally `verified` with `python tools/gate.py <manifest>`.

## 6. Shared files
Append to `SHARED/LITERATURE.md` (mark `[agent]`) and `SHARED/DEAD_ENDS.md` as warranted. Append only; never rewrite existing lines.
