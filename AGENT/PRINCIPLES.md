# Two loops, one backlog

The repo runs two coupled loops.

**Discovery loop (agents):** conjecture, derive, experiment, criticise, verify. Maximise the rate λ of important, *validated* findings. Lives in AgentWork/, Reports/, lean/.

**Understanding loop (human, served by the education agent):** reconstruct, compress, challenge, connect, derive something new independently. Maximise the rate μ at which validated findings become independent research capability. Lives in Education/, SPEC.md, HUMAN/.

The backlog B of findings that are validated but not yet assimilated grows at λ − μ. We do **not** try to drive B to zero. We triage it:

| Tier | Treatment | Who decides |
|---|---|---|
| `verify` | Trust the checker (Lean / tests / critic). Never reconstruct. Routine lemmas, bookkeeping bounds. | education agent proposes, human confirms |
| `tool` | Store as a reusable technique with a one-paragraph spine. Reconstruct only when needed. | same |
| `study` | Deserves blackboard time: it changes how the programme is understood or which questions are worth asking. Reconstruct fully, then derive one new implication unaided. | same |

Selection objective for the `study` tier: maximise expected gain in independent capability per hour of assimilation. Capability means the ability to choose research questions, build explanations, predict how a result moves under new assumptions, and transfer the technique. Fan-out in the SPEC claim graph and proximity to the hard core are the proxies the tools use.

Three tests that a finding has been assimilated (and not merely read): the human can (1) reconstruct the central argument with the document closed, (2) predict how the result changes under a specified change of assumption, (3) use the technique on a different problem. The education agent sets these; only the human can pass them.

Intuition relocates in this workflow: it often follows discovery rather than preceding it. That is acceptable only if reconstruction and later fresh transfer are demonstrated. Research truth stays in `SPEC.md`; capability evidence stays in `Education/UNDERSTANDING.md` and its append-only events.
