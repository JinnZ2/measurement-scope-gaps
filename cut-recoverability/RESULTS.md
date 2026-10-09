# RESULTS — run 2026-10-08

Toy settings (all toy runs): K=6 latents, 2 objects per latent per
discipline, SGNS dim 16, window 3, 4 negatives, lr 0.05, 6000 base docs.
Cross pairs: 12 coupled vs 132 uncoupled. Within-discipline control AUC
= 1.000 in every cell of every run.

## 1  Shared-term leak sweep (`cut_recover.py`, 3 seeds)

```
leak   ep1    ep3    ep6
0.00   0.48   0.44   0.43
0.05   0.59   0.74   0.84
0.20   0.93   0.98   1.00
0.50   1.00   1.00   1.00
1.00   1.00   1.00   1.00
```

## 2  Translator docs at leak 0 (`cut_bridge.py`)

```
bridge  seeds  ep1    ep3    ep6    cos coupled / uncoupled (ep6)
0.00    10     0.47   0.46   0.49   +0.153 / +0.154
0.01    5      0.57   0.59   0.59
0.05    5      0.56   0.50   0.46
0.20    5      0.67   0.64   0.58
```

OBSERVED: leak-0 below-0.5 drift in run 1 was noise (10 seeds, equal cosines).

## 3  Hop sweep (`cut_hops.py`, 5 seeds, 10% docs per chain link)

```
hops   ep1    ep3    ep6
2      0.55   0.71   0.81   shared term, leak 0.05
3      0.61   0.58   0.56   t1–t2
4      0.91   0.93   0.95   t1–X–t2
5      0.61   0.61   0.61
6      0.54   0.61   0.66
```

FALSIFIED here: "hop count sets recoverability" (proposed after run 2).

## 4  Parity / hub / volume (`cut_parity.py`, 5 seeds)

```
arm           ep1    ep3    ep6
hop7          0.46   0.45   0.46
hop8          0.60   0.59   0.57
hop3 + hub    0.85   0.86   0.84
hop2 @0.10    0.73   0.86   0.94
```

Combined at ep6:

```
arm           AUC    shared center node
hop2 @0.10    0.94   yes
hop4          0.95   yes
hop3 + hub    0.84   yes
hop2 @0.05    0.81   yes
hop6          0.66   yes (far)
hop5          0.61   no
hop8          0.57   yes (far)
hop3          0.56   no
leak 0        0.49   —
hop7          0.46   no
```

OBSERVED  even > adjacent odd at every pair (4>3, 6>5, 8>7)
OBSERVED  one hub added to direct pairing: 0.56 → 0.84
OBSERVED  volume-matched shared term ≈ one-middle chain (0.94 vs 0.95)
DERIVED   in SGNS geometry, recoverability tracks a shared center node both
          sides attach to; a shared term and a middle term are the same structure
DERIVED   SGNS groups words by shared neighbors, not by co-occurrence, so a
          direct term–term pairing leaves no center node
OBSERVED  far center nodes (hop 6, 8) decay toward chance; edge within ~1 sd

## 5  Real embedding (`real_probe.py`, en_core_web_md, 300-d, 20k rows)

Set mean cosine:

```
septic×hydro   +0.230
septic×tax     +0.106
hydro×tax      +0.088
centroid cos(septic, hydro)  +0.354
```

Hub score = min(cos to septic centroid, cos to hydro centroid),
percentile against all 20k vectors (vocab median +0.032, 99th pct +0.257):

```
term          toS     toH     hub     pct
aquifer      +0.627  +0.418  +0.418   99.93
siltation    +0.377  +0.357  +0.357   99.81   (same row as erosion)
sediment     +0.427  +0.259  +0.259   99.05
groundwater  +0.468  +0.241  +0.241   98.80
hydraulic    +0.236  +0.247  +0.236   98.69
flow         +0.300  +0.205  +0.205   97.53
gravity      +0.225  +0.183  +0.183   96.53
percolation  +0.314  +0.181  +0.181   96.36   (same row as drainage)
pressure     +0.253  +0.131  +0.131   91.19
discharge    +0.326  +0.119  +0.119   89.00
biofilm      +0.398  +0.106  +0.106   86.13
viscosity    +0.237  +0.075  +0.075   74.42
gradient     +0.183  +0.069  +0.069   71.69
head         +0.168  -0.016  -0.016   19.30
```

