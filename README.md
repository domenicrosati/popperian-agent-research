# Popperian Agent Research

A public, tool-agnostic template for autonomous research agents that optimizes for two things:

1. **Popperian science:** agents try to refute precise claims with severe tests instead of producing persuasive confirmations.
2. **Rapid human understanding:** verified discoveries are selectively converted into the human ability to reconstruct, predict, and transfer the important ideas.

The goal is not to maximize reports, tokens, experiments, proofs, or time spent interacting with AI. It is to increase the rate of reliable discovery while increasing—rather than eroding—the human researcher's independent judgment and uninterrupted time to think.

**The default human state should be away from the agents.** Agents work asynchronously, preserve context, recover from routine failures, and wait for a small number of deliberate review windows. The human's best hours belong to creativity, problem selection, mathematical thought, reading, writing, and understanding—not supervising an agent swarm or responding to a stream of plausible suggestions.

## Why this exists

Research agents can generate candidate results faster than a person can inspect or absorb them. Without an explicit architecture, this creates two debts:

- **verification debt:** claims accumulate faster than they can be challenged and reproduced;
- **understanding debt:** the project appears to advance while the human becomes less able to explain, modify, or extend it.

This repository treats those as separate control problems. A high-throughput discovery loop produces and attacks claims. A selective understanding loop turns only the most consequential verified findings into durable human capability. The human does not need to follow every agent action, read every failed attempt, or understand every routine lemma.

## Principle 1: Popperian science

Every task begins with a claim and a falsifier. Agents must seek the test most likely to expose the claim as false, preserve negative results, distinguish corroboration from confirmation, and label any post-hoc narrowing of the claim.

Evidence moves through an explicit state machine:

```text
candidate → reproduced → independently criticized → verified
```

A well-written report is not verified evidence. Verification requires frozen artifacts, provenance, an independent reproduction record, and a critic who is not the producing agent. Formal proof establishes the encoded theorem, not automatically the relevance or adequacy of its definitions and assumptions.

Even the research programme's “hard core” remains testable. Agents may not silently rewrite it, but contradictory evidence is preserved and routed into an independently replicated foundational challenge.

## Principle 2: rapid human understanding

The system does not ask the human to understand everything. Verified findings are triaged:

- **verify:** routine results that can remain delegated;
- **tool:** reusable techniques kept with a short conceptual spine;
- **study:** ideas that change research judgment and deserve deliberate assimilation.

Reading an explanation is not evidence of understanding. A concept is assimilated only when the human can:

1. reconstruct its central mechanism without the document open;
2. predict what changes when an important assumption changes;
3. transfer the mechanism to a genuinely different problem.

Briefs are therefore prompt-first: answers are rendered separately, and performance is tracked independently from the scientific claim ledger. The optimization target is capability gained per hour of human attention.

## Human absence is a design requirement

Human attention is not merely a scarce resource to allocate efficiently. Continuous AI interaction can fragment thought, replace problem incubation with reactive reviewing, and make the agent's framing dominate the researcher's own ideas. This system is therefore designed for long periods of human absence.

Agents independently handle reversible technical choices, bounded retries, diagnostics, checkpointing, recovery, and pre-approved fallback branches. They do not send progress chatter. They interrupt only for a changed scientific target, a replicated foundational contradiction, an irreversible or external action, or a budget breach. Routine ambiguity, failures, and suggestions are recorded and batched for the next review window.

The intended rhythm is:

```text
human sets direction → agents work independently → evidence is reproduced and criticized
→ one compact asynchronous packet → human thinks, learns, and decides → human leaves again
```

The repository should create fewer AI interactions over time as it learns the programme's constraints and the human's demonstrated understanding. A successful deployment gives the researcher more agent-free time, not a more elaborate agent dashboard.

The intended human interface is deliberately small and pull-based:

```sh
make attention   # consequential decisions, verified changes, and today's learning item
```

There are no routine progress notifications. If nothing consequential has changed, the correct packet is empty. The human chooses when to pull it.

Everything below explains how the repository implements those commitments.

## Repository architecture

## Bundled research skills

The reusable skill library lives in `.agents/skills/` within this repository, so instructions and tooling share one version history. It includes minimal-experiment, research-handoff, paper-companion, claim-reduction, and mathematical-anki. Agents read the matching SKILL.md when needed.

Morning understanding can include up to three source-checked Anki notes for relevant mathematical prerequisites: definitions and norms, theorem/lemma assumptions, proof techniques, identities, decompositions, complexity rates, and conceptual distinctions. Stable IDs support updates without duplicate notes. See `Education/ANKI.md` for the JSON schema, export command, and one-time Anki setup. Cards accompany useful weekday briefs and create no separate reminders.

