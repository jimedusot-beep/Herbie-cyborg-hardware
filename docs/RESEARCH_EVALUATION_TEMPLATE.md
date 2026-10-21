# Evaluate an outside robotics design — worksheet

**Copy these headings into a new review issue or decision record.** Do not import third-party assets while filling this out.

| Field | Entry |
|---|---|
| Research library ID / project | TBD |
| Exact source URL and author | TBD |
| Specific file or hardware revision examined | TBD |
| Original asset-level license and attribution obligations | **Unverified** |
| What will H.E.R.B.I.E. learn? | TBD |
| Responsibility: brain / electronics / body | TBD |
| Required MCU, framework, firmware versions | TBD |
| Exact servo/sensor/driver model and datasheet | TBD |
| Supply and logic voltages (including tolerances) | TBD |
| Typical, startup and worst-case/stall current evidence | TBD |
| Connector/pin mapping source | TBD |
| Wiring/protection schematic independently reviewed? | **No** |
| Mechanical mass, center of gravity and measured mounts | TBD |
| Faults: startup, link loss, stall, timeout and STOP | TBD |
| Simulated-only test and expected failure behavior | TBD |
| Physical bench evidence (date, instruments, values) | **None** |
| Current stage: proposed/acquired/bench-verified/simulated/physically-demonstrated | **Proposed reference only** |
| Reviewer decision and remaining unknowns | **Pending** |

## Decision rules

- **Cite the exact artifact's license.** A website's or article's license is not automatically the attached code, CAD or photo's license. No copying while unclear.
- **Require a part number and datasheet** before selecting power, a pin map or physical servo travel range. An online author's successful demo is not a compatibility guarantee.
- **Keep categories separate:** owning a board does not make it verified; simulated movement does not demonstrate physical movement.
- **Do not borrow a software STOP as a hardware stop.** Motor-power interruption needs its own design, review and controlled test.
- **Coordinate by ownership:** Herbie owns facial behavior and software intent; this repository owns electronics and measurement evidence; 3D Vision owns CAD shapes, mounting design and mechanical fit.
- **No live actuation from this worksheet.** Advance through [build readiness gates](../integration/BUILD_READINESS_CHECKLIST.md) only with independently reviewed evidence.
