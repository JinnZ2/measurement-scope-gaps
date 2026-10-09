#!/usr/bin/env python3
"""cut_oddcycle.py — odd-cycle dose on the chain arms, PPMI→SVD16.
In each chain link doc (a, b), with probability DOSE add a link-specific
token Z: doc = [a, b, Z, fillers]. That makes triangle a–b–Z, so a→b is
reachable by paths of length 1 AND 2: both parities open. 10 seeds.
"""
import random
import numpy as np
import cut_recover as cr, cut_hops as ch, cut_ppmi as pp

def corpus_chain_odd(objs, n_mid, dose, rng):
    docs = cr.corpus(objs, 0.0, rng)
    for k in range(cr.K):
        chain = [f"D1_t{k}"] + [f"X{j}_{k}" for j in range(n_mid)] + [f"D2_t{k}"]
        for li, (a, b) in enumerate(zip(chain, chain[1:])):
            for _ in range(int(cr.DOCS * ch.PER_LINK / cr.K)):
                doc = [a, b] + ([f"Z{li}_{k}"] if rng.random() < dose else []) \
                      + [f"C_f{rng.randrange(cr.FILLER)}" for _ in range(3)]
                rng.shuffle(doc); docs.append(doc)
    return docs

def main():
    objs, seeds = cr.build_world(), range(301, 311)
    doses = [0.0, 0.02, 0.1, 0.3, 1.0]
    print("hops  " + "  ".join(f"dose{d:<5}" for d in doses))
    for n_mid in range(4):
        row = []
        for d in doses:
            xs = [cr.probe(pp.build(corpus_chain_odd(objs, n_mid, d, random.Random(s)))[1], objs)[0]
                  for s in seeds]
            row.append(f"{np.mean(xs):.2f}±{np.std(xs):.2f}")
        print(f"{3+n_mid:4d}  " + "  ".join(row), flush=True)

if __name__ == "__main__":
    main()
