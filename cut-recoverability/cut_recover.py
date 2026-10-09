#!/usr/bin/env python3
"""cut_recover.py — CC0, stdlib only.
Measurand: can embedding geometry tell that a CUT HAPPENED AT ALL?

World (ground truth, physics):  K latent quantities. Every object is
  governed by exactly one latent. Two objects are COUPLED iff same latent.
Institutions: two disciplines D1, D2. Objects of D1 never co-occur with
  objects of D2 (the cut). Each discipline names each latent its own way.
  With prob LEAK a document uses the shared physics term instead.
Corpus -> skip-gram negative-sampling embedding (pure python).
Probe: cosine between cross-discipline object pairs.
  AUC(coupled vs uncoupled) = 0.5  -> cut indistinguishable from no relation
  AUC > 0.5                        -> cut recoverable from geometry
Positive control: same probe on within-discipline pairs.
"""
import math, random, sys, itertools

K, OBJ_PER_LATENT, DIM = 6, 2, 16
DOCS, WIN, NEG, LR = 6000, 3, 4, 0.05
FILLER = 8

def build_world():
    objs = {d: [(f"{d}_o{k}{i}", k) for k in range(K) for i in range(OBJ_PER_LATENT)]
            for d in ("D1", "D2")}
    return objs

def corpus(objs, leak, rng):
    docs = []
    for _ in range(DOCS):
        d = rng.choice(("D1", "D2"))
        o, k = rng.choice(objs[d])
        term = f"P{k}" if rng.random() < leak else f"{d}_t{k}"
        fill = [f"{d}_f{rng.randrange(FILLER)}" for _ in range(3)]
        doc = [o, term] + fill
        rng.shuffle(doc)
        docs.append(doc)
    return docs

def train(docs, rng, checkpoints):
    vocab = sorted({w for doc in docs for w in doc})
    idx = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    W = [[(rng.random() - .5) / DIM for _ in range(DIM)] for _ in range(V)]
    C = [[0.0] * DIM for _ in range(V)]
    snaps, epochs = {}, max(checkpoints)
    for ep in range(1, epochs + 1):
        rng.shuffle(docs)
        for doc in docs:
            ids = [idx[w] for w in doc]
            for a, wi in enumerate(ids):
                for b in range(max(0, a - WIN), min(len(ids), a + WIN + 1)):
                    if a == b: continue
                    targets = [(ids[b], 1)] + [(rng.randrange(V), 0) for _ in range(NEG)]
                    grad = [0.0] * DIM
                    for t, lab in targets:
                        s = sum(x * y for x, y in zip(W[wi], C[t]))
                        g = LR * (lab - 1 / (1 + math.exp(-max(-30, min(30, s)))))
                        for j in range(DIM):
                            grad[j] += g * C[t][j]
                            C[t][j] += g * W[wi][j]
                    for j in range(DIM):
                        W[wi][j] += grad[j]
        if ep in checkpoints:
            snaps[ep] = {w: list(W[idx[w]]) for w in vocab}
    return snaps

def cos(a, b):
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / (na * nb + 1e-12)

def auc(pos, neg):
    win = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return win / (len(pos) * len(neg))

def probe(E, objs):
    cross_pos, cross_neg, in_pos, in_neg = [], [], [], []
    for (a, ka), (b, kb) in itertools.product(objs["D1"], objs["D2"]):
        (cross_pos if ka == kb else cross_neg).append(cos(E[a], E[b]))
    for d in ("D1", "D2"):
        for (a, ka), (b, kb) in itertools.combinations(objs[d], 2):
            (in_pos if ka == kb else in_neg).append(cos(E[a], E[b]))
    return auc(cross_pos, cross_neg), auc(in_pos, in_neg)

def main():
    leaks = [0.0, 0.05, 0.2, 0.5, 1.0]
    checkpoints = [1, 3, 6]
    seeds = [11, 22, 33]
    objs = build_world()
    print("leak  epoch  cross_AUC(mean±sd)   within_AUC(control)")
    rows = []
    for leak in leaks:
        res = {c: [] for c in checkpoints}
        for s in seeds:
            rng = random.Random(s)
            snaps = train(corpus(objs, leak, rng), rng, checkpoints)
            for c in checkpoints:
                res[c].append(probe(snaps[c], objs))
        for c in checkpoints:
            xs = [r[0] for r in res[c]]; ws = [r[1] for r in res[c]]
            m = sum(xs) / len(xs); sd = math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))
            mw = sum(ws) / len(ws)
            print(f"{leak:4.2f}  {c:5d}  {m:.3f} ± {sd:.3f}        {mw:.3f}")
            rows.append((leak, c, m, sd, mw))
        sys.stdout.flush()
    return rows

if __name__ == "__main__":
    main()
