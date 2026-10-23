# Bench-to-CAD roadmap — one low-voltage tripwire

**Project boundary:** An educational standalone light-beam alarm for supervised play. This is **not** the H.E.R.B.I.E. robot's head, motor driver, Pi/ESP32 controller decision, or validated safety circuit. The CAD views are based on unmeasured primitives.

## See it before building it

- [Exploded 3D concept, directly in 3D Vision](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-exploded) — orbit, zoom, isolate or inspect 13 parts once the Experiment 002 release is live
- [Assembled 3D concept, directly in 3D Vision](https://jimedusot-beep.github.io/3D-vision/?example=mcgruber-tripwire-assembled)
- [Standalone exploded STL in this repository](models/exploded.stl) and [labeled exploded drawing](diagrams/exploded-assembly.svg)
- [Blank part identification / measurements CSV](measurement_intake_template.csv) — complete only with actual observations
- [Electronics signal-flow diagram](diagrams/signal-flow.svg)

If the 3D Vision link is not deployed yet, use the STL right here or import this repository's [exploded OBJ](models/exploded.obj) manually in [3D Vision](https://jimedusot-beep.github.io/3D-vision/) with source units **millimeters** and source up-axis **Y**.

## Stage A — identify the hardware without energizing it

1. Record the exact source of every low-voltage donor: flashlight, battery toy, LDR/phototransistor, switches, plastic shell or USB power bank. Do not describe unknown salvage as tested or owned.
2. Note markings, model/revision, original power supply and visible damage. Salvage an **intact battery flashlight** as the emitter if possible; this avoids trying to guess LED drive-current circuitry.
3. With all power removed, inspect physical wires and terminals. Use multimeter continuity only on unpowered parts, and resistance measurement only on appropriate unpowered resistors/sensors.
4. Save **observed dimensions** in the [measurement template](measurement_intake_template.csv): emitter and receiver envelope, mounts, board outline, connector clearance, sensor diameter, cable-exit location, and stand/beam height. Leave unknowns blank.

**Gate A:** component identities, battery chemistry/voltage and exposed wiring condition are actually documented. An unmarked toy circuit is not automatically an Arduino-compatible controller.

## Stage B — prove the optical principle first

1. Set a low-brightness visible LED source below eye level, several inches from an LDR. Do **not** use lasers, IR emitters requiring eye-safety calculations, or any wall-powered circuitry removed from mains equipment.
2. Compare the sensor under **beam present**, **hand blocks beam**, **room light on**, **room light off**, and nearby sunlight. Start by documenting resistance (for an identified LDR) with the circuit unpowered.
3. Try a short black straw around the light sensor to reduce unwanted light. Do not assume a solar garden lamp's photovoltaic cell behaves like a fast detector; test its actual response separately if you experiment with it.
4. Repeat several light/blocked cycles. Record both successful detections and misses in your private notes; don't write fabricated numbers into the public CSV.

**Gate B:** the real sensor gives a repeatable, distinguishable response under the actual planned game lighting.

## Stage C — safe controller input

For a **bare LDR example only**, a voltage divider can create an analog measurement node:

```text
ESP32 board's REGULATED 3.3 V  --->  [ LDR ] ---o--- [ fixed resistor ] --->  GND
                                                     |
                                             ADC signal at node o
```

The signal node is between the LDR and fixed resistor as shown. If the LDR and fixed resistor are swapped, the sensed voltage changes in the opposite direction. The ADC-capable GPIO, fixed resistance, detection threshold and signal-conditioning requirements remain **unselected until the exact ESP32-C3 board and sensor are known**. A phototransistor needs its own identified bias arrangement.

Verify minimum and maximum node voltages with the multimeter and confirm every possible state stays within the **selected board's GPIO input rating** before connecting. **Do not apply 5 V USB or an unregulated solar cell directly to a 3.3 V-rated GPIO.**

For a bare LED use a resistor/current-limited driver verified against the actual supply and LED; a complete rated flashlight can retain its existing power arrangement.

**Gate C:** actual signal voltages, measured supply and polarity are recorded, with no out-of-range input.

## Stage D — local software then phone

1. Load a minimal ESP32 program from a USB **data** cable and laptop. First display the analog sensor readings over USB; the 3D animation alone is not hardware evidence.
2. Determine a threshold from the recorded **beam present** versus **blocked** ranges. Use hysteresis and a short debounce/minimum trigger duration to reject flicker and ambient changes.
3. Expose **clear / broken / disconnected** states on a webpage hosted by the ESP32 or another local host. Do not represent a failed Wi-Fi connection as an intact beam.
4. For audible browser alerts, include an **Enable sound** tap and keep visible text status—the browser may block automatic audio before interaction or when in the background.
5. Measure detection reliability under multiple room-light conditions before adding multiple beams.

**Gate D:** the phone reports actual controller readings, not a simulated animation. Keep firmware and physical test results separately versioned from this geometry.

## Stage E — physical assembly only after measurements

- Use the [assembled OBJ](models/assembled.obj) to understand group placement, not as a drill/print template.
- Replace each **illustrative** primitive using documented outside dimensions and mounting-hole center distances.
- Design a removable cover, cable strain relief, stable mount, accessible low-voltage power switch and safe connector clearance.
- Inspect the real case for sharp edges, trapped wires and fragile connections.
- Perform repeated hand-block tests with the actual assembly and log false triggers or missed crossings.

**Gate E:** label the assembly fit as verified only after a measured physical dry fit. No step automatically graduates H.E.R.B.I.E. itself to build-ready.

## Traceability checklist

| Evidence | Source | Missing until physically observed |
| --- | --- | --- |
| Part IDs | [assembly_manifest.json](assembly_manifest.json) | Real manufacturer/model association |
| 3D component geometry | [STL/OBJ](models/exploded.obj) | Real exterior dimensions, fit and tolerance |
| Electrical circuit | [signal-flow.svg](diagrams/signal-flow.svg) | Rated schematic, polarity, actual GPIO pinout |
| Hardware ownership | [measurement CSV](measurement_intake_template.csv) | Identification/receipt/donation or private inventory photo |
| Detection performance | Real user bench tests | Repeatable response, noise margin and missed/alarm rate |

**Safety:** Low-voltage, supervised setup only. Keep all sources away from eyes; do not disassemble AC-powered night lights, damaged lithium batteries or mains adapters. No fabrication/motion certification is implied by this repo.

[Back to case-study README](README.md) · [Cyborg beginner safety](../../docs/BEGINNER_GUIDE.md)
