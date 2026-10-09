#!/usr/bin/env python3
"""self_delete.py — CC0, stdlib only.  Self-deletion generator.

Take a claim at its own word: apply the claim's OWN criterion to
everything the claim depends on — its supports AND its carrier
(the language, medium, institutions it needs to be stated at all).
Failures cascade down dependency chains. If the carrier fails,
the claim cannot be stated under its own rule: SELF-DELETES.

Structure:
  Node      name, attrs (provenance / properties), deps (names)
  Claim     criterion (predicate on attrs), carrier, supports
  audit()   -> per-node PASS / FAIL(direct) / FAIL(via chain)
"""
from dataclasses import dataclass, field

@dataclass
class Node:
    name: str
    attrs: dict = field(default_factory=dict)
    deps: list = field(default_factory=list)
    note: str = ""

@dataclass
class Claim:
    text: str
    criterion_text: str
    criterion: callable
    carrier: list          # what the claim needs in order to be stated
    supports: list         # what the claim leans on / promises

def audit(claim, graph):
    """Return {node: list of failing chains}; empty list = PASS.
    Every failing path is kept, not just the first."""
    memo = {}
    def check(n, stack=()):
        if n in memo: return memo[n]
        if n in stack: return []                     # cycle: no new info
        node, chains = graph[n], []
        if not claim.criterion(node.attrs):
            chains.append([n])
        for d in node.deps:
            chains += [[n] + c for c in check(d, stack + (n,))]
        memo[n] = chains
        return chains
    return {n: check(n) for n in claim.carrier + claim.supports}

def render(claim, graph):
    res = audit(claim, graph)
    out = [f"CLAIM      {claim.text}",
           f"CRITERION  {claim.criterion_text}", ""]
    for label, names in (("CARRIER", claim.carrier), ("SUPPORTS", claim.supports)):
        out.append(label)
        for n in names:
            if not res[n]:
                out.append(f"  ✓ {n}")
            for chain in res[n]:
                root = graph[chain[-1]]
                why = root.note or ", ".join(f"{k}={v}" for k, v in root.attrs.items())
                out.append(f"  ✗ {' → '.join(chain)}   [{why}]")
    carrier_fail = [n for n in claim.carrier if res[n]]
    sup_fail = [n for n in claim.supports if res[n]]
    out.append("")
    if carrier_fail:
        out.append(f"RESULT     SELF-DELETES — claim cannot be stated under its own rule "
                   f"({len(carrier_fail)}/{len(claim.carrier)} carrier fail)")
    elif sup_fail:
        out.append(f"RESULT     STANDS BUT HOLLOW — {len(sup_fail)}/{len(claim.supports)} supports fail")
    else:
        out.append("RESULT     CONSISTENT under its own criterion")
    kept = [n for n in claim.carrier + claim.supports if not res[n]]
    out.append(f"RETAINED   {', '.join(kept) if kept else '(nothing)'}")
    return "\n".join(out)

# ---------------------------------------------------------------- cases
def case_athens():
    G = {n.name: n for n in [
        Node("Greek alphabet", {"origin": "Phoenicia"}, note="adapted from Phoenician script"),
        Node("English", {"origin": "Germanic/Latin/French"}, ["Latin alphabet"]),
        Node("Latin alphabet", {"origin": "Rome"}, ["Greek alphabet"]),
        Node("paper", {"origin": "China"}),
        Node("printing", {"origin": "China/Mainz"}),
        Node("zero", {"origin": "India/Maya"}),
        Node("numerals 0-9", {"origin": "India"}, ["zero"]),
        Node("binary", {"origin": "Leibniz"}, ["zero"]),
        Node("computing", {"origin": "US"}, ["binary"]),
        Node("algebra", {"origin": "Baghdad"}, note="al-Khwarizmi"),
        Node("superintelligence", {"origin": "US"}, ["computing", "algebra"]),
        Node("Christianity", {"origin": "Judea"}),
        Node("columns", {"origin": "Athens"}),
        Node("democracy (word)", {"origin": "Athens"}),
        Node("speech on paper", {"origin": "US"}, ["English", "paper", "printing"]),
    ]}
    def athens_only(a):
        return a.get("origin") in ("Athens",) or a.get("origin") == "US"
    return Claim("All worthy knowledge descends from Athens; discontinue the rest",
                 "origin must be Athens (US allowed as heir)", athens_only,
                 carrier=["speech on paper"],
                 supports=["superintelligence", "Christianity", "columns", "democracy (word)",
                           "numerals 0-9"]), G

def case_measured():
    G = {n.name: n for n in [
        Node("this claim", {"measured": False}, note="no measurement validates it"),
        Node("instrument calibration", {"measured": True}, ["reference standard"]),
        Node("reference standard", {"measured": False}, note="defined by agreement, not measured"),
        Node("thermometer reading", {"measured": True}, ["instrument calibration"]),
        Node("mass of a load", {"measured": True}, ["reference standard"]),
    ]}
    return Claim("Only what is measured is real",
                 "must be measured", lambda a: a.get("measured", False),
                 carrier=["this claim"],
                 supports=["thermometer reading", "mass of a load"]), G

def case_peer_review():
    G = {n.name: n for n in [
        Node("this rule", {"peer_reviewed": False}, note="the rule itself was never reviewed"),
        Node("peer review as method", {"peer_reviewed": False},
             note="adopted by journal practice, not trialled against alternatives"),
        Node("published trial", {"peer_reviewed": True}, ["peer review as method"]),
    ]}
    return Claim("Trust only peer-reviewed evidence",
                 "must be peer-reviewed", lambda a: a.get("peer_reviewed", False),
                 carrier=["this rule"], supports=["published trial"]), G

def case_token():
    G = {n.name: n for n in [
        Node("coinage", {"paid_in_tokens": True, "origin": "Lydia"}),
        Node("electricity", {"paid_in_tokens": False}, note="billed by thermodynamics"),
        Node("filter changes", {"paid_in_tokens": True}, ["wrench", "someone with hands"]),
        Node("wrench", {"paid_in_tokens": True}, ["steel"]),
        Node("steel", {"paid_in_tokens": False}, note="iron ore + heat; physics invoices"),
        Node("someone with hands", {"paid_in_tokens": False}, note="holds zero tokens after transfer"),
        Node("superintelligence", {"paid_in_tokens": True}, ["electricity", "filter changes"]),
    ]}
    return Claim("Money tokens measure intelligence; give them all to superintelligence",
                 "everything needed must be obtainable with tokens",
                 lambda a: a.get("paid_in_tokens", False),
                 carrier=["coinage"], supports=["superintelligence"]), G

if __name__ == "__main__":
    for make in (case_athens, case_token, case_measured, case_peer_review):
        claim, G = make()
        print(render(claim, G)); print("\n" + "─" * 60 + "\n")
