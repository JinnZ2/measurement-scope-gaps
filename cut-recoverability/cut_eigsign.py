#!/usr/bin/env python3
"""cut_eigsign.py — mechanism test for the sign inversion.
SVD (U*sqrt|s|) discards eigenvalue sign. Compare:
  SVD      top-16 by |eigenvalue|, sign dropped (as before)
  EIG+     top-16 POSITIVE eigenvalues only, U*sqrt(lambda)
  EIG±abs  top-16 by |lambda|, but cosine uses a signed metric:
           sim = sum lambda_i u_i(a) u_i(b) / norms  (P restricted to 16 dims)
If inversion vanishes under EIG+ / signed metric → eigenvalue sign is the cause.
"""
import random
import numpy as np
import cut_recover as cr, cut_oddcycle as oc

def builds(docs, dim=16):
    vocab = sorted({w for d in docs for w in d}); idx = {w: i for i, w in enumerate(vocab)}
    C = np.zeros((len(vocab),) * 2)
    for d in docs:
        ids = [idx[w] for w in d]
        for a, i in enumerate(ids):
            for b in range(max(0, a - cr.WIN), min(len(ids), a + cr.WIN + 1)):
                if a != b: C[i, ids[b]] += 1
    tot = C.sum(); r = C.sum(1, keepdims=True); c = C.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        P = np.log(C * tot / (r * c)); P[~np.isfinite(P)] = 0; P = np.maximum(P, 0)
    lam, U = np.linalg.eigh(P)
    top_abs = np.argsort(-np.abs(lam))[:dim]
    top_pos = np.argsort(-lam)[:dim]
    svd = U[:, top_abs] * np.sqrt(np.abs(lam[top_abs]))
    pos = U[:, top_pos] * np.sqrt(np.maximum(lam[top_pos], 0))
    L, Ua = lam[top_abs], U[:, top_abs]
    return idx, svd, pos, (Ua, L)

def probe_signed(idx, Ua, L, objs):
    def sim(a, b):
        x, y = Ua[idx[a]], Ua[idx[b]]
        num = np.sum(L * x * y)
        den = np.sqrt(np.abs(np.sum(L * x * x)) * np.abs(np.sum(L * y * y))) + 1e-12
        return num / den
    pos, neg = [], []
    for (a, ka) in objs["D1"]:
        for (b, kb) in objs["D2"]:
            (pos if ka == kb else neg).append(sim(a, b))
    return cr.auc(pos, neg)

def main():
    objs, seeds = cr.build_world(), range(401, 411)
    cases = [(n, d) for n in (0, 2, 3) for d in (0.0, 0.3)]
    print("hops dose   SVD(|λ|)   EIG(λ>0)   signed-metric")
    for n_mid, dose in cases:
        r = {"svd": [], "pos": [], "sgn": []}
        for s in seeds:
            idx, svd, pos, (Ua, L) = builds(oc.corpus_chain_odd(objs, n_mid, dose, random.Random(s)))
            vocab = list(idx)
            r["svd"].append(cr.probe({w: svd[idx[w]] for w in vocab}, objs)[0])
            r["pos"].append(cr.probe({w: pos[idx[w]] for w in vocab}, objs)[0])
            r["sgn"].append(probe_signed(idx, Ua, L, objs))
        f = lambda xs: f"{np.mean(xs):.2f}±{np.std(xs):.2f}"
        print(f"{3+n_mid:4d} {dose:4.1f}   {f(r['svd'])}  {f(r['pos'])}  {f(r['sgn'])}", flush=True)

if __name__ == "__main__":
    main()
