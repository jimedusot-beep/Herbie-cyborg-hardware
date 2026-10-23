# H.E.R.B.I.E. — Cyborg Hardware

Electronics and physical integration engineering. **This repository is preliminary; no physical electrical or motion testing is demonstrated.**

- [Brain — Herbie](https://github.com/jimedusot-beep/Herbie)
- [Body — 3D-vision](https://github.com/jimedusot-beep/3D-vision)
- **Electronics — this repository**

Electrical schematics, power, wiring, BOM and integration will be documented here. Do not energize components based on unverified plans.

## McGruber tripwire — exploded assembly and 3D learning case

**[OPEN THE TRIPWIRE EXPLODED ASSEMBLY](examples/mcgruber-light-beam-tripwire/README.md)** · [**One-click 3D Vision exploded model**](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-exploded) · [Part measurement workbook](examples/mcgruber-light-beam-tripwire/measurement_intake_template.csv) · [Bench-to-CAD guide](examples/mcgruber-light-beam-tripwire/BENCH_TO_CAD.md) · [View labeled diagram](examples/mcgruber-light-beam-tripwire/diagrams/exploded-assembly.svg) · [Rotate exploded 3D STL](examples/mcgruber-light-beam-tripwire/models/exploded.stl) · [Download editable separate-part OBJ](examples/mcgruber-light-beam-tripwire/models/exploded.obj) · [Open 3D Vision](https://jimedusot-beep.github.io/3D-vision/)

A **13-component, conceptual** emitter → sensor → ESP32 → phone tripwire assembly is mirrored here as a standalone electronics and CAD learning example.

**[Verified cross-repository audit and outstanding blockers](examples/mcgruber-light-beam-tripwire/RELEASE_AUDIT_2026-10-23.md)** · [Reproduce/check illustrative meshes](examples/mcgruber-light-beam-tripwire/regenerate_models.py) Both assembled and exploded STL/OBJ meshes are included, with component IDs, a measurement-gap manifest and provenance tracing back to [Project McGruber](https://github.com/jimedusot-beep/project-mcgruber).

This is **not** part of the H.E.R.B.I.E. V1 robot, BOM, motion architecture or validated CAD. Source geometry is approximate and unmeasured; real component voltage ratings, mechanical fit, functionality and testing are still unknown.


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

## Phase 2 — Datasheet-backed candidate evaluation

- [Manufacturer comparison](docs/PHASE2_COMPONENT_RESEARCH.md)
- [Research candidates JSON](bom/researched_candidates.json) — candidates only; no confirmed ownership or compatibility
- [Candidate catalog tests](tests/test_researched_candidates.py)

Actual component selections, servo fit, power budget and physical safety are **unverified**. Research does not authorize physical actuation.

## Inventory evidence and procurement truth

- [Acquisition evidence policy](docs/INVENTORY_EVIDENCE_POLICY.md) — defines when a component may be called owned, donated or requested
- [Public-safe evidence ledger](bom/acquisition_evidence.csv) — currently empty; no acquisition claims made
- [Evidence validation tests](tests/test_acquisition_evidence.py) — reject unsupported acquisition statuses and model mismatches

The existing four BOM entries remain planned and unverified. Never commit private addresses, tracking numbers, receipts or serial numbers.

## CAD/electronics integration — review required

- [Provisional component-to-CAD mapping](integration/cad-electronics-compatibility.json)
- [Compatibility and measurement guide](integration/CAD_COMPATIBILITY_GUIDE.md)
- [Mapping consistency tests](tests/test_cad_compatibility.py)

The existing fixed-neck concept is **not** a verified two-axis servo mount. Physical fit and electrical safety remain unverified.
