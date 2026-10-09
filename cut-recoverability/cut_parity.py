#!/usr/bin/env python3
"""cut_parity.py — CC0, stdlib only. Branches P + V.
P  parity:  hops 7 (4 mids) vs hops 8 (5 mids)
P  hub:     hop 3 direct t1–t2 docs + one shared neighbor H (t1–H, H–t2)
            prediction if hub-not-hops: ≈ hop 4, not ≈ hop 3
V  volume:  hop 2 shared term at leak 0.10 (= per-link volume of chain arms)
"""
import math, random
import cut_recover as cr
import cut_hops as ch

def corpus_direct_plus_hub(objs, rng):
    docs = ch.corpus_chain(objs, 0, rng)             # t1–t2 direct
    for k in range(cr.K):
        for a, b in ((f"D1_t{k}", f"H_{k}"), (f"H_{k}", f"D2_t{k}")):
            for _ in range(int(cr.DOCS * ch.PER_LINK / cr.K)):
                doc = [a, b] + [f"C_f{rng.randrange(cr.FILLER)}" for _ in range(3)]
                rng.shuffle(doc)
                docs.append(doc)
    return docs

def main():
    objs, cps, seeds = cr.build_world(), [1, 3, 6], [11, 22, 33, 44, 55]
    arms = [("hop7",        lambda r: ch.corpus_chain(objs, 4, r)),
            ("hop8",        lambda r: ch.corpus_chain(objs, 5, r)),
            ("hop3+hub",    lambda r: corpus_direct_plus_hub(objs, r)),
            ("hop2@0.10",   lambda r: cr.corpus(objs, 0.10, r))]
    print("arm        epoch  cross_AUC(mean±sd)  within")
    for name, make in arms:
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
            print(f"{name:10s} {c:5d}  {m:.3f} ± {sd:.3f}    {w:.3f}", flush=True)

if __name__ == "__main__":
    main()
