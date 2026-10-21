# Motion protocol compatibility audit — two existing *simulators*

**Engineering status:** This comparison is based on existing Herbie source/tests. Neither interface controls motors or meets hardware safety requirements. **Do not connect either to a physical motor controller.**

## Existing formats

| Property | Protocol Workbench V2 | Simulated Motion Port |
|---|---|---|
| Implementation | [Prototype V2](https://github.com/jimedusot-beep/Herbie/blob/main/prototypes/HERBIE_protocol_workbench_v2.html) | [Reuse simulated motion port](https://github.com/jimedusot-beep/Herbie/blob/main/experiments/reuse/simulated-motion-port.js) |
| Tests | [V2 tests](https://github.com/jimedusot-beep/Herbie/blob/main/tests/protocol-workbench-v2.test.cjs) | Test coverage must be independently checked |
| Envelope | `protocol:"herbie.motion", version:1, type:"command", id, seq, command, args` | `version:1, requestId, type, [direction, step]` |
| Command names | `look`, `center`, `stop`, `reset_stop` | `MOVE`, `CENTER`, `STOP`, `RESET` |
| Motion values | Simulated pan/tilt degrees | Simulated direction and small virtual steps |
| STOP | Software STOP latch with sequence exception | Simulated STOP latch; full ledger permits STOP |
| Reset behavior | Test explicitly expects STOP reset to **preserve prior virtual position** | Reset invokes simulator reset and **centers virtual position** |
| Hardware status | Software only | Software only |

**Critical incompatibility:** Both use the number `1` for a version while defining *different protocols*. Their command envelopes and reset semantics are not interchangeable. Do not implement an automatic translator just because versions match.

## Decision required before any live adapter

1. Choose a canonical, newly identified contract (`herbie.motion.hardware` proposed name only, no actual version assigned).
2. Define move units, valid range from real mechanisms, request ID and ordering, acknowledgements, error and timeout handling.
3. Define `STOP`, `clear_fault`, `reset` separately. Resetting a software latch must never unexpectedly command motor movement.
4. Require local actuator controller limits and loss-of-link handling regardless of browser operation.
5. Keep hardware communication opt-in and disabled by default. Require verified physical motor power interruption separate from any browser STOP.
6. Test deterministic fault injection in simulation and only then bench-test with selected electronics.

Open-source references worth studying for *patterns, not copied code*: [ROS 2 control demos](https://github.com/ros-controls/ros2_control_demos) and [Pan-Tilt-TeleOp](https://github.com/irfanjamal88/Pan-Tilt-TeleOp). No third-party interface is implied compatible with H.E.R.B.I.E.

**Related owner-reviewed requirements:** [Herbie engineering requirements V0.2](https://github.com/jimedusot-beep/Herbie/blob/main/docs/engineering/foundation-v0.2/REQUIREMENTS.md). Owner approval of desired behavior is not physical testing or approved electrical design.
