#!/usr/bin/env python3
"""real_readings.py — pilot: reading disagreement on a real embedding.
spaCy en_core_web_md vectors (20k rows). No co-occurrence matrix here, so
readings are those available on static vectors:
  R1 cosine   R2 mean-centered cosine   R3 neg euclidean
  R4 shared-neighbor overlap (Jaccard of top-50 neighbors) — the hub reading
COUPLED pairs: cross-discipline, same governing physics (hand-labelled).
UNCOUPLED: all cross-pairings of the same words that do not share it.
"""
import itertools
import numpy as np
import load_vecs as lv
import cut_recover as cr

COUPLED = [  # (a, b, shared variable)
    ("artery", "pipeline", "pressure-driven flow"),
    ("lung", "bellows", "pressure–volume pumping"),
    ("glacier", "lava", "viscous creep"),
    ("septic", "turbine", "hydraulic head"),
    ("rumor", "epidemic", "contagion spread"),
    ("fever", "thermostat", "setpoint control"),
    ("soil", "sponge", "porous wicking"),
    ("pendulum", "heartbeat", "oscillation"),
    ("traffic", "plumbing", "flow under congestion"),
    ("forest", "battery", "stored energy, discharge"),
]

def main():
    V, k2r = lv.load()
    Vn = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)
    mu = V.mean(0)
    def row(w):
        r = k2r.get(lv.mm64a(w.encode())); return r
    words = sorted({w for a, b, _ in COUPLED for w in (a, b)})
    rows = {w: row(w) for w in words}
    miss = [w for w, r in rows.items() if r is None]
    shared_rows = {}
    for w, r in rows.items(): shared_rows.setdefault(r, []).append(w)
    print("missing:", miss, "| merged rows:", [v for v in shared_rows.values() if len(v) > 1])
    nbr = {w: set(np.argsort(-(Vn @ Vn[r]))[1:51]) for w, r in rows.items() if r is not None}
    def readings(a, b):
        x, y = V[rows[a]], V[rows[b]]
        xc, yc = x - mu, y - mu
        return [float(Vn[rows[a]] @ Vn[rows[b]]),
                float(xc @ yc / (np.linalg.norm(xc) * np.linalg.norm(yc))),
                -float(np.linalg.norm(x - y)),
                len(nbr[a] & nbr[b]) / len(nbr[a] | nbr[b])]
    A = [a for a, _, _ in COUPLED]; B = [b for _, b, _ in COUPLED]
    cpl = {(a, b) for a, b, _ in COUPLED}
    pairs = list(itertools.product(A, B))
    R = np.array([readings(a, b) for a, b in pairs])
    lab = np.array([p in cpl for p in pairs])
    Z = (R - R.mean(0)) / (R.std(0) + 1e-12)
    au = lambda s: cr.auc(list(s[lab]), list(s[~lab]))
    names = ["cosine", "centered", "neg-euclid", "nbr-overlap"]
    print(f"\npairs: {lab.sum()} coupled vs {(~lab).sum()} uncoupled\n")
    for i, n in enumerate(names): print(f"  {n:12s} AUC {au(R[:, i]):.2f}")
    print(f"  {'DISAGREE':12s} AUC {au(Z.std(1)):.2f}")
    print(f"  {'MAXABS':12s} AUC {au(np.abs(Z).max(1)):.2f}")
    print("\nper coupled pair (z: cos, centered, euclid, nbr | disagree):")
    for (a, b, v) in COUPLED:
        z = Z[pairs.index((a, b))]
        print(f"  {a:9s}–{b:10s} " + " ".join(f"{t:+.1f}" for t in z) + f" | {z.std():.2f}   [{v}]")

if __name__ == "__main__":
    main()
