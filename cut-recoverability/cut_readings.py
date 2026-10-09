#!/usr/bin/env python3
"""cut_readings.py — reading choice as a cut.
Four similarity readings per cross pair:
  R1 SVD |λ| cosine   R2 signed metric   R3 λ>0 cosine   R4 raw PPMI cosine
Each z-scored across all cross pairs. Per pair:
  DISAGREE = std of the four z-scores  (where readings split)
  MAXABS   = max |z|                   (any reading sees structure, either sign)
Report AUC (coupled vs uncoupled) for each single reading, DISAGREE, MAXABS.
Question: does disagreement between readings itself locate the cut?
"""
import random, itertools
import numpy as np
import cut_recover as cr, cut_oddcycle as oc, cut_eigsign as es

def readings(docs, objs):
    idx, svd, pos, (Ua, L) = es.builds(docs)
    vocab = sorted(idx)
    # raw PPMI rows
    C = np.zeros((len(idx),) * 2)
    for d in docs:
        ids = [idx[w] for w in d]
        for a, i in enumerate(ids):
            for b in range(max(0, a - cr.WIN), min(len(ids), a + cr.WIN + 1)):
                if a != b: C[i, ids[b]] += 1
    tot = C.sum(); r = C.sum(1, keepdims=True); c = C.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        P = np.log(C * tot / (r * c)); P[~np.isfinite(P)] = 0; P = np.maximum(P, 0)
    def cos(M, a, b):
        x, y = M[idx[a]], M[idx[b]]
        return float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
    def sgn(a, b):
        x, y = Ua[idx[a]], Ua[idx[b]]
        return float(np.sum(L * x * y) / (np.sqrt(abs(np.sum(L * x * x)) * abs(np.sum(L * y * y))) + 1e-12))
    pairs = list(itertools.product(objs["D1"], objs["D2"]))
    R = np.array([[cos(svd, a, b), sgn(a, b), cos(pos, a, b), cos(P, a, b)]
                  for (a, _), (b, _) in pairs])
    lab = np.array([ka == kb for (_, ka), (_, kb) in pairs])
    Z = (R - R.mean(0)) / (R.std(0) + 1e-12)
    return R, Z, lab

def auc(score, lab):
    return cr.auc(list(score[lab]), list(score[~lab]))

def main():
    objs, seeds = cr.build_world(), range(501, 511)
    arms = [("leak0", None, 0.0)] + [(f"hop{3+n}", n, d) for n in range(4) for d in (0.0, 0.3)]
    print("arm        dose   R1svd  R2sgn  R3pos  R4raw | DISAGREE  MAXABS")
    for name, n_mid, dose in arms:
        acc = []
        for s in seeds:
            rng = random.Random(s)
            docs = cr.corpus(objs, 0.0, rng) if n_mid is None else oc.corpus_chain_odd(objs, n_mid, dose, rng)
            R, Z, lab = readings(docs, objs)
            acc.append([auc(R[:, i], lab) for i in range(4)] +
                       [auc(Z.std(1), lab), auc(np.abs(Z).max(1), lab)])
        m = np.mean(acc, 0)
        print(f"{name:9s} {dose:4.1f}   " + "  ".join(f"{v:.2f} " for v in m[:4]) +
              f"|   {m[4]:.2f}     {m[5]:.2f}", flush=True)

if __name__ == "__main__":
    main()
