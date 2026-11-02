# Name sweep 2026-11-02

One personal name (written `<name>` below) was removed from file contents. Git history was not rewritten,
so past commit messages and past file versions still carry it. Commit messages from now
on carry no name.

## Rule applied

```text
"Co-authored (<name> + Claude)" and similar headers  -> "Co-authored" (the date is kept)
"[stated] (<name>)"                                   -> "[stated]"
"OBSERVED by <name>", "OBSERVED (<name>)"              -> "OBSERVED (field report)"
any other attribution                                -> name dropped, status tag kept
"<name>'s method/frame/tool"                          -> "the method / a working tool"
```

Only the name changed on each line. Vendored and upstream third-party files were not touched.

## Files changed (replacements)

```text
gap-registers/COMPLEXITY_DELINEATION.md                        2
gap-registers/CULTURE_PHYSICS_ANCHOR.md                        6
gap-registers/DIGITAL_VS_PHYSICAL_CLOCK_2026.md                3
gap-registers/FLOAT_SKILL.md                                   6
gap-registers/README.md                                        2
gap-registers/RESONANCE_SPHERE_EVENT_LOG.md                    3
gap-registers/SUPERCONDUCTOR_PATCHWORK_GAPS.md                 2
gap-registers/TRUST_WEB_DENSITY.md                             3
gap-registers/WORKFORCE_EXTRACTION_CHAIN.md                    3
```

9 files, 30 replacements.

## Left in place, for the owner's call

These are identity or rights records, not attributions. Removing the name from them would
change what the line records, so they are listed here instead of edited:

None. Every hit was swept.

## Where removing the name changed meaning

```text
gap-registers/SUPERCONDUCTOR_PATCHWORK_GAPS.md   "([stated] <name>'s priority)" -> "([stated] priority)": whose priority is no longer stated
gap-registers/README.md         "`[stated]` = <name> said it directly" -> "said directly by the human co-author":
                                the tag's definition now names a role, not a person
gap-registers/COMPLEXITY_DELINEATION.md   "([stated] <name>, volunteer firefighter)" -> "([stated], volunteer firefighter)":
                                the source is now described only by role
```

## Test results

The suites were run before and after the sweep, and the counts below match. See the
commit message for the exact commands.
