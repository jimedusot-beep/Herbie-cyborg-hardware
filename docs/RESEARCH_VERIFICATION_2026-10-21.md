# Research library evidence review — 2026-10-21

This review checks project identity and certain explicit source-page claims for entries **13–24** in [the numbered library](RESEARCH_LIBRARY.md). It **does not** validate build safety, electrical ratings, dependencies, CAD fit, downloaded files, or open-source redistribution clearance. No source assets copied.

| ID | Evidence reviewed | Source finding | Still unverified |
|---|---|---|---|
| 13 | [Hackaday project](https://hackaday.io/project/181344) | Stack-chan; author states Apache-2.0 covers firmware, case and schematic | Actual individual GitHub file licenses, controller compatibility, mechanics |
| 14 | [Hackaday project](https://hackaday.io/project/204422-fieb-friendly-interactive-exploring-bot) | ESP32 wheeled experiment and dual OLEDs; source currently shows zero files, zero listed components, zero instructions | Wiring, exact model/revisions, downloadable assets, license |
| 15 | [Hackster project](https://www.hackster.io/roboattic_Lab/diy-smart-desktop-companion-016aed) | XIAO ESP32-S3 with OLED, touch and servo; article shows CC BY-NC-SA | Attached code/CAD licensing, current capacity, pinout: step text says touch GPIO2 while embedded firmware prompt says GPIO4. **Do not adopt wiring** |
| 16 | [Hackster project](https://www.hackster.io/fabiosouza/esp32-robot-with-esp-now-control-and-animated-eyes-efa2a2) | ESP-NOW telemetry and 500 ms link-loss stop; robot uses N20 **DC gear motors**, MX1508 H-bridge; article displays MIT | Attached library licenses, proof of fail-safe independence or applicability to servos |
| 17 | [Indexed Instructables page](https://www.instructables.com/Pan-and-Tilt-Camera-With-ESP32-CAM-L0Cost-Robot-Co/) | ESP32-CAM with two SG90 servos; LiPo supply described | Full direct page extraction blocked; actual safe wiring and ratings not independently checked |
| 18 | [Indexed Instructables page](https://www.instructables.com/Wi-Servo-Wi-fi-Browser-Controlled-Servomotors-with/) | Arduino Uno + ESP8266 remote browser demo; text warns about Servo/SoftwareSerial timer conflict | Full direct extraction blocked; cannot treat tutorial limits as physical safety |
| 19 | [Indexed Printables listing](https://www.printables.com/model/251907-robot-head-from-stray-game) | Modular facial attachments; CC BY-NC 4.0 listing and a remix relationship | Full direct extraction blocked; upstream model provenance and attached files need a separate license review |
| 20 | [Indexed Printables listing](https://www.printables.com/model/967152-pan-tilt-camera-mount) | Manual camera tripod mount, fasteners and washers; CC BY-SA 4.0 listing | Full direct extraction blocked; not a servo-driven design or H.E.R.B.I.E. fit proof |
| 21 | [GitLab project](https://gitlab.com/noeFly/simpleservoesp32) + [LICENSE](https://gitlab.com/noeFly/simpleservoesp32/-/blob/main/LICENSE) | Lightweight ESP32 servo library; LICENSE page identifies MIT | Compatibility, maintenance, examples, hardware tests |
| 22 | [GitLab project](https://gitlab.com/lgdxrobotics/lgdxrobot2-chassistuner) + [GitHub mirror](https://github.com/yukaitung/lgdxrobot2-chassistuner) | Qt GUI for robot diagnostics; mirror identifies GPL-3.0 and cites differently licensed third-party libraries | Original GitLab LICENSE contents and individual files/assets not independently reviewed |
| 23 | [Arduino Project Hub page](https://projecthub.arduino.cc/ryan6534/recordable-cardboard-robot-arm-4b6783) | Record/replay arm demo; site displays GPL3+; illustrated code includes 5 servo channels | Electrical suitability, load measurements, reuse permissions on attached assets |
| 24 | [Arduino Project Hub page](https://projecthub.arduino.cc/milespeterson101/arduino-robotic-arm-8b8601) | Three-servo Arduino learning example; page displays CC BY-ND 4+ | Permissions for derivatives, selected servo/board match, physical safety |

### Verification levels used

- **Direct page/repository**: web-readable primary page or source repository landing page; not an audit of its entire codebase.
- **Indexed page**: discoverable search-engine project text while direct extraction is inaccessible; lower confidence for complete instructions.
- **License claim**: page-level assertion or a specific visible LICENSE landing page; not conclusive for separately attached code, CAD, photos or dependencies.
- **reference_only**: no approval to reuse, connect, power, move, purchase or merge parts.

### Critical corrections to the first draft

1. Record #21's visible MIT license instead of leaving its license completely unchecked. Its *technical compatibility* remains unchecked.
2. Record #16's MIT article claim; do not infer a license for every referenced library.
3. Flag #15's conflicting touch-sensor GPIO number as well as the risk of sourcing servo power from the controller board.
4. Flag #14's lack of published project files/instructions, #19's upstream remix license, and #22's GPL-3.0 mirror with third-party-license caveats.

Before reusing any example, document **exact component datasheets, software versions, license of each artifact, reproducible tests, mechanical fit and independent motor-power safety review** in the [research evaluation worksheet](RESEARCH_EVALUATION_TEMPLATE.md).
