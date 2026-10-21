# Measure the head before selecting an actuator

**H.E.R.B.I.E. engineering worksheet — planning only (2026-10-21).**
There is **no measured head mass, center of gravity, moving joint, tested motor, or validated servo mount** in the repositories reviewed. The [body's skeleton manifest](https://github.com/jimedusot-beep/3D-vision/blob/main/EXPERIMENTS/001_HERBIE_SKELETON/assembly_manifest.json) is `DIGITAL_CONCEPT_UNTESTED` and says electronics placeholders have not been measured. A successful static-torque calculation **does not authorize energizing hardware**.

## Ownership across our three repositories

- **3D Vision / body:** authoritative CAD geometries, mechanical part labels, eventual printed-part fit, center-of-gravity location, physically measured travel, fasteners and new moving-neck design.
- **Cyborg Hardware / nervous system:** records mechanical *requirements* for actuator choices, torque screening, part datasheets, wiring/power selection and evidence gates. Do not duplicate authoritative STL/STEP parts here.
- **Herbie / brain:** simulation, high-level intent and fault response; software virtual angles are **not** calibrated travel limits for a real head.

See open [CAD compatibility review PR #7](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/pull/7). The current `HBR-005` part in [3D Vision's provisional part inventory](https://github.com/jimedusot-beep/3D-vision/blob/main/HERBIE_V1/PARTS.csv) is **Fixed_Neck**, *not* evidence of a working pan/tilt axis. No design change is assumed by this worksheet.

## Minimum physical evidence to gather

| Measurement | Why it matters | Source required |
|---|---|---|
| Moving head assembly mass, in **grams** | Actuator gravity load and inertia | Weighed physical assembly, including its intended display, brackets, fasteners and cables as appropriate |
| Center of gravity relative to proposed **tilt axis** | Gravity moment depends on offset from tilt axis | Physical balance/geometry evidence; identify assembly revision |
| Projected **gravity lever arm**, in **millimeters**, at each relevant tilt pose | The horizontal offset from the horizontal tilt axis to the center-of-gravity **gravity force line**, projected into the plane normal to the tilt axis | A dated measurement with uncertainty and pose label; **not** just the radial distance from servo horn |
| Proposed pan axis, bearings and mass distribution | Vertical pan bearing torque depends on inertia, friction, acceleration and cable drag, not static gravitational tilt moment | 3D Vision design notes and actual measurements |
| Range, hard stops, pinch points and cable routing | Prevent collisions and cable twist | CAD interference study **then** physical check |
| Joint speed, acceleration, duty cycle, mounting dimensions | Continuous operation and load capacity differ from stall torque | Design requirements and manufacturer continuous ratings |
| Actual device models, voltage and worst-case current | Safe power calculations and protocol compatibility | Exact manufacturer datasheets and supervised electrical design |

**No component has been selected.** Keep original CAD IDs and component IDs in their authoritative repositories. New moving-neck or bracket CAD belongs in 3D Vision, not this repo.

## Header-only measurement evidence template

File: [head-load-observations.csv](../integration/head-load-observations.csv). It deliberately has **zero rows** until someone reports genuine measurements.

- `record_id`: unique `HEAD-001` etc.
- `axis`: `tilt_horizontal` or `pan_vertical`; **only tilt-horizontal** static gravity moments are calculated.
- `assembly_revision`: physical/printed assembly identifier, not just a conceptual render.
- `pose_label`: describe exactly which pose was measured (e.g., centered, tilted forward); the lever arm can change with pose.
- `measurement_basis`: `physical_measurement` or `cad_estimate`. **CAD-only estimates are deliberately rejected** by the physical load screen.
- `moving_mass_g`: actually weighed moving mass, in grams; excludes permanently stationary parts.
- `gravity_lever_arm_mm`: magnitude of horizontal CG offset, in mm, *perpendicular to the tilt axis*, at that pose. Not generic centroid-to-horn distance.
- `measurement_date`: a real calendar date in `YYYY-MM-DD` format.
- `evidence_reference`: a non-sensitive note/document reference with method and measurement source. **A non-empty string is not independent certification.**
- `notes`: measurement instrument, tolerance, approximations and uncertainty; do not disclose private identity/location/serial data.

A pose-specific observation is **not** sufficient to define a full safe range. Record several real poses and compare with exact actuator continuous ratings, dynamics, and mechanical factors after the body exists.

## Offline static gravity screening (no electronics)

Run from repository root:

```bash
python3 tools/head_static_torque.py
```

Until physically recorded and complete measurements exist, the script exits with **MECHANICAL SCREEN INCOMPLETE**. It never treats missing values as zero and it does not calculate a servo rating.

For a **horizontal tilt axis only**, the magnitude of a static gravity moment is:

```text
static_torque_Nm = (moving_mass_g / 1000) × 9.80665 × (gravity_lever_arm_mm / 1000)
```

This is a physics **screening calculation** for the chosen pose, not an actuator-selection or continuous-torque formula. Tests use **fictional numeric inputs** as mathematical examples; those numbers are not H.E.R.B.I.E. measurements and are never stored as real evidence. An observed zero lever arm can produce zero *static* gravity moment at one pose while dynamic torque and bearing loads remain.

For a **vertical pan axis**, ideal static gravity torque about that axis is insufficient for motor sizing; acceleration, head rotational inertia, joint friction, bearings, disturbances, cable twist and duty cycle remain unknown. The tool **rejects** pan rows rather than reporting a misleading usable zero.

Even with valid rows, a screen result remains **not build-ready**. Real motor choice still requires mechanical fit, acceleration/inertia, continuous torque/duty cycle, stall current, voltage/interface compatibility, collision/limits and independently reviewed STOP/power interruption.

## Next review handoff

1. The owner identifies any actual printed/assembled parts (if none, status remains **unknown**).
2. 3D Vision evaluates how `Fixed_Neck` could be revised for a two-axis mechanism without assuming it already moves.
3. When actual moving assembly exists, record *real measurements* with date, method and uncertainty.
4. Cyborg Hardware can calculate gravity screening and compare **possible** exact actuator datasheets.
5. Do not advance to wiring, purchasing or live control without the [build readiness checklist](../integration/BUILD_READINESS_CHECKLIST.md), a reviewed schematic and a tested independent motor-power interruption plan.

**No physical testing or hardware motion has been performed by this documentation.**
