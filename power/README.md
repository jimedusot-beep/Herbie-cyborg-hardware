# Power and protection — planning only

**Electrical design is unverified.** A Raspberry Pi must not power motors through GPIO. Different logic and motor power rails may be appropriate, as explained in [Adafruit's Raspberry Pi servo driver guide](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up). Actual voltage domains, current ratings, reference grounding, conductor size and physical interruption must be selected from the *exact* devices and datasheets, not generic tutorials.

Use [POWER_BUDGET_TEMPLATE.csv](POWER_BUDGET_TEMPLATE.csv) to enter idle, operating and **peak/stall current** with sources and units, and [build readiness gates](../integration/BUILD_READINESS_CHECKLIST.md) before first actuation. Blank entries intentionally mean unknown; they are **not zero-current values**.

Keep mains, damaged lithium batteries, and unsupervised actuation outside beginner bench prototyping.

## Conservative screening calculator

Run `python3 tools/power_budget.py` from the repository root. It groups the *summed documented peak or stall currents* by specified voltage rail **only if every row is verified with an exact model and datasheet**. Otherwise it reports the missing evidence and exits without a current estimate. It does not recommend a power supply, fuse, conductor or a safety margin; those require engineering decisions and supervised measurement.

The example input currently has no verified electrical models, so the expected result is **POWER BUDGET INCOMPLETE**.
