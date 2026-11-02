# COMPLEXITY_DELINEATION -- a tool: which requirements address a hazard, and which do not

Co-authored, 2026-10-31 / 2026-11-01. CC0. Markdown only.
Tags: OBSERVED / DERIVED / PROPOSED / [stated] / VERIFY / OWED.

## Per rule or requirement, ask (PROPOSED tool)

```text
Q1  physical hazard addressed?         name it, or "none"
Q2  who bears the hazard?              occupant / neighbour / responder / installer / nobody
Q3  disclosure vs standardization      could DISCLOSING the condition give the same safety as
                                       STANDARDIZING it away?
Q4  cost, and who can absorb it        moat check: does the cost fall harder on small actors?
Q5  first-principles purpose           does it reduce to a hazard, or does it serve a department,
                                       liability position or status?
```

## Responder view ([stated], volunteer firefighter)

- [stated]  What responders need is foreknowledge of a site, not standardization of every site.

Precedents for disclosure-based safety (VERIFY each):

- VERIFY  NFPA 704 hazard diamond (on-site hazard disclosure)
- VERIFY  NFPA 1620 pre-incident planning
- VERIFY  Knox boxes (responder access without forced entry)
- VERIFY  U.S. DOT hazmat placards
- VERIFY  PV rapid shutdown, NEC 690.12 (introduced 2014 edition; module-level requirement in
  later editions -- check which)

## Coupled degradation loop (PROPOSED)

```text
standardize structures -> responders lose skill with older structures -> older structures read as
more dangerous -> pressure to standardize those too -> loop
```

- VERIFY  UL fire-dynamics work reported flashover in a modern furnished room in about 5 minutes
  vs about 29 minutes for a legacy-furnished room (Kerber, UL ~2012)
- PROPOSED  remedy: train across regimes (old and new construction) + require site disclosure

## Worked application: residential / farm wind + solar (PROPOSED; requirements to be listed from
the adopted codes, VERIFY editions)

```text
requirement (example)           Q1 hazard          Q2 bears          Q3 disclosure-substitutable?
rapid shutdown (PV)             shock to responder responder          partly: labelled disconnect
                                                                      + site plan (VERIFY)
working clearance               arc / shock        installer, owner   no: physical space
labelling / placards            confusion          responder          is itself disclosure
specific listed-equipment only  varies             installer, owner   often yes (moat check)
interconnection paperwork       none direct        utility            interface/compliance, not hazard
```

## Measure / Test

```text
M1  tag every requirement in one adopted code section with Q1-Q5; count hazard-based vs
    interface/compliance
M2  for disclosure-substitutable requirements, compare incident data where disclosure
    alternatives exist (pre-plans, placards) vs where they do not
M3  responder survey: what information was missing at incidents involving the structure type
```

## Open gaps

1. OWED  No code section has been tagged yet.
2. OWED  Flashover figures and NEC editions unverified.
3. OWED  No incident dataset joined to requirement type.
