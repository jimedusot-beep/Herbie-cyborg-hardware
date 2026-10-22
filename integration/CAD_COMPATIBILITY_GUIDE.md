# CAD-to-electronics compatibility — provisional mapping

This is a **planning map**, not a measured fit or electrical schematic. The authoritative mechanical part inventory is [3D-vision/HERBIE_V1/PARTS.csv](https://github.com/jimedusot-beep/3D-vision/blob/main/HERBIE_V1/PARTS.csv). The authoritative electronic component IDs are [bom/components.csv](../bom/components.csv). The [machine-readable map](../integration/cad-electronics-compatibility.json) references both without copying their canonical inventories.

| Electronic component | Provisional CAD locations | Next measurement |
| --- | --- | --- |
| `CTRL-MAIN-001` | `HBR-016` computer adapter tray | Exact board model, holes, connector reach and airflow |
| `SERVO-HEAD-PAN-001` | `HBR-004` internal head frame; `HBR-005` neck; `HBR-006` upper frame | Pan axis loading, mounting/shaft geometry and cable twist |
| `SERVO-HEAD-TILT-001` | `HBR-004` internal head frame; `HBR-005` neck | Center of gravity, tilt torque, stops and travel clearance |
| `DISPLAY-FACE-001` | `HBR-003` faceplate; `HBR-004` head frame | Screen overall dimensions, active area, bezel, connector and heat |

**Caution:** `HBR-005` is presently named **Fixed_Neck**. A proposed moving pan/tilt joint cannot be assumed compatible with a fixed neck. It may require an additional redesigned part and bearing arrangement. Do not drill, print or mount based solely on this table.

## Two mutually exclusive servo paths

1. **RC PWM:** select two conventional positional RC servos, then evaluate PCA9685 or Pololu Maestro 6. Requires a suitable separate motor supply and mechanical design.
2. **DYNAMIXEL TTL:** select appropriate XL330/XC330 serial smart actuators and a compatible TTL interface; PCA9685/Maestro pulse outputs are **not** compatible with this bus.

Neither path is selected. Do not transfer the published dimensions of a smart servo to an unidentified RC servo.

## Minimum measurement worksheet

For each selected part, record manufacturer model/revision, measured envelope (width/height/depth in mm), mounting-hole center distances, shaft/horn geometry, measured mass (g), clearance from moving joints, cable strain relief and routing, supply and signal connector orientation, and physical source of each measurement.

For the head, record **measured total mass** and center-of-mass offset relative to each joint axis. Compute static torque from the appropriate perpendicular lever arm and then independently consider dynamic loading and manufacturer continuous ratings.

The existing [skeleton assembly manifest](https://github.com/jimedusot-beep/3D-vision/blob/main/EXPERIMENTS/001_HERBIE_SKELETON/assembly_manifest.json) is explicitly `DIGITAL_CONCEPT_UNTESTED` with electronics placeholders not measured. Its five listed transforms do not establish the complete 18-part physical assembly.

## Automated checks and their limit

`python3 -m unittest discover -s tests -p 'test_*.py'` checks that component IDs match the BOM, referenced CAD IDs exist in the known HBR-001–HBR-018 range, and no unsupported verified fit/dimension claims appear. The mechanical inventory is still owned by 3D-vision; **these tests do not fetch live remote CAD files or validate mesh geometry**.

Before first physical assembly, confirm the CAD part list has not changed, then review real dimensions and power/electrical design independently.
