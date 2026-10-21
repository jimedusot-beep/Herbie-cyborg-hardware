# Main computer and actuator-control architecture — preliminary comparison

**Status: options only (2026-10-21). No selection or physical tests.** The target is a tabletop expressive robot with a simulated face and *proposed* two-axis head. Do not infer that a Raspberry Pi, ESP32, servo driver or suitable motor supply is owned.

## Architecture options

| Option | Proposed division of labor | Advantage | Main weakness / evidence needed |
|---|---|---|---|
| **A: Raspberry Pi + PCA9685-style PWM driver** | Pi runs higher-level software and sends servo pulses indirectly via I2C driver; driver only produces PWM | Relatively simple setup and a separate pulse generator; manufacturer documentation exists | **A PWM board is not an independent watchdog or safety controller.** Pi freeze or stale pulse/driver behavior needs explicit tested design; independent motor-power cutoff remains essential |
| **B: Raspberry Pi + ESP32 MCU** | Pi owns expression/vision/AI; ESP32 *could* enforce local state, commands, limits, watchdog and generate PWM | Separation may allow local fault handling even when Linux/browser crashes | More firmware and versioned messaging; USB/UART unplug/restart behavior must be measured. Independent safety depends on *implemented and tested* firmware plus **separate electrical power interruption** |
| **C: ESP32 MCU only for an early standalone demo** | MCU handles limited sensor, display and motion experiments; Herbie's full conversational software stays external/simulated | A small educational bench target and lower software complexity for limited tasks | Not a drop-in home for a full AI/vision app; different capabilities, RAM, display interface and networking require verification. Do not declare it H.E.R.B.I.E.'s selected brain |

### Why these are research candidates

- Raspberry Pi [hardware documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) explicitly warns **not** to connect motors directly to GPIO; computer GPIO generally uses 3.3 V logic.
- Adafruit's [PCA9685 servo driver guide](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up) explains why servo V+ must be supplied appropriately and separately from logic VCC. Its tutorial **is not** a final schematic or power-supply selection for this robot.
- Espressif's [ESP32-S3 MCPWM documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/mcpwm.html) documents programmable pulse generation and fault features. Hardware peripheral *capabilities* are not proof that required firmware or safe power interruption exists.
- [Simulated protocol comparison](../docs/MOTION_PROTOCOL_COMPARISON.md) shows two contradictory version-1 schemas. Neither can be connected to motors without an independently specified, validated hardware protocol.

## Intended functional boundary (illustrative, NOT wiring)

```text
Herbie browser/AI/face
         |
         | software intent: LOOK / STOP / query state (protocol TBD)
         v
Selected host or control service (undecided)
         |
         +-- Option A: PCA9685-style pulse driver (no local watchdog)
         |
         +-- Option B: ESP32 supervisor (local watchdog *to design/test*)
         |
         +-- Option C: educational ESP32-only standalone prototype
         |
         v
Motor signals (never enabled at this stage)
         |
Independent, reviewed motor-power interruption (NOT DESIGNED)
         |
Unselected actuators (NO PHYSICAL CONNECTION)
```

This diagram is about responsibilities, not physical series ordering or a schematic. Exact supply, controller enable pins, grounds, signal isolation, output behavior and power interruption need a reviewed **real** circuit.

## Selection requirements

1. **Mechanical:** measured moving head mass, center of gravity, moment arm, speed, estimated inertia and collision/cable clearance from *3D Vision*. Part dimensions in STL are insufficient.
2. **Electrical:** exact motor datasheets and logic thresholds, stalled/starting current, source impedance, separate motor and logic supply plans, wiring, fusing/overcurrent design, electrical shutoff and back-powering review.
3. **Software:** unique, authenticated/authorized command source as appropriate, strict version + sequence, acknowledgement, timeouts, replay protection, **power-on disarmed**, locally enforced calibrated travel boundaries, fault latch and distinct STOP/reset semantics.
4. **Faults:** bench-test startup, host crash, transport loss, MCU reset, undervoltage, sensor failure, stall and recovery. Determine what remains energized if PWM stops.
5. **Beginner feasibility:** number of interacting environments, reproducible simulator tests, maintainability, power cost, physical envelope and test equipment available.

## Provisional preference (NOT a decision)

Option B is **worth studying first** because it can segregate AI workloads from locally supervised motion *if* an independent watchdog and safe power-control path are designed and proven. Option A may be easier to prototype for pure pulse generation, but adds **no independent stop authority** by itself. Neither should be approved until the [decision worksheet](DECISION_WORKSHEET.md) and [safety gates](../integration/BUILD_READINESS_CHECKLIST.md) have evidence.

**Do not purchase parts, connect a servo, enable motion, or claim an E-stop based on this document.**
