# McGruber light-beam tripwire — exploded assembly in Cyborg Hardware

**Status: `DIGITAL_CONCEPT_UNTESTED` · educational side project · not a H.E.R.B.I.E. robot component.**

This case study puts the **light-beam tripwire's diagrams and explorable 3D models directly inside H.E.R.B.I.E. Cyborg Hardware**, so you can inspect the physical arrangement alongside controller, wiring, and hardware-integration research. The original design and live editable viewer code remain under [Project McGruber](https://github.com/jimedusot-beep/project-mcgruber); H.E.R.B.I.E.'s own robot BOM, 18 CAD part identities and integration manifest remain unchanged.

## Engineering audit and regeneration

- [**2026-10-23 three-repository audit**](RELEASE_AUDIT_2026-10-23.md) — confirms what works, what is deployed, what is blocked and what requires real measurements
- [**Rebuild/check the 3D concept files**](regenerate_models.py) — run `python3 examples/mcgruber-light-beam-tripwire/regenerate_models.py --check`; append `--write` only when intentionally regenerating outputs
- [Physical measurement worksheet](measurement_intake_template.csv) and [bench-to-CAD build guide](BENCH_TO_CAD.md) — all observation fields start blank

These files are intentionally **not print-ready**. Passing geometry consistency checks does not measure components, establish an LED or sensor circuit, or turn the tripwire into a tested product.

## Silent standalone tripwires B and C — 3D Vision Experiment 003

