# Three-project machine-readable integration contract

[`integration/system-manifest.json`](../integration/system-manifest.json) is a **planning interface manifest**, not a runtime command or verified wiring schematic. It references the authoritative electronic BOM here and the existing CAD and software source repositories.

The IDs `SERVO-HEAD-PAN-001`, `SERVO-HEAD-TILT-001`, `CTRL-MAIN-001`, and `DISPLAY-FACE-001` match `bom/components.csv`. CAD associations are deliberately `null` until measured mount compatibility is established. Software activation remains explicitly disabled.

This repository owns the electronics mappings; [3D-vision](https://github.com/jimedusot-beep/3D-vision/blob/main/HERBIE_V1/PARTS.csv) owns the 18 provisional mechanical identifiers `HBR-001`–`HBR-018`; [Herbie](https://github.com/jimedusot-beep/Herbie/blob/main/hardware/README.md) owns the software adapter planning.

Run `python3 tests/validate_bom.py` and `python3 tests/validate_manifest.py`. GitHub Actions automatically runs those checks and unit tests on a proposed PR; none of these tests confirm physical safety, mechanical fit, or build-ready schematics.