OBSERVED  septic and hydro sit closer to each other than either does to tax
OBSERVED  shared physics variables occupy the top 1–4% of the vocabulary
          for sitting between both sets
OBSERVED  "head" — the governing variable in both — sits below the vocabulary
          median; "gradient" near 72nd pct
PROPOSED  the word of the shared variable is held by another sense (body,
          math/ML), so the center node exists in physics and is missing in the
          geometry. Polysemy acts as a renaming cut.

## Scope limits

- toy SGNS only; W-vectors probed; one latent per object; symmetric disciplines
- 3–10 seeds; hop 6/8 parity edge within ~1 sd
- chain arms fix docs per link, so longer chains carry more text (biased toward recovery)
- real probe: the md vector table has 20k rows for 685k keys; words are merged
  onto shared rows. Merged in this probe: septic=sewage=sludge,
  turbine=dam=penstock, hydroelectric=spillway, percolation=drainage,
  siltation=erosion. Within-hydro cosine (+0.827) is inflated by this.
  The merge is itself a compression cut and was not designed into the probe.
- real probe has no ground-truth coupled/uncoupled pairs; it reads structure, not recoverability
- term lists chosen by hand; no sense tagging

## Unrun

- sense-tagged "head" (hydraulic head vs body) in a full-vocabulary model
- recoverability probe on real data with a physics-derived coupling list
- same toy under a transformer objective

## 6  Different geometry builder (`cut_ppmi.py`, 10 seeds, numpy, 8 s)

Same corpora as runs 1–4. PPMI rows (first-order) and PPMI→SVD16.

```
arm         PPMI raw   PPMI-SVD16
leak0       0.500      0.500
hop2@0.05   1.000      1.000
hop2@0.10   1.000      1.000
hop3        0.500      0.346 ± 0.058   ← below chance
hop3+hub    0.500      1.000
hop4        0.500      1.000
hop5        0.500      0.497
hop6        0.500      1.000
hop7        0.500      0.558
hop8        0.500      1.000
```

OBSERVED  SVD: every even path recovers fully, no decay with distance;
          every odd path at or below chance
OBSERVED  direct term–term pairing (hop3) sits BELOW chance under SVD:
          coupled pairs pushed apart
OBSERVED  raw PPMI rows: only a shared term recovers; all chains read 0.5
DERIVED   SVD of a symmetric co-occurrence matrix = eigenvectors of P²;
          P² joins only even-length paths. Parity is linear algebra on a
          path-like co-occurrence graph, not an SGNS optimizer effect.
DERIVED   SGNS shows the same parity, blurred, with decay over distance;
          SGNS approximates a shifted-PMI factorization (Levy & Goldberg
          2014), consistent with the blur
SCOPE     toy chains are clean paths; real graphs carry odd cycles that
          would mix parity. Untested on real data.

## 7  Odd-cycle dose (`cut_oddcycle.py`, PPMI→SVD16, 10 seeds, 14 s)

Triangle per chain link with probability DOSE (doc gets a link token Z).

```
hops  0.00   0.02   0.10   0.30   1.00
3     0.32   0.97   1.00   1.00   1.00
4     1.00   0.93   1.00   1.00   1.00
5     0.50   0.79   0.16   0.00   0.00
6     1.00   0.41   0.00   0.00   0.00
```

OBSERVED  hop3 recovers at 2% dose — Z is a shared neighbor of both terms
          (the hub rule again, not parity washing out)
