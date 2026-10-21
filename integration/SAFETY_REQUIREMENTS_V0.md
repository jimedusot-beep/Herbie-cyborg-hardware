# Physical motion safety requirements — proposed V0

**Not implemented or certified.** These are reviewable target properties for a future tabletop robot. Do not follow this document as wiring instructions. All physical actuation stays disabled in `integration/system-manifest.json`.

| ID | Requirement to implement and verify | Evidence required later |
|---|---|---|
| SAFE-01 | Power-on and every restart begin **disarmed**; unknown controller state cannot generate a movement request | Local-controller startup test and measured actuator output |
| SAFE-02 | Distinguish **software STOP**, latched fault, physical motor-power interruption, and RESET/CLEAR; clearing a stop must never command motion | Simulated state-machine tests, then supervised physical tests |
| SAFE-03 | Unexpected host disconnect, controller reset, stale/duplicate/out-of-order command and timeout prevent new motion | Fault-injection test logs with timing |
| SAFE-04 | Local controller (if selected) enforces measured axis travel, speed and acceleration limits, irrespective of browser command | Mechanical fit record and supervised limit tests |
| SAFE-05 | Motor supply has independently reviewed disconnect/interrupt, overcurrent protection and appropriate wiring; web STOP is **not** an emergency-stop device | Circuit/schematic independent review plus physical interruption verification |
| SAFE-06 | Brownout, watchdog trip or signal loss must not silently return to armed movement | Restart/disconnect/undervoltage test matrix |
| SAFE-07 | Physical end-stops, cable snag, pinch points and load/torque limits are evaluated before energization | [3D Vision](https://github.com/jimedusot-beep/3D-vision) measurements and inspection |
| SAFE-08 | Logs label a command as simulated or physically demonstrated and record which controller/firmware revision was used | Test evidence with device identity; not mere CI green |
| SAFE-09 | Recovery requires deliberate owner action and verified safe state; no remote automatic restart into motion | Fault-latch state model and controlled recovery test |

**Stop categories are different:** software STOP requests behavior; an ESP32 watchdog (if present) can independently reject/stop commands only if implemented; a correctly designed **physical motor-power interruption** removes the energy path. None exists in verified H.E.R.B.I.E. hardware today. Cutting servo power can cause a load to move under gravity; mechanical hazard analysis and supervised tests remain necessary.

## Offline-only design exercises

1. Draw a state chart: `DISARMED → READY → FAULT_LATCHED`; show that `CLEAR_FAULT` returns to **DISARMED** without an implied movement.
2. Write table-driven simulator tests for stale IDs, missing ACK, invalid target and repeated STOP.
3. Determine the unknown physical measurements needed for actual local limits. **Do not use the simulated angle range** as hardware calibration.
4. Draft questions for an electronics reviewer about power domain separation and physical stop effectiveness under MCU failure.

Related documents: [real build gates](BUILD_READINESS_CHECKLIST.md), [controller options](../controllers/ARCHITECTURE_OPTIONS.md), [simulated protocol split](../docs/MOTION_PROTOCOL_COMPARISON.md).

**No electronics have been selected, wired or tested through this document.**
