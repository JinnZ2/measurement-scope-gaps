# DIGITAL_VS_PHYSICAL_CLOCK_2026 -- design moves on a fast clock, the physical chain on an old one

Co-authored (Kavik + Claude), 2026-10-31 / 2026-11-01. CC0. Markdown only.
Tags: OBSERVED / DERIVED / PROPOSED / [stated] / VERIFY / OWED.
Every figure below is from secondary sources and is VERIFY against the primary source named.

## Gap

- [stated] (Kavik) Time offset: design and office work compressed to months; the physical chain
  (equipment, grid, trades) still runs on the old clock.
- DERIVED   In theory-of-constraints terms (Goldratt), throughput is set by the slowest link; a
  faster design clock only grows the queue in front of the physical constraint.

## Figures (VERIFY each against the source named)

```text
data-center pipeline   ~12 GW announced; ~1/3 under construction; ~half delayed or
                       canceled                                         (Bloomberg; Sightline Climate)
transformers           3-5 year lead times, up from ~2 years pre-2020   (industry reports)
grid interconnection   4-10 year waits; ~2,600 GW queued end of 2023    (LBNL "Queued Up")
cost                   ~$11.3M/MW in 2026 vs ~$7.7M/MW in 2020          (JLL)
construction labor     92% of contractors report hiring difficulty;
                       45% report project delays from it               (AGC 2025 survey)
                       ~439k data-center construction worker shortfall  (ITIF, Jan 2026)
cost share             electrical work 45-70% of build cost             (ABC, July 2026)
backlog                data-center contractors ~11.4 months vs 7.5 for
                       others                                           (ABC, July 2026)
megaprojects           ~9 in 10 large infrastructure projects run over
                       schedule                                         (Flyvbjerg, Oxford megaprojects)
```

Note 2026-11-02: attributions corrected against the source notes. Earlier version credited the
439k shortfall to ABC (source: ITIF), the pipeline line to JLL (source: Bloomberg / Sightline
Climate), and left the cost (JLL) and electrical share (ABC) unsourced. Figures unchanged; all
still VERIFY against the primary reports.

## Open: electrical trades knowledge discrepancy ([stated] Kavik)

- PROPOSED  The knowledge an electrician must hold has grown faster than the training time that
  produces it.

## Measure / Test

```text
M1  DOL apprenticeship data: completion and retention rates for electrical, by year
M2  hours to journeyman, by state and year
M3  entrant hands-on exposure before apprenticeship (survey)
M4  NEC page count by edition vs required training hours over the same editions
test  does required content (M4) outgrow training time (M2), and does completion (M1) fall
      where the gap is widest?
```

## Open gaps

1. OWED  None of the figures above has been checked against its primary source here.
2. OWED  The cost and electrical-share figures need a named primary source.
3. OWED  No measure links the design-clock speed to queue growth at the physical constraint.
