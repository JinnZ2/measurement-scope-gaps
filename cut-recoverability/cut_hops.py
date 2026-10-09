#!/usr/bin/env python3
"""cut_hops.py — CC0, stdlib only. Branch B: hop sweep.
Object-to-object co-occurrence path length forced explicitly.
  hops 2 : shared physics term, leak 0.05 (object–P–object), reference arm
  hops 3 : chain D1_t – D2_t                      (bridge, no intermediates)
  hops 4 : chain D1_t – X1 – D2_t
  hops 5 : chain D1_t – X1 – X2 – D2_t
  hops 6 : chain D1_t – X1 – X2 – X3 – D2_t
Chain docs: each link gets PER_LINK * DOCS docs (fixed per link, so longer
chains carry MORE total bridge text — biased toward recovery).
"""
import math, random
import cut_recover as cr

PER_LINK = 0.10

def corpus_chain(objs, n_mid, rng):
    docs = cr.corpus(objs, 0.0, rng)
    for k in range(cr.K):
        chain = [f"D1_t{k}"] + [f"X{j}_{k}" for j in range(n_mid)] + [f"D2_t{k}"]
        for a, b in zip(chain, chain[1:]):
            for _ in range(int(cr.DOCS * PER_LINK / cr.K)):
                doc = [a, b] + [f"C_f{rng.randrange(cr.FILLER)}" for _ in range(3)]
                rng.shuffle(doc)
                docs.append(doc)
    return docs

def main():
    objs, cps, seeds = cr.build_world(), [1, 3, 6], [11, 22, 33, 44, 55]
    arms = [(2, lambda r: cr.corpus(objs, 0.05, r))] + \
           [(3 + m, (lambda m: lambda r: corpus_chain(objs, m, r))(m)) for m in range(4)]
    print("hops epoch  cross_AUC(mean±sd)  within")
    for hops, make in arms:
        res = {c: [] for c in cps}
        for s in seeds:
            rng = random.Random(s)
            snaps = cr.train(make(rng), rng, cps)
            for c in cps:
                res[c].append(cr.probe(snaps[c], objs))
        for c in cps:
            xs = [r[0] for r in res[c]]
            m = sum(xs) / len(xs); sd = math.sqrt(sum((v - m) ** 2 for v in xs) / len(xs))
            w = sum(r[1] for r in res[c]) / len(res[c])
            print(f"{hops:4d} {c:5d}  {m:.3f} ± {sd:.3f}    {w:.3f}", flush=True)

if __name__ == "__main__":
    main()
