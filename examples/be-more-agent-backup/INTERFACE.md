# Backup-body interfaces

This wheel protocol is separate from Herbie's unfinished pan/tilt formats. Units are signed PWM **permille**, not degrees, m/s or a calibrated speed. The example accepts at most 200 permille (20% duty). Slew is a command-shaping bound, not measured vehicle acceleration.

## Pi / Pico / driver mapping

| Pico | Physical header pin | Pololu #2130 terminal |
|---|---:|---|
| GP2 | 4 | AIN1, left input 1 |
| GP3 | 5 | AIN2, left input 2 |
| GP4 | 6 | BIN1, right input 1 |
| GP5 | 7 | BIN2, right input 2 |
| GND | 8 | GND; motor return separately to driver |
| GP7 | 10 | nFAULT; external 10k pull-up to Pico 3V3 |
| 3V3 OUT | 36 | Pull-up and optional 3.3V sensor supply |
| USB | USB | Pi host data and Pico power |

Optional sensor inputs are GP8 pin 11 SDA, GP9 pin 12 SCL, GP10 pin 14 left bumper and GP11 pin 15 right bumper; GND pin 13. Bumpers remain disabled until fitted and tested. Leave carrier nSLEEP and sense terminals at their documented defaults. Do not join positive supply rails. The AA pack feeds driver VIN through the fuse and physical cutoff. Pi uses its separate UPS supply.

## USB serial packets

ASCII newline-delimited JSON, at most 256 characters per frame. Exactly the documented fields are accepted. Integer fields reject booleans and floats. Read `{"v":1,"op":"status"}` first. The response supplies a boot `session`, current `epoch`, `last_seq`, state, fault, outputs and whether arming is allowed.

- `arm`: `v`, `op`, `session`, `epoch`, `seq`. Requires DISARMED and the source-level physical-output review gate. It starts at zero output.
- `drive`: the same fields plus integer `left`, `right` (-200..200) and `lease_ms` (20..200). Requires ARMED. Expiry latches a fault and sets both outputs to zero. STATUS does not renew the lease.
- `clear`: the common fields, healthy inputs and a current epoch. Returns to DISARMED, never movement.
- `stop`: a recognizable `op:"stop"` always removes the movement request, even if its session/sequence is stale. It increments the epoch and does not clear an existing fault.

Sequence must strictly increase for arm/drive/clear. STOP and newly latched faults advance the epoch, invalidating packets queued before that event. After a fault, inspect the cause, request STATUS and explicitly clear, then separately arm. Never automatically replay a queue or reconnect into motion. A USB session is not network authentication; only a trusted local diagnostic/operator process may own the serial port.

The Pico loop polls rather than blocking on an unfinished line. Its watchdog candidate resets the MCU after a 250ms loop stall; reset behavior and end-to-end stop latency must be measured. PWM pins are blanked before possibly blocking USB responses and initialized low at startup. Keep motor power disconnected while flashing or editing firmware.

## Face controls

Feather input order is D5, D6, D10, D11, D12, A0, A1. Each closes to GND with an internal pull-up. D9 and D13 are avoided because of the board's battery divider and LED. Key outputs are button 1 Enter (PTT toggle), button 2 Space (speech interrupt), button 3 Escape (exit fullscreen), then four serial-event-only buttons. Hold button 7 during power-on to suppress HID keys for diagnostics.

These bindings were inspected in upstream `agent.py`; they act on whichever desktop window has focus. Verify them in a text editor before focusing the agent. Buttons do not control wheels. Herbie's existing browser is not wired to this keyboard or controller by this change.
