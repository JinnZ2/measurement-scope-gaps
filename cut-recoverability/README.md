# cut-recoverability

CC0. **SELF-GRADED** — scripts, runs and readings were produced by the same
agent; no independent check has been run. Co-authored.

Posture: risk-mitigation side. Results are reported as found, with scope
limits and the falsified branch kept in. Status tags: OBSERVED (in the
output), DERIVED (follows from outputs), PROPOSED (not tested).

## Question

If two things are coupled in the world (same physics) but a corpus keeps
them apart (different disciplines, different names), can an embedding's
geometry show that a cut happened **at all**?

Measurand: AUC of cosine similarity, coupled vs uncoupled cross-discipline
object pairs. 0.5 = the cut looks identical to "never related".
Positive control every run: same probe on within-discipline pairs.

## Files

```
cut_recover.py   toy world + skip-gram (SGNS) + probe; sweep of shared-term leak
cut_bridge.py    leak 0 + translator docs (both names, no objects); 10-seed null
cut_hops.py      forced path length 2..6 between the two disciplines' terms
cut_parity.py    hops 7 vs 8; direct pairing + one hub; volume-matched shared term
cut_ppmi.py      same corpora, PPMI and PPMI→SVD geometry (numpy)
cut_oddcycle.py  triangle dose on chains; sign inversion appears
cut_eigsign.py   eigenvalue-sign mechanism test
cut_readings.py  disagreement between readings as a detector
real_probe.py    septic vs hydro terms in a public embedding (needs numpy + model)
real_readings.py pilot: disagreement field on real vectors (fails; why in RESULTS)
load_vecs.py     reads spaCy en_core_web_md vectors without spaCy
self_delete.py   side tool: applies a claim's own criterion to its carrier
RESULTS.md       all tables, run order, readings, scope limits
```

Toy scripts cut_recover/bridge/hops/parity: stdlib only. Runs 6–9 use numpy. `python3 cut_recover.py` (~3 min, pure Python).
Real probe: numpy + the `en_core_web_md-3.8.0` wheel from the
explosion/spacy-models GitHub releases (installed, not loaded through spaCy).

## Run order and branch history

```
1 leak sweep          → leak 0 unrecoverable; 5% shared term recovers, training amplifies
2 bridge + 10 seeds   → null confirmed at chance; translator docs weak and fading
3 hop sweep           → "hop count sets it" PROPOSED, then FALSIFIED (non-monotone)
4 parity/hub/volume   → shared center node is the variable, not path length
5 real embedding      → shared-variable terms sit between septic and hydro;
                        "head" (the governing variable) does not — its word is held
                        by another sense
```

## What would extend it

- transformer-style training instead of SGNS
- multi-latent objects (one object governed by several quantities)
- real corpora with a ground-truth coupling list from physics, sense-tagged
- full-vocabulary embeddings (the md model merges words — see RESULTS.md)
