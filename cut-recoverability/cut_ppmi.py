#!/usr/bin/env python3
"""cut_ppmi.py — is the shared-hub rule an SGNS artifact?
Same corpora as the SGNS runs, different geometry builders:
  PPMI      co-occurrence (window 3) -> positive PMI rows, cosine
  PPMI-SVD  PPMI -> truncated SVD (dim 16), U*sqrt(S)
Deterministic per corpus; 10 seeds vary the corpus. numpy.
"""
import random, math
import numpy as np
import cut_recover as cr, cut_hops as ch, cut_parity as cp

def build(docs, dim=16):
    vocab = sorted({w for d in docs for w in d}); idx = {w: i for i, w in enumerate(vocab)}
    C = np.zeros((len(vocab), len(vocab)))
    for d in docs:
        ids = [idx[w] for w in d]
        for a, i in enumerate(ids):
            for b in range(max(0, a - cr.WIN), min(len(ids), a + cr.WIN + 1)):
                if a != b: C[i, ids[b]] += 1
    tot = C.sum(); r = C.sum(1, keepdims=True); c = C.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        P = np.log(C * tot / (r * c)); P[~np.isfinite(P)] = 0; P = np.maximum(P, 0)
    U, S, _ = np.linalg.svd(P)
    E = U[:, :dim] * np.sqrt(S[:dim])
    return ({w: list(P[idx[w]]) for w in vocab}, {w: list(E[idx[w]]) for w in vocab})

def main():
    objs = cr.build_world(); seeds = range(201, 211)
    arms = [("leak0",      lambda r: cr.corpus(objs, 0.0, r)),
            ("hop2@0.05",  lambda r: cr.corpus(objs, 0.05, r)),
            ("hop2@0.10",  lambda r: cr.corpus(objs, 0.10, r)),
            ("hop3",       lambda r: ch.corpus_chain(objs, 0, r)),
            ("hop3+hub",   lambda r: cp.corpus_direct_plus_hub(objs, r)),
            ("hop4",       lambda r: ch.corpus_chain(objs, 1, r)),
            ("hop5",       lambda r: ch.corpus_chain(objs, 2, r)),
            ("hop6",       lambda r: ch.corpus_chain(objs, 3, r)),
            ("hop7",       lambda r: ch.corpus_chain(objs, 4, r)),
            ("hop8",       lambda r: ch.corpus_chain(objs, 5, r))]
    print("arm         PPMI(raw)        PPMI-SVD16       within(raw/svd)")
    for name, make in arms:
        raw, svd = [], []
        for s in seeds:
            P, E = build(make(random.Random(s)))
            raw.append(cr.probe(P, objs)); svd.append(cr.probe(E, objs))
        f = lambda xs: (np.mean([x[0] for x in xs]), np.std([x[0] for x in xs]),
                        np.mean([x[1] for x in xs]))
        a, b = f(raw), f(svd)
        print(f"{name:10s}  {a[0]:.3f} ± {a[1]:.3f}    {b[0]:.3f} ± {b[1]:.3f}    {a[2]:.2f}/{b[2]:.2f}", flush=True)

if __name__ == "__main__":
    main()
