---
task: {{ID}}
date: {{DATE}}
spec_version: {{SPEC_VERSION}}
status: candidate       # candidate | reproduced | criticized | verified | refuted
confidence: 0.0         # overall, 0-1, that the Claims section is correct as stated
---

# Report {{ID}}: {{TITLE}}

## Claims
Precisely what this task establishes, as narrowly as the evidence supports. Each with its SPEC claim id and its evidence links.
- **C?-a** <statement>. Evidence: `Reports/evidence/{{ID}}/...`, `lean/Evidence/....lean` (theorem `name`). Confidence: 0.0

## Evidence
Table of every artifact cited above: path, what it is, how it was produced (command / config / seed).
| Path | What | How produced |
|---|---|---|

The sibling `.manifest.json` is authoritative for hashes, provenance, reproduction, and independent review.

## Critical tests
The severe tests that were designed to refute the claims, and their outcomes. Include tests that failed.
| Test | What it would have shown if failed | Outcome |
|---|---|---|

## Corroborations
Independent checks that agree (second method, second agent, numerical check of a proof, replication across seeds). Note explicitly what is *not* independent.

## Criticism
Self-criticism against AGENT/CRITIC_RUBRIC.md, then the critic agent's verdict verbatim if one ran. Every `[GAP]` listed here.

## Conceptual load
Does this change the picture or fill a slot? Which SPEC claims does it bear on, and what depends on those? Propose a tier (verify / tool / study) with one sentence of reason. If `study`: name the single distinction that determines the rest.

## Deviations from the task and spec
Anything done differently from plan.md or the task file, and why.

## Not done
What the task asked for that was not delivered.

## Dead ends encountered
Lines added to SHARED/DEAD_ENDS.md this task (copy them here).

## Literature added
Lines added to SHARED/LITERATURE.md this task.

## Future suggestions
Next tasks, in priority order, each with the claim it serves and a one-line reason.

## Suggested spec edits
Proposed changes to SPEC.md, as diffs or precise sentences. The human decides.

## Questions raised
Entries added to the queue this task (ids).
