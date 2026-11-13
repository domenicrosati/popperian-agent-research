---
id: {{ID}}
title: {{TITLE}}
created: {{DATE}}
spec_version: {{SPEC_VERSION}}
spec_sha: {{SPEC_SHA}}
status: new            # new | planned | running | blocked | done | refuted
review_class: routine  # routine | consequential
critic: required       # required for every claim eligible for verification
task_kind: research    # research | replication | foundational-challenge | education
budget:
  wall_clock_hours: 6
  compute: "see SPEC §4"
  tokens: unlimited
  external_cost_usd: 0
---

# {{TITLE}}

## Goal (human-written)


## Serves claims
- C?

## Falsifier for this task
What outcome would mean the task failed in an informative way:


## Deliverables
- Report with evidence under Reports/evidence/{{ID}}/
- Lean certificate at lean/Evidence/{{LEANID}}.lean (if applicable)

## Pre-approved fallback ladder
1. Retry once after diagnosing the failure.
2. Use an independent method that preserves the claim and evidence standard.
3. Narrow only the method or diagnostic, never the claim; record the limitation.
4. Escalate only if all branches fail or the scientific target must change.

## Escalate only if
- irreversible or externally consequential action
- budget/cost threshold exceeded
- evidence challenges the hard core
- a new assumption materially changes the claim

## Notes from the human
