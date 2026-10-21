# H.E.R.B.I.E. — Cyborg Hardware

Electronics and physical integration engineering. **This repository is preliminary; no physical electrical or motion testing is demonstrated.**

- [Brain — Herbie](https://github.com/jimedusot-beep/Herbie)
- [Body — 3D-vision](https://github.com/jimedusot-beep/3D-vision)
- **Electronics — this repository**

Electrical schematics, power, wiring, BOM and integration will be documented here. Do not energize components based on unverified plans.

## Start here: learn and research

- [Beginner guide](docs/BEGINNER_GUIDE.md) — a safe simulation-first learning path
- [Numbered robotics research library (1–24)](docs/RESEARCH_LIBRARY.md) — portals and 12 project references, with verification and licensing cautions
- [Machine-readable research list (13–24)](docs/RESEARCH_PROJECTS_13_24.csv) — searchable reference index, not a component list
- [Research-source verification notes](docs/RESEARCH_VERIFICATION_2026-10-21.md) — access limits, licenses and corrections
- [Part intake guide](bom/INTAKE_GUIDE.md) — use the existing acquisition-evidence ledger; do not invent owned parts
- [Controller architecture comparison](controllers/ARCHITECTURE_OPTIONS.md) — Pi, driver and ESP32 options; no choice made
- [Proposed safety requirements](integration/SAFETY_REQUIREMENTS_V0.md) — review-only, not implemented
- [Research evaluation template](docs/RESEARCH_EVALUATION_TEMPLATE.md) — review evidence before adopting external ideas
- [Community engineering references](docs/COMMUNITY_RESEARCH.md) and [open-source design review](docs/OPEN_SOURCE_DESIGN_REVIEW.md)

## Engineering references and build gates

- [Preliminary electronics block diagram](schematics/CONCEPTUAL_BLOCK_DIAGRAM.md) — not a wiring schematic
- [Electrical power budget worksheet](power/POWER_BUDGET_TEMPLATE.csv) and [screening calculator](tools/power_budget.py) — blank values mean unknown, not zero
- [Build readiness checklist](integration/BUILD_READINESS_CHECKLIST.md) — evidence gates before physical motion
- [Versioned integration manifest](integration/system-manifest.json) — cross-repository component IDs; actuation disabled
- [Motion protocol incompatibility audit](docs/MOTION_PROTOCOL_COMPARISON.md) — simulated formats need reconciliation
- [Targeted engineering audit](docs/AUDIT_2026-10-21.md) — verified findings, open questions and CI caveats
- [Community design feedback issue](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/issues/2) — datasheet-backed suggestions welcome
- [Automated quality workflow](.github/workflows/hardware-quality.yml) — inventory, manifest, worksheet and unit checks

**Foundation PR [#1](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/pull/1) was merged on 2026-10-21.** That was a documentation/software-quality milestone, **not** a successful physical prototype. Exact parts, KiCad schematics, independently assessed motor-power interruption and supervised bench tests remain pending. **Do not enable motion from these materials.**
