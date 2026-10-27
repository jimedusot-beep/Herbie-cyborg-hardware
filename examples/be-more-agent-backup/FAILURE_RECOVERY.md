# Failure and recovery matrix

| Failure or test | Expected behavior / recovery | Evidence still needed |
|---|---|---|
| Display SKU differs from CAD | Stop full printing. Measure and revise aperture, clips and cable route. | Actual dimensions and coupon fit |
| No microphone/speaker audio | Test ALSA device separately; check routing, USB-audio type, volume and foreground window. | Heard playback and recorded speech |
| Enter/Space reaches wrong app | Focus agent window; use ordinary keyboard first. Hold Feather button 7 on boot for HID-off diagnostics. | Correct UI action without wheel commands |
| Model missing or wrong name | Correct installed model/config match; run model alone before full UI. | Local model response and recorded version |
| Internet disappears | Report web-search unavailable. Use only already installed local features. Do not pretend fresh results. | Offline voice test plus honest search error |
| Pi undervoltage/reboot | Open motor cutoff and restore stable regulated power. Controller restart is disarmed. Investigate PSU, USB load and pogo contact. | Voltage log and no-motion restart |
| Host dies / USB unplugged | Command lease expires and latches. No replay/re-arm on reconnect. Physical cutoff remains independent. | Measured output timing and stopping distance |
| Partial/oversized/garbled serial input | Bounded parser rejects and latches; zero output request. | Simulated tests plus Pico input-flood bench |
| Duplicate, old-session or pre-stop command | Reject sequence/session/epoch, remain stopped or faulted. | Unit tests plus controller capture |
| Firmware loop/USB write stalls | Outputs blanked before reply; watchdog candidate resets to disarmed. | Actual PWM reset timing, MCU version |
| Driver fault asserted | Latch zero request; inspect fault cause with cutoff open. CLEAR requires healthy input; ARM is separate. | Measured nFAULT level and stop |
| Bumper pressed | Once fitted/enabled, latch stop. No automatic reverse or retry. | Switch polarity and test capture |
| Motor stall, binding or overheating | Open physical cutoff. Do not keep trying to overcome it in software. Inspect mechanics and resize parts if required. | Loaded current, temperature, torque/clearance review |
| Physical cutoff opened while MCU unhealthy | Interrupt the motor energy path without depending on browser/Linux. Wheels may coast. | Independent circuit review and supervised power test |
| Corrupt config/memory | Keep original files; restore a verified backup into a new directory for inspection. Memory backup is opt-in. | Successful restore comparison |
| App or motion fault cleared | Return to DISARMED. Fix cause, inspect state, then deliberate separate ARM in a future reviewed bench revision. | Recovery tests; no automatic resumed motion |

Keep a private incident record: date, exact part/firmware/source revision, test setup, expected result, observed result, measurements, evidence file/hash and corrective action. Never record a hardware pass from a software simulation. Avoid private addresses, credentials, receipts, serial numbers and conversation memory in the public repository.
