#!/usr/bin/env python3
"""real_probe.py — Branch D. Septic vs hydro in a public embedding
(spaCy en_core_web_md, 300-d, 20k vectors). Read-only probe, no training.
M1 set distance: septic×hydro vs each against a control domain (tax).
M2 hub score:   h -> min(cos(h,centroid_S), cos(h,centroid_H)),
                ranked against all 20k vocabulary vectors (percentile).
                Shared physics variables high = center node present.
"""
import numpy as np
import load_vecs as lv

SEPTIC = "septic sewage wastewater effluent cesspool sewer sludge latrine leach".split()
HYDRO  = "turbine hydroelectric dam reservoir penstock spillway hydropower megawatt".split()
TAX    = "tax deduction audit taxable refund invoice payroll deductible".split()
HUBS   = ("head pressure gradient flow gravity sediment percolation permeability "
          "viscosity discharge velocity hydraulic siltation pipe valve pump "
          "drainage aquifer groundwater infiltration erosion biofilm").split()

def main():
    V, k2r = lv.load()
    def get(ws):
        out = {w: lv.vec(w, V, k2r) for w in ws}
        miss = [w for w, v in out.items() if v is None]
        return {w: v / np.linalg.norm(v) for w, v in out.items() if v is not None}, miss
    S, mS = get(SEPTIC); H, mH = get(HYDRO); T, mT = get(TAX); B, mB = get(HUBS)
    print("missing:", mS + mH + mT + mB)
    def setcos(a, b):
        return float(np.mean([x @ y for x in a.values() for y in b.values()]))
    within = lambda a: float(np.mean([x @ y for i, x in enumerate(a.values())
                                       for j, y in enumerate(a.values()) if i < j]))
    print("\nM1 set mean cosine")
    for n, a, b in (("septic×hydro", S, H), ("septic×tax", S, T), ("hydro×tax", H, T)):
        print(f"  {n:13s} {setcos(a, b):+.3f}")
    print(f"  within septic {within(S):+.3f} · within hydro {within(H):+.3f}")

    cS = np.mean(list(S.values()), 0); cS /= np.linalg.norm(cS)
    cH = np.mean(list(H.values()), 0); cH /= np.linalg.norm(cH)
    Vn = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)
    allscore = np.minimum(Vn @ cS, Vn @ cH)
    print(f"\n  centroid cos(S,H) {cS @ cH:+.3f}")
    print("\nM2 hub score = min(cos to septic centroid, cos to hydro centroid)")
    print("  term          toS     toH     hub    pct_of_20k")
    rows = []
    for w, v in B.items():
        s, h = float(v @ cS), float(v @ cH); m = min(s, h)
        rows.append((m, w, s, h, float((allscore < m).mean() * 100)))
    for m, w, s, h, p in sorted(rows, reverse=True):
        print(f"  {w:12s} {s:+.3f}  {h:+.3f}  {m:+.3f}  {p:6.2f}")
    print(f"\n  vocab hub score: median {np.median(allscore):+.3f} · 99th pct {np.percentile(allscore, 99):+.3f}")

if __name__ == "__main__":
    main()
