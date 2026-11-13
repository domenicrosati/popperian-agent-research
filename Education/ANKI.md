# Mathematical Anki notes

Cards retain mathematical building blocks supporting a discovery. Favor definitions (for example an RKHS norm), theorem or lemma hypotheses, proof techniques such as the union bound, identities such as Woodbury, decompositions, complexity rates, and distinctions about when each applies.

Use at most three new cards per useful morning brief by default. No minimum, no weekend human obligation, no automatic reminders. Reading the original paper and working on paper takes priority.

## Authoring standard
One retrieval target per card, enough notation and assumptions to answer without yesterday's digest, concise answer, exact source location, and an explicit connection to the discovery. Definitions should include the mathematical object and its interpretation. Formula cards must test applicability or meaning as well as recall. Avoid full-proof recitation, ambiguous reversals, trivia, experimental scores, and unsupported project conjectures. A correct prerequisite does not validate the discovery.

Prefer pre-2023 foundational papers and textbooks. Post-2023 sources follow LITERATURE_POLICY.md. Source verification is an agent attestation, not a mathematical or automated citation proof.

## Storage
Education/anki/notes.json is an array. Each note has:
- id: stable descriptive ID, retained across edits
- concept: reusable concept
- kind: definition, theorem, lemma, technique, identity, decomposition, rate, or conceptual
- front and back: plain text with Anki MathJax delimiters
- source_title, source_url, source_location
- source_verified: true only after reading the actual passage
- discovery_link: repository path/claim or report explaining relevance
- tags: list of whitespace-free tags

Export: python3 tools/export_anki.py Education/anki/notes.json Education/anki/research.tsv

## One-time Anki setup
Create a note type named Research Math with fields ID, Front, Back, Source, Connection, in that order. Use Front as the front template and FrontSide followed by Back, Source, and Connection as the back template. ID is the first stored field for duplicate matching but is not displayed.

Import research.tsv as UTF-8 tab-separated text with HTML enabled. The headers select Research Math and map the sixth column to tags. Select update-existing behavior: stable IDs then update notes while preserving scheduling. Do not use these IDs as Anki internal GUIDs. Anki MathJax renders backslash-parenthesis and backslash-bracket notation.

No Anki app, account, or collection is modified by this repository. Import happens when the human chooses.

Reference: https://docs.ankiweb.net/importing/text-files.html
