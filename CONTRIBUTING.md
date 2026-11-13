# Contributing

Contributions should strengthen one of the repository's two objectives: severe, falsifiable research or rapid growth in demonstrated human understanding.

For changes to evidence gates, include a failure case the change prevents. For changes to the understanding loop, state what observable human capability should improve and how it would be measured. Avoid adding dashboards, prompts, or agent roles without showing that they reduce epistemic risk or human-attention cost.

Run before opening a pull request:

```sh
python3 -m py_compile tools/*.py
python3 tools/check_report.py
python3 tools/check_brief.py Education/BRIEF_TEMPLATE.md
```