OBSERVED  hop5/6 at dose ≥0.1 → AUC 0.00: perfect separation, sign inverted
DERIVED   AUC far below 0.5 = information PRESENT, read upside down by a
          similarity probe. Measurand must be two-sided:
          separability = 2·|AUC−0.5|, sign reported separately
DERIVED   under that reading, with triangles present every chain carries
          the coupling fully; only the sign varies. Leak 0 (no path) is the
          only true zero in every run so far.
OPEN      mechanism of the inversion (likely SVD discarding eigenvalue
          sign; untested)

## 8  Eigenvalue-sign mechanism test (`cut_eigsign.py`, 10 seeds, 6 s)

```
hops dose   SVD(|λ|)   EIG(λ>0)   signed metric (Σλ·u·u)
3    0.0    0.32       0.04       1.00
3    0.3    1.00       0.00       0.62
5    0.0    0.47       0.10       1.00
5    0.3    0.00       0.39       0.00
6    0.0    1.00       0.28       0.45
6    0.3    0.00       0.43       0.00
```

OBSERVED  signed metric reads clean ODD chains correctly (1.00);
          |λ| (SVD) reads clean EVEN chains correctly (1.00)
DERIVED   signed metric ≈ P (odd path powers); |λ| ≈ P² (even powers)
          → each similarity reading resolves one parity, inverts the other
OBSERVED  dose 0.3, hops 5/6: inverted under both → eigen-sign is part of
          the cause, not all of it. OPEN.
DERIVED   no single similarity reading is right for every structure;
          two-sided separability recovers every arm except leak 0

## 9  Reading disagreement as its own field (`cut_readings.py`, 10 seeds, 12 s)

Four readings per cross pair, z-scored across pairs.
DISAGREE = std across readings · MAXABS = max |z|.

```
arm    dose   R1svd  R2sgn  R3pos  R4raw | DISAGREE  MAXABS
leak0  0.0    0.50   0.50   0.50   0.50  |  0.50     0.50
hop3   0.0    0.32   1.00   0.08   0.50  |  0.89     0.83
hop3   0.3    1.00   0.58   0.00   0.50  |  0.99     0.95
hop4   0.0    1.00   0.25   0.00   0.50  |  0.99     0.97
hop4   0.3    1.00   1.00   0.21   0.50  |  0.99     1.00
hop5   0.0    0.52   1.00   0.09   0.50  |  0.98     0.98
hop5   0.3    0.01   0.02   0.39   0.50  |  1.00     1.00
hop6   0.0    1.00   0.51   0.26   0.50  |  0.97     0.98
hop6   0.3    0.00   0.00   0.43   0.50  |  1.00     1.00
```

OBSERVED  every single reading fails somewhere (chance or inverted)
OBSERVED  DISAGREE locates coupled pairs in every arm with a path
          (0.89–1.00), and stays at 0.50 where no path exists
DERIVED   the split between readings is itself the detector; it needs no
          sign convention and no choice of "correct" reading
SCOPE     z-scoring is population-relative: works because coupled pairs
          are a minority (12/144). Untested at high coupled fraction.

## 10  Pilot: disagreement on real vectors (`real_readings.py`)

en_core_web_md, 10 hand-labelled coupled cross-discipline pairs vs 90
cross-pairings. Readings available on static vectors only.

```
cosine        0.68
centered      0.65
neg-euclid    0.62
nbr-overlap   0.60   (top-50 neighbors: zero overlap for 7/10 coupled pairs)
DISAGREE      0.45
MAXABS        0.50
```

OBSERVED  single readings weakly above chance; disagreement field fails
DERIVED   the four readings are near-copies of one geometry (all computed from
          the same static vectors), so their split carries no information.
          In the toy, readings came from structurally different operators
          (P vs P², sign kept vs dropped). The detector needs readings that
          differ in structure, which a finished static embedding does not offer.
SCOPE     n=10 coupled, labels hand-chosen, one model; pilot only
NEXT      real raw corpus → build co-occurrence matrix → structurally
          different readings (P, P², signed) → rerun
