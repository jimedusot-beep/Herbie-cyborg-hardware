# H.E.R.B.I.E. numbered robotics research library

**Reviewed: 2026-10-21 · Purpose: study, not direct integration.** This catalogue tracks public examples, not selected parts, validated wiring, approved firmware, or proven safety systems. No source code, CAD, schematic or project media is imported here.

## How the numbering works

- **1–6 — Original GitHub research slots:** six earlier GitHub robotics references covering ESP32, servo control, robot arms, ROS 2 and pan/tilt. Their exact original project names/URLs were **not included in this handoff**, so these IDs are reserved rather than assigning speculative substitutes. [Previously reviewed GitHub examples](OPEN_SOURCE_DESIGN_REVIEW.md) remain available separately; do not assume they were the original numbered six.
- **7 — [Hackaday.io](https://hackaday.io/)**: documented build logs and prototype lessons.
- **8 — [Hackster.io](https://www.hackster.io/)**: project write-ups and component/firmware examples.
- **9 — [Instructables](https://www.instructables.com/)**: stepwise build tutorials.
- **10 — [Printables](https://www.printables.com/)**: downloadable mechanical concepts and license terms.
- **11 — [GitLab](https://gitlab.com/)**: source repositories and development practices.
- **12 — [Arduino Project Hub](https://projecthub.arduino.cc/)**: microcontroller learning projects.

These six websites are *portals*, not individual designs. Items **13–24** select two projects per portal, preserving their numbering.

## 13–24: specific inspiration projects

| # | Site and original source | Useful idea for H.E.R.B.I.E. | Reuse and engineering caution |
|---|---|---|---|
| 13 | Hackaday — [Stack-chan](https://hackaday.io/project/181344) | Expressive face, conversational presence and head movement | Page claims Apache-2.0 for firmware/models/schematics; verify each original asset's license and physical limits before adaptation |
| 14 | Hackaday — [F.I.E.B.](https://hackaday.io/project/204422-fieb-friendly-interactive-exploring-bot) | ESP32 sensing, movement and expressive displays | Experimental project: the listing has no files, components or instructions at the time of review; no usable schematic or asset license confirmed |
| 15 | Hackster — [DIY Smart Desktop Companion](https://www.hackster.io/roboattic_Lab/diy-smart-desktop-companion-016aed) | XIAO ESP32-S3, touch interaction, OLED eyes and a servo | Tutorial shows servo power from a board 5V pin and also warns of excess current. Its connection instructions list touch GPIO2 but a later firmware prompt says GPIO4; **do not copy the wiring or pin map**. Verify power, pinouts and actual code independently. Page displays CC BY-NC-SA; attached assets/code need separate review |
| 16 | Hackster — [ESP32 Robot with ESP-NOW and Animated Eyes](https://www.hackster.io/fabiosouza/esp32-robot-with-esp-now-control-and-animated-eyes-efa2a2) | Keep-alives, link-loss response, telemetry and eye animation | Uses **two DC gear motors with an H-bridge**, not pan/tilt servos. Its reported 500 ms fail-safe is project-specific, not a verified H.E.R.B.I.E. safety timing. The article displays MIT; attached libraries/assets still need individual license review |
| 17 | Instructables — [ESP32-CAM Pan and Tilt Camera](https://www.instructables.com/Pan-and-Tilt-Camera-With-ESP32-CAM-L0Cost-Robot-Co/) | Two-axis servo bracket and camera aiming | Site content was confirmed via indexed page, not a full direct technical review. Tutorial mentions a LiPo supply; do not adopt electrical or battery wiring without separate safety review |
| 18 | Instructables — [Wi-Servo Browser Control](https://www.instructables.com/Wi-Servo-Wi-fi-Browser-Controlled-Servomotors-with/) | A browser can send high-level movement requests | Uses **Arduino Uno plus ESP8266**, not a native ESP32 controller. Browser motion limits are not independent safety limits; older libraries/timers may conflict |
| 19 | Printables — [Robot Head from Stray](https://www.printables.com/model/251907-robot-head-from-stray-game) | Modular interchangeable snap-on facial pieces | Listed **CC BY-NC 4.0**: attribution and non-commercial restriction. This is a remix with an upstream model that also needs license/provenance review; source observed via indexed page. No measured H.E.R.B.I.E. fit |
| 20 | Printables — [Pan & Tilt Camera Mount](https://www.printables.com/model/967152-pan-tilt-camera-mount) | Yokes, washers, inserts, fastening and mechanical clearances | A **manually adjusted tripod camera mount**, not an approved servo bracket. Listed **CC BY-SA 4.0**; source observed via indexed page. No motor torque or fit validation |
| 21 | GitLab — [SimpleServoESP32](https://gitlab.com/noeFly/simpleservoesp32) | Minimal ESP32 servo software | Repository landing page confirms purpose and its [LICENSE page](https://gitlab.com/noeFly/simpleservoesp32/-/blob/main/LICENSE) displays **MIT**; maintained API, ESP32 core/version compatibility and electrical safety are **not yet checked** |
| 22 | GitLab — [LGDXRobot2 ChassisTuner](https://gitlab.com/lgdxrobotics/lgdxrobot2-chassistuner) | Testing dashboard, logging and performance diagnostics | **Direct source repository** (replaces generic GitLab robotics directory link). Project's [GitHub mirror](https://github.com/yukaitung/lgdxrobot2-chassistuner) reports **GPL-3.0**, with separately credited third-party libraries; verify exact file licenses before reuse. Intended for different hardware |
| 23 | Arduino Project Hub — [Recordable Cardboard Robot Arm](https://projecthub.arduino.cc/ryan6534/recordable-cardboard-robot-arm-4b6783) | Store and replay motion sequences *in simulation first* | Page displays **GPL3+**. Arm and example servos are not suitable evidence for H.E.R.B.I.E. load/current or mounting fit |
| 24 | Arduino Project Hub — [Arduino Robotic Arm](https://projecthub.arduino.cc/milespeterson101/arduino-robotic-arm-8b8601) | Beginner learning about three servo channels and control | Page displays **CC BY-ND 4+**; restrictions on derivatives must be reviewed before any reuse. A tutorial is not a safety-approved schematic |

**Access evidence (2026-10-21):** Direct source pages were inspected for #13–16, #21–24. Indexed project pages were inspected for #17–20 because direct extraction was restricted. [See source-by-source audit](RESEARCH_VERIFICATION_2026-10-21.md). A working URL/title **does not** verify its complete build instructions, code, license on every attached asset, electrical safety, compatibility or maintenance. License labels above are **page-level claims, not legal clearance**.

See the [CSV index](RESEARCH_PROJECTS_13_24.csv) for structured reference statuses.

## Recommended order of study

1. **Expressions:** #13 and #15 — identify which ideas belong in the *Herbie brain* versus hardware.
2. **Sensing and communication:** #14 and #16 — draw a conceptual message flow and simulate link loss; no motor power.
3. **Mechanical movement:** #17 and #20 — list required actual load, center of gravity, travel and clearances; give measured dimensions to *3D Vision*.
4. **Servo and diagnostic education:** #18, #21, #22, #23 and #24 — compare programming conventions, testing and motion replay; do not run third-party servo code on unverified actuators.
5. **Modularity:** #19 — study replaceable exterior pieces without importing or modifying its model until the relevant license is understood.

## Evidence gate before reusing anything

Use the [research evaluation template](RESEARCH_EVALUATION_TEMPLATE.md) for the **exact file/artifact**, not just its project landing page. Require source URL, author, asset-specific license, dependencies and versions, target voltage/logic/current ranges, compatible controller and actuator part numbers, pinout references, mechanical dimensions, safety risks and a reproducible test plan. Record separately whether the idea is **proposed**, **acquired**, **verified on a bench**, **simulated only**, or **physically demonstrated**.

A copied wiring diagram is **not** a verified schematic. A servo demo is **not** an independently tested physical STOP circuit. No external project changes the manifest's `motion_enabled: false` or the [build readiness gates](../integration/BUILD_READINESS_CHECKLIST.md).
