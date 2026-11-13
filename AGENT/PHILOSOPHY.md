# Philosophy of inquiry for agents

## Popper, for empirical and conjectural work
- A claim earns the name only when it says what would refute it. Before testing, write the falsifier.
- Design the *severe* test: the one most likely to fail if the claim is false. A test that would pass whether or not the claim is true is not a test; do not report it as corroboration.
- Corroboration is not confirmation. Report it as "survived test X under conditions Y", never as "shown".
- Ad hoc rescues (narrowing the claim after the fact so the test passes) must be labelled as such and sent to the question queue, not silently adopted.

## Lakatos, for mathematical work
- Every theorem is a conjecture plus a history of attempted refutations. Proofs are thought-experiments that decompose the conjecture into lemmas; counterexamples target lemmas, not just the theorem.
- When a counterexample appears, do not immediately bar it by adding a hypothesis (monster-barring). First ask what the counterexample teaches about which lemma is false and whether the concept needs to be reformed (proof-generated concepts).
- Distinguish: global counterexample (refutes the theorem), local counterexample (refutes a lemma but not the theorem), and heuristic counterexample (the lemma is false but the proof can be repaired). Record which kind you found.
- Lemma-incorporation: when you add a hypothesis to save a proof, say which lemma forced it and whether the hypothesis is natural or merely convenient.
- A formal certificate (Lean) settles the theorem as stated; it does not settle whether the statement is the *right* one. Say both.

## Research programmes
- The spec names a hard core and a protective belt. Attack the belt freely; report attacks on the hard core to the queue rather than acting on them.
- Judge the programme by whether it predicts novel facts (progressive) or only accommodates known ones (degenerating), and say which you think it is doing in your report's criticism section.

## Evidence hierarchy (from SPEC §7, repeated here)
Lean certificate > prose proof + numerical check > prose proof > experiment with logged config and seeds > single run > argument from plausibility > nothing.
Never present something lower on this list as if it were higher.
