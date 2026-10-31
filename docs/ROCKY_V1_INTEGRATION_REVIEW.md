# Rocky / Desk Robot V1 — Hardware Integration Review

**Status:** Research and simulation only. No copied firmware, pinout approval, physical build, or motor activation.
**Upstream:** https://github.com/cgro00/desk-robot
**Frozen reference:** https://github.com/cgro00/desk-robot/releases/tag/v1.0
**Upstream license:** MIT; copyright 2026 Casey (github.com/cgro00). Preserve its copyright and license notice if source is copied later.

## Evidence inspected
- V1 README and `docs/wiring.md`
- `docs/protocol.md`
- `firmware/include/config.h`
- `firmware/src/servo_neck.cpp`, `firmware/src/link.cpp`
- `firmware/platformio.ini`
- Upstream LICENSE and v1.0 Git tree

These are source inspections, **not** successful builds or independent electrical validation.

## V1 reference architecture
- **Computer:** Python brain server for speech, vision and high-level behavior.
- **Controller:** Seeed XIAO ESP32-S3 Sense with camera and microphone on-board.
- **Head:** SH1106 I2C OLED; Adafruit mini pan/tilt bracket with two SG90 servos (MG90S mentioned as alternative).
- **Audio:** MAX98357A I2S amplifier and speaker.
- **Communication:** ESP32 initiates Wi-Fi WebSocket connection to Python server; JSON control/state frames and binary audio/camera frames.
- **Power:** V1 guide describes 5 V / 2 A supply, shared ground, servo/amp 5 V and display 3.3 V, 470–1000 µF capacitor. **Do not adopt this wiring as H.E.R.B.I.E.'s power design.** Independent motor supply/protection and physical interruption require engineering review.

## Specific comparison with H.E.R.B.I.E.
| Topic | Rocky V1 evidence | Cyborg requirement / gap | Decision |
|---|---|---|---|
| Host/controller split | Python host + ESP32 local firmware | Controller architecture not selected | Adopt separation as **design pattern only** |
| Pan/tilt | Two SG90-class positional servos; firmware angle/speed limits | Actual H.E.R.B.I.E. head mass, mounts, travel, torque unknown | Research candidate, not approved part |
| Protocol | `hello` with shared token, JSON `pan`/`tilt` degrees, state, binary camera/audio | Canonical versioned contract, ACK, ordering, timeout, STOP/clear fault | **Not wire-compatible**; no direct import |
| Link loss | WebSocket reconnect and heartbeat | Local watchdog, fault latch, safe disarm | Source does not demonstrate full required safety |
| Calibration | Firmware `setRaw` permits bypass of normal travel bounds; command exposed for assembly | Physical limits cannot be bypassed by ordinary commands | **Do not reuse raw bypass** |
| Startup | Servo begin attaches and commands 0; idle glances supported | Boot disarmed; no unexpected motion | **Do not reuse startup behavior** |
| STOP | No physical power interruption established by inspected files | Independently reviewed motor power interrupt | Block actuation |
| CAD | V1 off-the-shelf bracket | 3D Vision geometry provisional; fit unknown | Compare measurements before any transplant |

## Adaptation scope
**Safe to implement now:** isolated, dependency-free Python simulation of a high-level host/controller message boundary with versioning, validation, sequence ordering, STOP latch, disarmed restart and explicit CLEAR_FAULT. No servo libraries, pin numbers or network listeners.

**Do not import:** Rocky `firmware/src/servo_neck.cpp`, `firmware/src/link.cpp`, pin maps, power wiring, personality/voice assets or proprietary artwork without a separate engineering and per-file license review.

## Release gates
1. Record actual owned components, exact model/revision and manufacturer datasheets.
2. Select and measure mechanical loads and clearances with 3D Vision.
3. Define one new hardware protocol independent of the two Herbie simulator v1 formats.
4. Specify independent motor power interruption, startup disarm and fault latch; review schematic.
5. Simulate disconnect, duplicate/stale messages, STOP/CLEAR_FAULT and startup.
6. Obtain owner approval and supervised bench evidence before any physical motor control.

**Fork status:** Research fork confirmed at https://github.com/jimedusot-beep/desk-robot . Frozen V1 branch: https://github.com/jimedusot-beep/desk-robot/tree/research/rocky-v1-frozen at upstream V1 commit `34614769c1211fc6943c18bc37ca7ddf850a7cc6`. This Cyborg branch remains a separate adaptation, not a fork.
