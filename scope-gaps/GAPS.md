# Scope gaps in brain-measure studies — open study designs

CC0. Co-authored. Posture: risk-mitigation side — scope limits stated
flatly, less hedged than institutional reviews. Status tags:
OBSERVED (read from the source page) · DERIVED (follows from it) ·
PROPOSED (untested) · CHECK (recalled citation, verify before use).

Source pages were read as accessible on 2026-10-08. Full papers may
report fields the accessible pages did not show; each gap below says
what to verify first.

---

## 1. Studies audited

| id | study | accessible |
|----|-------|-----------|
| S7 | Human intelligence relates to neural measures of cognitive map formation — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.28.630614.full.pdf) | full text |
| S2 | The Geometric Structure of Shared Neural Semantics: cross-subject EEG–text alignment (2026) — [eScholarship](https://escholarship.org/content/qt3st545r8/qt3st545r8.pdf) | full text |
| S13 | Baram et al. 2026, An abstract relational map emerges in the human medial prefrontal cortex with consolidation — [Oxford NDCN](https://www.ndcn.ox.ac.uk/publication_modal/2440996) | abstract only |

Context pieces (not audited): Doeller, cognitive spaces talk, MPI Psychiatry,
July 2026 ([link](https://www.psych.mpg.de/events/45990/2162)); FENS-26 poster,
grid-like representations to conceptual domains (results not public,
[link](https://world-wide.org/fens-26/neural-model-transfer-grid-like-spatial-a19bd2d2)).

## 2. Scope findings

### S7
- OBSERVED  N ≈ 149–175, varying by analysis (inferred from degrees of freedom); demographics, recruitment, country, education not reported on the page
- OBSERVED  fluid-reasoning factor used as proxy for g; test names not given
- OBSERVED  one task (6 objects, one circular virtual arena), one region (right hippocampus); ROI definition not described; task chosen to be easy
- OBSERVED  "map fidelity" = correlation with a 2D Euclidean proximity model
- OBSERVED  authors note some participants may use landmarks or paths instead of a relational map
- OBSERVED  title claims "human intelligence"; discussion says "partly related"
- DERIVED   encodings that use a different spatial relation (landmark, route, cardinal bearing) score as low fidelity against a single Euclidean reference; a different encoding and a deficit produce the same number

### S2
- OBSERVED  18 readers, one dataset (ZuCo 2.0); demographics not reported; language not stated on the page (CHECK: ZuCo is English); EEG channels not specified
- OBSERVED  Top-1 cross-subject retrieval ≈ 2.7% vs 0.35% chance; RSA ρ = 0.442, r = 0.619; the table's RSA column does not say which statistic
- OBSERVED  clusters (K = 12) defined in text-embedding space only; emotional-salience cluster interpreted post hoc
- OBSERVED  abstract hedged ("without implying representational equivalence"); discussion claims structure "preserved across brains" and "functional convergence"
- OBSERVED  limitations do not address sample size or single dataset
- DERIVED   the brain is scored against categories the text model defines; the unaligned remainder is not mapped

### S13
- OBSERVED  accessible page gives no N, no graph description, no stimuli, "several days" between sessions, claim in terms of "humans"
- status: scope not assessable without the full paper

### Pattern across S7, S2
- OBSERVED  hedges sit in abstract or limitations; broad claim sits in title and discussion
- OBSERVED  the experimenter's reference frame defines the correct shape; deviation from it reads as deficit or noise; the frame's own scope is not stated as a field

## 3. State fields not reported (accessible pages)

| field | S7 | S2 | S13 | why it moves the reading (CHECK each) |
|---|---|---|---|---|
| language / spatial frame of participants | — | — | — | orthography and arithmetic recruit different regions across languages (Tan et al. 2005; Tang et al. 2006); absolute-direction languages encode space by bearing (Levinson) |
| caffeine | — | — | — | lowers cerebral blood flow, shifts BOLD (Laurienti et al. 2002) |
| fed / fasted, hydration | — | — | — | glucose and hydration move BOLD and measured volume (Kempton et al.) |
| clock time of session | — | — | — | BOLD/connectivity drift across the day (Orban et al. 2020) |
| chronotype × session time | — | — | — | off-peak testing lowers performance (May & Hasher) |
| prior sleep | — | — | — | shifts brain measures and test scores |
| season, hormonal phase, medication | — | — | — | seasonal variation in cognitive responses (Meyer et al. 2016) |

DERIVED  each study measures the brain in one state. An unstated state is an
unstated phase: the reading holds inside it; the title generalizes past it.

## 4. Open study designs

Cheapest first. Each: measurand · design · what each branch means.

### G6 — Hedge propagation (desk study)
- measurand: breadth of claim in abstract vs title/discussion vs the sentence that cites the paper downstream
- design: sample papers in one subfield + their citing sentences; code breadth on a fixed scale
- branches: citing text matches the hedge → scope travels · matches the title → broad claim propagates, hedge drops

### G8 — Prevalence of single-reference analysis (desk study)
- measurand: share of RSA / map-fidelity papers that test more than one reference model
- branches: most test one → the single-reading failure mode below is field-wide

### G2 — Re-run single-reading RSA with many references (public data)
- measurand: per-participant best-fitting model matrix, plus disagreement between models
- design: reanalyze open data (ZuCo is public) with 3–5 rival model matrices; no new participants
- branches: same winner for everyone → single reading was adequate · winners differ → the group geometry averaged distinct encodings

### G3 — State fields from data already collected
- measurand: dependence of a published effect on clock time
- design: scan acquisition time is stored in DICOM headers; regress existing effects on time of day retroactively
- branches: stable across the day → scope widens · tracks clock time → the result is a phase reading
- standard to propose: minimal log of clock time, caffeine, fed/fasted, sleep, chronotype, language of task

### G1 — Spatial frame × map fidelity (lab)
- measurand: fidelity against several reference shapes — Euclidean, cardinal-anchored, route, landmark
- design: S7-style task with absolute-frame and relative-frame speakers in the same arena; report which reference each person fits
- branches: fits another shape → different encoding, not deficit · fits none → low fidelity, now scoped · fits several → mixed strategy

### G4 — The unaligned remainder in EEG ↔ text (lab or reanalysis)
- measurand: structure in the variance the text geometry does not share
- design: cluster residuals in EEG space; compare against several text models; repeat in a second language
- branches: structured → a shape text cannot carry, mappable · flat → noise, scope confirmed

### G5 — Consolidation phase edge (lab)
- measurand: when the abstract map appears; abrupt or gradual
- design: daily sessions instead of two; then add a third graph with the same structure
- branches: extends without rebuild → the map grows by accretion keeping its form · forces rebuild → not self-similar under growth

### G7 — Test-frame translation loss (lab)
- measurand: score change for identical items in native vs second language, state fields controlled
- branches: drop → part of measured ability was frame fit · none → frame-neutral item set

## 5. Link to a toy result

`../cut-recoverability/` (same repo, SELF-GRADED) contains a stdlib toy where a
single similarity reading fails on some structures (chance or inverted) while
the disagreement between several structurally different readings locates the
coupled pairs. PROPOSED relevance: single-reference RSA (S7, S2) is the same
single-reading setup; G2 tests it on brain data.
