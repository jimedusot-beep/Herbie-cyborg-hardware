# Herbie backup option: Be More Agent body

**Option ID: HERBIE-BACKUP-BMA-001. Status: backup-only, prototype, physically unverified.** Recorded at the owner's request on 2026-10-27. It does not replace the expressive pan/tilt concept, canonical four-role BOM or current 3D-vision body. The existing integration manifest keeps `motion_enabled=false`.

This fallback uses a Pi 5, screen face, USB audio, camera and local AI, inspired by [brenpoly's Be More Agent](https://github.com/brenpoly/be-more-agent) and [build video](https://youtu.be/l5ggH-YhuAw). Start as a plugged-in stationary companion. A separate Pico 2 / DRV8833 wheel base is a later prototype, not an upstream feature. No walking or powered arms are supplied.

The owner's Rev A export contains the 18-page drawing book, STEP assembly/explosion, 13 custom-part types, prototype STLs and six flat DXFs. Those approximate purchased-component envelopes are not verified manufacturer CAD. The private Herbie project register links the personal export. This example holds candidate electronics, wiring and reliability work; it does not claim the geometry is Herbie's canonical Body design.

## Start here

1. Read [commissioning](COMMISSIONING.md) and [failure/recovery notes](FAILURE_RECOVERY.md).
2. Inspect [candidate catalog](candidate_catalog.json), [interface/protocol](INTERFACE.md) and the three [module wiring sheets](schematics/). Catalog entries are namespaced `BMA-*`, candidate-only and not evidence of ownership. Do not merge them into `bom/components.csv` as acquired parts.
3. Run `python3 bench_console.py --demo`. It uses no GPIO or serial port. Run `python3 preflight.py` for read-only software/audio-device diagnostics. Add `--check-local-ollama` only when you want a bounded loopback GET.
4. Copy `build_record.template.json` to ignored `local-build-record.json`. Record real measurements and private evidence. `python3 readiness.py local-build-record.json` reports missing records; blank fields and checked boxes alone never pass. A complete format does not certify hardware or enable outputs.
5. Study [Pico candidate firmware](pico_main.py) and [Feather button sketch](feather_buttons/feather_buttons.ino). Physical wheel output is disabled in source. Arduino compilation, Pico execution and physical timing still need hardware/toolchain checks.

## Reliability work supplied

- Boot disarmed; strict fields, boot session, stop/fault epoch and increasing sequence checks.
- Bounded duty requests and slew, a zero-output step on reversal, short command leases, latched faults, explicit clear-then-arm and no automatic reconnect/re-arm.
- Bounded input framing, malformed/flooded packet rejection, driver-fault input and optional bumper inputs.
- A 250ms MicroPython watchdog candidate, output blanking before USB writes and zeroing on exit. Board reset/PWM behavior remains a physical test.
- Diagnostic host console: real serial mode can send only STATUS or STOP. There is no internet listener, LLM-to-wheel adapter or background motion service.
- Debounced Feather controls: Enter, Space and Escape match current upstream desktop bindings. Remaining buttons only emit serial events. Desktop focus matters; these are not motor controls or an emergency stop.
- Local configuration backup and restore to a new directory. Conversation memory is included only with `--include-memory`. No live-file overwrite or automatic startup occurs.

The wheels can coast after PWM or power is removed. Neither this controller nor the web STOP replaces an independently reviewed physical motor-power cutoff. No test here proves printed strength, battery suitability, payload, speed, stopping distance or physical safety.

## Validation

From the repository root: `python3 -m unittest discover -s tests -p 'test_*.py' -v`, `python3 tests/validate_bom.py`, and `python3 tests/validate_manifest.py`. The existing workflow discovers the new tests. Tests cover digital behavior with simulated time; physical gates remain pending.

The implementation is independently written. No donor Python code, face assets, voice model or STL files are redistributed. Sources and the inspected upstream commit are recorded in `option.json`. Keep private receipts, addresses, serial numbers, memory and bench evidence out of public commits.