The practices were informed by [autoresearch](https://github.com/karpathy/autoresearch), [The Agentic Researcher](https://github.com/ZIB-IOL/The-Agentic-Researcher), [long-running agent handoffs](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), and [Michael Nielsen's work on reading and memory](https://augmentingcognition.com/ltm.html). These are design influences, not evidence that this workflow is experimentally optimal.

Apply `AWAY_POLICY.md` for unattended operation: coordinators may work through weekends, while all human review waits for weekday mornings. Each goal needs explicit recovery permissions and budgets. Local supervision requires an online executor.

Research is seasonal. `RESEARCH_SEASONS.md` distinguishes theory formation, empirical discovery and validation, mathematical consolidation, and rigorous confirmation/paper reduction. The same quiet morning and afternoon runners change behavior with the active season; only the human creates new goals.

Understanding artifacts are grounded in human literature under `Education/LITERATURE_POLICY.md`: foundational pre-2023 papers and textbooks are preferred, post-2023 sources require trusted authorship or explicit justification, and every study brief provides a short path into the relevant human intellectual lineage.

The repo is split by **who may write where**. Agents operate independently inside a declared autonomy envelope, preserve durable checkpoints, and surface only consequential decisions. A report is not “verified” merely because it is well formatted.

| Path | Writer | Purpose |
|---|---|---|
| `SPEC.md` | **human only** | The living spec: claims, falsifiers, constraints, current beliefs. Agents read it at the start of every task and never edit it. |
| `PAPER/` | **human only** | The manuscript. Agents may be asked to *check* it, never to write into it. |
| `HUMAN/` | **human only** | Reading notes, decision records, thinking. |
| `SHARED/` | human + agents | Living literature review, dead-end ledger, question queue, decisions log. Agents append; you prune. |
| `AGENT/` | human (agents read) | The agent charter, philosophy, protocol, rubrics and templates. Inspect and edit freely; this is the meta that steers every agent. |
| `AgentWork/` | agents | Everything an agent produces while working. Scratch, logs, plans, drafts. Treated as disposable; never cited directly. |
| `Reports/` | agents (fixed template) | Reports plus machine-readable manifests. Evidence is hashed and remains `candidate` until independently reproduced and criticized. |
| `lean/` | agents (checked by Lake) | Lake project. Each task's formal certificates go in `lean/Evidence/<TaskId>.lean`. No `sorry` is allowed in anything a report cites. |
| `Education/` | education agent (criteria human-edited) | The understanding loop. A scheduled agent reads validated reports and writes one short morning brief for the iPad: one concept as an explanatory spine, self-tests, spaced retrieval, backlog triage. See `AGENT/PRINCIPLES.md` for the two-loop model. |
| `tools/` | human | Scaffolding, validation, digest, queue, guards. |

## Daily shape

```
morning   make attention; answer only consequential questions; do one prompt-first understanding exercise
day       agents run bounded fallback ladders, checkpoint, reproduce, criticize, and resume independently
evening   inspect only newly verified claims or foundational challenges; acknowledge digest when actually read
```

## Setup

```
make init          # installs git hooks, creates lean toolchain if available
make task T="tighten the curvature bound under assumption A2"
make check         # validate every report + build Lean certificates
make digest        # what happened since the last digest
make queue         # open questions waiting on you
make attention     # the smallest packet that genuinely needs human attention
```

## Understanding loop

Validated findings pile up faster than you can assimilate them; that backlog is triaged, not eliminated (`AGENT/PRINCIPLES.md`). Each SPEC claim carries `Assimilated:` (only you edit it) and `Tier: verify|tool|study`. The education agent proposes tiers in `Education/backlog.md` and teaches one `study` item per morning. A concept counts as assimilated when you pass the three self-tests (reconstruct, predict, transfer), not when you've read the brief.

## Guards

- `.claude/settings.json` denies agent edits to `SPEC.md`, `PAPER/`, `HUMAN/`.
- The pre-commit hook rejects any commit touching those paths unless `HUMAN=1` is set in the environment.
  You commit with `HUMAN=1 git commit ...`; agents cannot.
- `tools/check_report.py` enforces claim IDs, typed states, frozen hashes, provenance, independent-review records, and status consistency.
- `tools/gate.py` is the only normal path to `verified`; it requires a different producer, reproducer, and critic.
- Run agents in separate worktrees or filesystem sandboxes when available, then run `tools/check_role_writes.py <role>` before accepting their changes. Prompt rules and Git hooks are defense in depth, not a security boundary.

## Epistemic state machine

`candidate → reproduced → criticized → verified`. The education loop reads only `verified` manifests. Foundational challenges are preserved and replicated rather than blocked or hidden. Brief and digest cursors commit only after successful completion, so crashes and missed runs are safe to retry.

## Human attention contract

Agents decide reversible technical details, retry transient failures, and use pre-approved fallback branches. They interrupt only for a changed scientific target, a replicated foundational contradiction, an irreversible/external action, or a budget breach. Everything else is batched into pull-based review windows. Research truth remains in `SPEC.md`; demonstrated human capability remains separately in `Education/UNDERSTANDING.md` and the append-only understanding events.

## Agent entry point

`CLAUDE.md` and `AGENTS.md` at the root both point to `AGENT/CHARTER.md`, so Claude Code, Codex-style tools and anything else that reads a root instruction file get the same charter.