**[Open the interactive 3D model gallery](https://jimedusot-beep.github.io/3D-vision/optical-tripwires.html)** · [3D Vision source and builder notes](https://github.com/jimedusot-beep/3D-vision/tree/main/EXPERIMENTS/003_MCGRUBER_SILENT_TRIPWIRES)

### Interactive step-by-step assembly teacher

**[Start Experiment B · Step 1 of 6](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-visible-b-assembled&step=1)** · **[Start Experiment C · Step 1 of 7](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-infrared-c-assembled&step=1)**

The published Three.js viewer now includes an on-screen mobile-friendly **guided build panel** that:
- Highlights the relevant actual 3D part groups for each stage; tap a part name or focus the camera.
- Shows **where to place** the components, a readable from→to wiring/lead connection list, and a Fluke/safety checkpoint before the next physical stage.
- Has **Previous/Next**, collapsible lesson on mobile, and a linkable `&step=N` that survives assembled/exploded and simulated beam changes.
- Tracks only **lessons read** in the browser. It explicitly does **not** store passed circuit tests or certify a working tripwire.

**Critical truthfulness gate:** B's amplifier-to-2N4401 connection remains marked **BLOCKED — DESIGN MISSING**. C's described 5 V/10 kΩ pull-up/1 kΩ warning LED circuit is **Adafruit 2167/2168-specific** and must be confirmed on actual identified hardware before energizing. Neither build is physically measured, print-ready or proven to operate over a doorway.

The original 13-part McGruber concept remains below. There are also two **distinct** standalone, no-audio teaching assemblies in the same 3D Vision workshop:

| Experiment | Rotatable 3D scene | Exploded 3D scene | Evidence boundary |
| --- | --- | --- | --- |
| **B · blue LED → unpowered red sensor → amplifier → 2N4401 → silent red warning LED** | [Open B](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-visible-b-assembled) | [Explode B](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-visible-b-exploded) | 16 conceptual part groups; amplifier and automatic warning **unverified** |
| **C · invisible matched IR transmitter/receiver → current-limited silent red warning LED** | [Open C](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-infrared-c-assembled) | [Explode C](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-infrared-c-exploded) | 15 conceptual groups; Adafruit-style output is visually simulated, **not physically tested** |

The new models have direct **Beam clear / Block beam** links. C makes the **illustrated** red LED glow when the *simulated* IR beam is blocked; it is **not reading a sensor**. B deliberately leaves the missing signal-conditioning interface and the silent warning output unproven. In both cases, wire routing, part dimensions and mounting are approximate, and the glowing line is only a visual guide (ordinary LEDs and invisible infrared do not produce visible light shafts in clear air).

The canonical electronics instructions remain [McGruber P01](https://github.com/jimedusot-beep/project-mcgruber/tree/main/projects/01-light-beam-tripwire) and [McGruber P08](https://github.com/jimedusot-beep/project-mcgruber/tree/main/projects/08-infrared-tripwire). Do not use these instructional meshes as a pin-by-pin wiring diagram or print-ready enclosure.

## Open the exploded view

### 1. Original exploded assembly illustration — opens in GitHub

[![Concept exploded assembly for transmitter, receiver, controller and phone](diagrams/exploded-assembly.svg)](diagrams/exploded-assembly.svg)

[**Enlarge original exploded SVG**](diagrams/exploded-assembly.svg) · [**Electrical signal-flow diagram**](diagrams/signal-flow.svg)

### 2. 3D mesh assembly — inspect without installing software

| View | Open on GitHub | What's shown |
| --- | --- | --- |
| **Exploded 3D model** | [**Open / rotate exploded STL**](models/exploded.stl) | The 13 illustrated component groups spread apart |
| **Assembled 3D model** | [**Open / rotate assembled STL**](models/assembled.stl) | Same generic components placed together |

GitHub normally provides an interactive 3D preview for STL files; browser support and current GitHub UI vary. If GitHub displays a download instead, use the **3D Vision workflow** below. These are genuine triangle meshes, **not measured mechanical parts**.

### 3. Open the assembly directly in the 3D Vision workshop

After the accompanying 3D Vision Experiment 002 update is published, these links open the **actual 13-part mesh assembly without a download or manual import**:

- [**Open exploded tripwire in 3D Vision**](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-exploded)
- [**Open assembled tripwire in 3D Vision**](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-assembled)

The viewer provides orbit, zoom, a part tree, hide/isolate, visual inspection and exporting. It is an educational 3D concept, **not a measured case, functional electrical design, or proof of printing fit**. If the links have not yet been deployed, use the manual OBJ-import steps next.

### 4. Select, hide and inspect individual components through manual import into 3D Vision

1. Download the [**exploded OBJ**](models/exploded.obj) or [**assembled OBJ**](models/assembled.obj) from GitHub (use the file's **Download raw file** option).
2. Open the existing [**3D Vision workshop**](https://jimedusot-beep.github.io/3D-vision/) on your phone or computer.
3. **Import models** and select the downloaded `.obj` file; choose **millimeters** as source units and **Y up** for the source model if the import settings ask.
4. Orbit/zoom, select a component in the tree, hide/isolate it, and use 3D Vision's mesh inspection tools.
5. Save a revision or **Export complete project (.3dv)** if you want a portable backup. Browser imports are not automatically committed to GitHub.

For the more specialized **beam-break simulator and explode slider**, see [McGruber Lab's interactive Three.js implementation](https://github.com/jimedusot-beep/project-mcgruber/blob/main/web/src/tripwire-3d.js). That browser app is a separate project and its web deployment must be available before the `#/tripwire-3d` route can be used publicly.

## What's inside

| File | Role | Source / status |
| --- | --- | --- |
| [Exploded drawing](diagrams/exploded-assembly.svg) | Beginner-friendly, labeled 2D breakdown | Exact McGruber SVG snapshot; conceptual |
| [Signal flow](diagrams/signal-flow.svg) | Light path, sensor, ADC, controller, Wi-Fi and phone | Exact McGruber SVG snapshot; not a validated wiring pinout |
| [Case-study assembly manifest](assembly_manifest.json) | Stable 13-part IDs, salvage ideas, offsets, measurement gaps and copied-source provenance | Machine-readable, provisional |
| [Assembled OBJ](models/assembled.obj) / [Exploded OBJ](models/exploded.obj) | Individually named illustrative 3D parts for 3D Vision | Original, derived from McGruber concept positions |
| [Assembled STL](models/assembled.stl) / [Exploded STL](models/exploded.stl) | GitHub/browser 3D previews | Original approximate triangle meshes; unprinted and not fit-checked |

### What the 13 part groups represent

- **Emitter / transmitter:** mount, optional housing, battery supply, switch, current limiter, and low-brightness visible LED (or reuse a complete battery-operated flashlight).
- **Receiver:** mount, optional light-shield tube, light sensor, suitable sensor bias/divider, and optional housing.
- **Controller:** ESP32-C3 development board and compatible USB supply; its Wi-Fi page would be implemented/programmed separately.

**Light travels from emitter to receiver without a cable between them.** The receiver's sensor electrically connects to the microcontroller, and the controller can communicate over Wi-Fi after real firmware and network setup. The visual crossing-beam status in McGruber is a *simulation*, not connected hardware.

## What still needs real-world measurements

No exact board variant, LED current, sensor threshold, battery voltage, GPIO pin, housing clearance, mechanical fit, or physical testing is established. The component positions, diameters, box sizes and offsets in these OBJ/STL files are **illustrative only**. Do not send these meshes to a printer as ready-to-fit parts.

Before a physical build, identify the actual low-voltage donor parts, check the manufacturer's specifications, measure and document safe input voltages (especially the ESP32's 3.3 V GPIO), choose the proper LED current-limiting components, and test a single beam under varying ambient lighting.

**Safety:** use battery-powered low-voltage parts only; prefer a diffused low-brightness visible LED below eye height. Avoid lasers, high-power invisible IR, mains-powered plug-in lights and damaged rechargeable cells. See [Cyborg beginner safety](../../docs/BEGINNER_GUIDE.md).

## Ownership, provenance and synchronization

- **Source of truth for the tripwire:** [McGruber P01](https://github.com/jimedusot-beep/project-mcgruber/tree/main/projects/01-light-beam-tripwire) and its [assembly manifest](https://github.com/jimedusot-beep/project-mcgruber/blob/main/projects/01-light-beam-tripwire/assembly_manifest.json).
- **Standalone 3D inspection tool:** [3D Vision](https://github.com/jimedusot-beep/3D-vision).
- **This repository:** stores a transparent *reviewed snapshot* for electronics-learning and CAD/electrical handoff. It is **not** the canonical McGruber source and has no automatic sync.
- [`assembly_manifest.json`](assembly_manifest.json) records original blob IDs and the snapshot date so future differences can be audited.
- H.E.R.B.I.E. robot electronics, servo mounts, power budgets and safety checks do **not** inherit compatibility from this tripwire case study.

[Return to H.E.R.B.I.E. Cyborg Hardware](../../README.md)
