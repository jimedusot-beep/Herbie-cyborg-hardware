# H.E.R.B.I.E. — Cyborg Hardware

Electronics and physical integration engineering. This repository is preliminary and not physically tested.

- [Brain — Herbie](https://github.com/jimedusot-beep/Herbie)
- [Body — 3D-vision](https://github.com/jimedusot-beep/3D-vision)
- **Electronics — this repository**

Electrical schematics, power, wiring, BOM and integration will be documented here. Do not energize components based on unverified plans.

## Engineering references and build gates

- [Preliminary electronics block diagram](schematics/CONCEPTUAL_BLOCK_DIAGRAM.md) — not a wiring schematic
- [Electrical power budget worksheet](power/POWER_BUDGET_TEMPLATE.csv) and [screening calculator](tools/power_budget.py) — blank values mean unknown, not zero
- [Build readiness checklist](integration/BUILD_READINESS_CHECKLIST.md) — evidence gates before physical motion
- [Versioned integration manifest](integration/system-manifest.json) — cross-repository component IDs; actuation disabled
- [Motion protocol incompatibility audit](docs/MOTION_PROTOCOL_COMPARISON.md) — two existing simulated command formats need reconciliation
- [Targeted engineering audit](docs/AUDIT_2026-10-21.md) — verified findings, open questions and CI caveats
- [STEAM learning path](docs/STEAM_LEARNING_PATH.md) — science, technology, engineering, art and math mini-lessons
- [Open-source research review](docs/OPEN_SOURCE_DESIGN_REVIEW.md) — design patterns, not copied circuits
- [Community design feedback issue](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/issues/2) — datasheet-backed suggestions welcome
- [Automated quality workflow](.github/workflows/hardware-quality.yml) — BOM, manifest, worksheet and unit checks

**Hardware PR #1 is a draft.** Actual component selection, KiCad schematics, physical E-stop, and bench tests remain pending.

## Phase 2 — Manufacturer-backed component research

- [Compare controller and servo architectures](docs/PHASE2_COMPONENT_RESEARCH.md)
- [Machine-readable research candidates](bom/researched_candidates.json) — **not** an ownership inventory or a confirmed BOM selection
- [Catalog verification tests](tests/test_researched_candidates.py) — checks citations, required fields and protocol distinctions

Do not select motor voltage or wiring from candidate research alone. Physical motion stays disabled.
