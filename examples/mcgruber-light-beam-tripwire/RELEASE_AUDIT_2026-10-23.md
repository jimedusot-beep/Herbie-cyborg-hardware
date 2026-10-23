# Cross-repository release audit — McGruber light-beam tripwire
Audited **2026-10-23** against the linked main branches, GitHub Actions runs and known concept assets.

## Verdict

**Interactive digital concept: software-verified. Physical build: NOT verified. McGruber Lab deployment: requires owner configuration.**

| Severity | Finding | Evidence | Resolution / remaining work |
| --- | --- | --- | --- |
| P0 deployment | McGruber Lab public website unavailable: GitHub Pages site missing and integration cannot create it | [Main build/deployment run #39996218874](https://github.com/jimedusot-beep/project-mcgruber/actions/runs/39996218874): Python, Node, Vite, desktop/iPhone tests pass; deploy fails `Not Found / Resource not accessible by integration` | [McGruber deployment fix PR #20](https://github.com/jimedusot-beep/project-mcgruber/pull/20) reports exact error and keeps preview artifact. Owner must set **Settings → Pages → Source → GitHub Actions**, then rerun workflow. This cannot be completed with repository file-write permissions alone |
| P1 misleading viewer label | 3D Vision viewport previously called the tripwire `H.E.R.B.I.E. V1` because the stage badge was static | Main `3D-vision/index.html`, `src/main.js` | [3D Vision context fix PR #6](https://github.com/jimedusot-beep/3D-vision/pull/6) labels `TW-*` as **ILLUSTRATIVE · NOT MEASURED**, and checks Chromium/WebKit |
| P1 reproduce 3D assets | Original Cyborg STL/OBJ snapshot had tests but no saved regeneration/check script | [13-part concept manifest](assembly_manifest.json), [models](models/) | Added [`regenerate_models.py`](regenerate_models.py) with a non-mutating `--check` command plus explicit `--write` rebuild path; CI checks 13 parts, per-part explode offsets and 1,044 triangle facets against the stored meshes |
| P1 hardware design | No exact donor LED, LDR/phototransistor, sensor divider voltage, controller board revision, wiring pinout or fitted mount | [Unverified manifest](assembly_manifest.json) and [blank measurement CSV](measurement_intake_template.csv) | **Still open:** measure real parts, verify current limit / ADC voltage, bench-test receiver, record evidence before saying electrically or mechanically validated |
| P2 partial assembly representation | The 3D scene shows **13 conceptual component groups**, not every cable, fastener, terminal, resistor lead, phone or software prerequisite | [Assembly drawing](diagrams/exploded-assembly.svg) and [manifest](assembly_manifest.json) | Use the [complete build workbook](BENCH_TO_CAD.md) and McGruber's BOM for actual acquisition planning; never treat 13 meshes as the entire shopping list |
| P2 source synchronization | Three repositories have linked but intentionally separate source assets | Cyborg `assembly_manifest.json` source blob IDs; [3D Vision Experiment 002](https://github.com/jimedusot-beep/3D-vision/tree/main/EXPERIMENTS/002_MCGRUBER_TRIPWIRE); [McGruber P01](https://github.com/jimedusot-beep/project-mcgruber/tree/main/projects/01-light-beam-tripwire) | Cyborg is a reviewed snapshot, **not automatic sync**; check original blob SHA and deliberately update/migrate whenever the McGruber manifest changes |
| P2 browser audio/connectivity | Light crossing is simulated in the digital viewers; no phone notification from actual ESP32 has been observed | [Digital handoff](https://github.com/jimedusot-beep/project-mcgruber/blob/main/projects/01-light-beam-tripwire/THREE_D_HANDOFF.md) | Add firmware, physical ADC tests, disconnected state, threshold calibration, phone browser sound-enable interaction, and repeated tests before live-alert claim |

## What has passed

- **3D Vision:** [GitHub Pages publication run #40001092037](https://github.com/jimedusot-beep/3D-vision/actions/runs/40001092037) and [public Chromium/WebKit run #40001313432](https://github.com/jimedusot-beep/3D-vision/actions/runs/40001313432) succeeded with the one-click **13-part exploded/assembled** model URLs.
- **Cyborg Hardware:** [main hardware-check run #40001170653](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/actions/runs/40001170653) passed; test success is a document/mesh integrity result, not a physical build.
- **McGruber Lab:** [main run #39996218874](https://github.com/jimedusot-beep/project-mcgruber/actions/runs/39996218874) passed the application validation job; deployment job failed because Pages is not configured.
- Physical photographs, component ownership, electrically checked sensor/LED supply, enclosure fit and repeatable beam performance **have not been established**.

## Directly inspect the assembly now

[Open exploded model — live 3D Vision](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-exploded) · [Open assembled model](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-assembled) · [Open GitHub STL preview](models/exploded.stl)

The 3D Vision website's dedicated digital model links are the *working deployed path*. They are separate from McGruber Lab's yet-to-be-enabled Pages site. The Cyborg directory holds raw models and engineering documentation but does **not** host a second interactive app.

## Before anyone buys or solders

**Required for one Wi-Fi phone-alert optical tripwire** (not necessarily separately purchased):
- Low-brightness visible emitter (ready-made battery flashlight **or** properly current-limited bare LED), suitable batteries and holder.
- One identified light detector (bare LDR / phototransistor with a compatible bias circuit **or** complete rated sensor module).
- Wi-Fi-capable ESP32 development board, compatible USB power/data cable and USB supply.
- Appropriate wires and a reliable electrical assembly method (breadboard for the first prototype; soldered wiring only after testing), mounting support for both sides.
- Computer to flash firmware, phone for local Wi-Fi status, and actual tested ESP32 software with calibration and communication-failure handling.
- Suitable resistors are **conditional** on the chosen emitter and sensor modules; a bare LED needs current limiting, and a bare LDR needs a divider. Exact values depend on part identification.

**Optional:** emitter switch (if not in flashlight), black receiver-shading tube, enclosure, physical buzzer/driver, status LED/limiter, additional beam/sensor, timer/scoring.

**Not required:** laser emitter, extra Arduino in addition to ESP32, separate Wi-Fi transmitter module, native iPhone app, mains-powered donor electronics.

A real optical alarm needs careful ambient-light rejection. Ordinary LEDs do not produce cinema-style visible shafts in clear air, so game decoration should not be mistaken for a continuous visible laser beam. Keep illumination well below eye level and never use hazardous IR or lasers for this supervised child-friendly prototype.

## Evidence and finishing gates

1. Use [blank identification/measurement intake](measurement_intake_template.csv) and photo evidence kept private. Do not invent dimensions or acquisition records.
2. Identify controller revision/pinout and verify LED/sensor electrical design against datasheets.
3. Demonstrate beam-present/beam-blocked sensor voltages with a multimeter, including ambient light changes.
4. Demonstrate actual ESP32 ADC readings and real Wi-Fi statuses on a phone, including disconnection and browser sound activation.
5. Create dimensioned replacement CAD for real parts, dry-fit, and record clearances before suggesting 3D printing.
6. Only describe a build as working once repeated real crossing tests and logs confirm it.

## Maintaining the models

From the repository root, execute:

```bash
python3 examples/mcgruber-light-beam-tripwire/regenerate_models.py --check
# Only after intentionally changing the unmeasured model or explosion offsets:
python3 examples/mcgruber-light-beam-tripwire/regenerate_models.py --write
python3 examples/mcgruber-light-beam-tripwire/regenerate_models.py --check
```

The source `models/assembled.obj` is still a generic illustrative mesh, not a measured component model. The command rebuilds derived files from that mesh and the 13-part manifest, not a validated printed object. Run geometry tests and review repository diffs before committing any regenerated assets.

[Return to case study](README.md) · [Build guide](BENCH_TO_CAD.md) · [Cyborg home](../../README.md)
