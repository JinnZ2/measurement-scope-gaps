#!/usr/bin/env python3
"""cut_bridge.py — CC0, stdlib only. Extends cut_recover.py.
Branch A: leak = 0 (each discipline uses only its own term), plus a
  fraction BRIDGE of extra docs containing BOTH discipline terms for one
  latent and no objects (a translator layer: textbook using both names).
Branch C: 10 seeds at bridge 0 to settle the below-chance drift; reports
  mean cosine of coupled vs uncoupled cross pairs.
"""
import math, random, itertools
import cut_recover as cr

def corpus_bridge(objs, bridge, rng):
    docs = cr.corpus(objs, 0.0, rng)
    for _ in range(int(cr.DOCS * bridge)):
        k = rng.randrange(cr.K)
        doc = [f"D1_t{k}", f"D2_t{k}"] + [f"B_f{rng.randrange(cr.FILLER)}" for _ in range(3)]
        rng.shuffle(doc)
        docs.append(doc)
    return docs

def cross_means(E, objs):
    pos, neg = [], []
    for (a, ka), (b, kb) in itertools.product(objs["D1"], objs["D2"]):
        (pos if ka == kb else neg).append(cr.cos(E[a], E[b]))
    return sum(pos) / len(pos), sum(neg) / len(neg)

def main():
    objs, cps = cr.build_world(), [1, 3, 6]
    plan = [(0.0, list(range(101, 111))), (0.01, [11, 22, 33, 44, 55]),
            (0.05, [11, 22, 33, 44, 55]), (0.20, [11, 22, 33, 44, 55])]
    print("bridge seeds epoch  cross_AUC(mean±sd)  within  cos_coupled  cos_uncoupled")
    for bridge, seeds in plan:
        res = {c: [] for c in cps}
        for s in seeds:
            rng = random.Random(s)
            snaps = cr.train(corpus_bridge(objs, bridge, rng), rng, cps)
            for c in cps:
                x, w = cr.probe(snaps[c], objs)
                res[c].append((x, w) + cross_means(snaps[c], objs))
        for c in cps:
            col = list(zip(*res[c]))
            m = sum(col[0]) / len(col[0])
            sd = math.sqrt(sum((v - m) ** 2 for v in col[0]) / len(col[0]))
            avg = [sum(v) / len(v) for v in col[1:]]
            print(f"{bridge:5.2f} {len(seeds):5d} {c:5d}  {m:.3f} ± {sd:.3f}    "
                  f"{avg[0]:.3f}   {avg[1]:+.3f}       {avg[2]:+.3f}", flush=True)

if __name__ == "__main__":
    main()
