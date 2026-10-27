# Build in stages

No software package can guarantee a failure-free physical build. This procedure makes uncertainties visible before later stages depend on them. Record a failed check as a failure and keep its evidence; do not change it to pass because CI is green.

## 1. Confirm the exact parts before ordering or printing

Record each SKU/revision and its datasheet. Especially measure the Freenove display outside size, active area, holes and cable exits; the Rev A 125x84x12mm envelope is an assumption. Measure switch height and camera mounting pattern. Print one clip, one cap and one screw-boss coupon first. The major CAD dimensions are not proof of fit.

Use the stationary Pi/screen/audio subset first. Leave the NVMe stack, battery pack and wheels out until each is needed. Select genuine cells and have the current X1203/X12-A1 battery, charging, connector-polarity and protection requirements reviewed against their datasheets. Do not substitute a series battery pack. A generic USB-powered analog speaker may need an audio adapter; prefer a real Linux USB-audio device.

## 2. Bring up the stationary software

- Start with a current-compatible 64-bit Raspberry Pi desktop installation and the official supply. Review the exact installed OS/Python versions and display instructions.
- Review Be More Agent at the recorded upstream commit. Review its installer before running it. Follow its current dependency instructions in a dedicated environment; this package does not auto-run a remote installer or claim a locked complete dependency environment.
- Run `preflight.py`; list the actual recording and playback devices. First play and hear a tone, then record and hear speech. A device enumeration alone is not an audio pass.
- Install and test the chosen local model in Ollama before starting the full UI. Make the pulled model names match the agent configuration. Test Piper and Whisper separately, then the whole voice loop. Model response latency on the chosen Pi is unmeasured.
- Fit the correct Pi 5 camera/display cables with power off. Test camera frames and the screen separately before closing the shell.
- Test Enter PTT and Space interrupt using a normal keyboard. Only then flash/fit the Feather sketch and check the same keys with the intended window focused. Actual Arduino compilation and board behavior are outstanding hardware/toolchain tests.
- Repeat at least five whole voice interactions, then restart the application and reboot the Pi. Record audible output and errors. Internet search requires internet; cached local conversation does not prove every feature is offline.

## 3. Mechanical/electrical dry fit

Follow the drawing book's assembly order. Check the selected display/camera, cable bend radii, battery retention, motor brackets, wheel gap, cooler airflow, board insulation and access to the physical cutoff. Use the X1203 supplied stack hardware to verify pogo-pin compression, not the illustrative CAD Z levels.

Weigh the complete assembly and measure balance. The current 1.5kg drive estimate is an assumption, not a payload rating. Review power domains, worst-case starting/stall currents, fuse behavior, wire/connector ratings and stop circuit with appropriate electronics expertise. The supplied KiCad module diagrams are not a board-level design or an independently reviewed safety circuit. Keep the motor positive lead disconnected until this review is complete.

## 4. Logic-only controller candidate

Run the host unit tests and `bench_console.py --demo`. Both are no-hardware exercises. For a later reviewed Pico bench, disconnect motor power, install the board-appropriate MicroPython image, and copy `controller_core.py` plus `pico_main.py` renamed to `main.py`. It ships with physical output disabled. The serial console's real-device mode sends only STATUS and STOP and performs no automatic reconnect.

Record actual firmware/interpreter versions, no-motion boot/reset behavior, driver fault polarity, rejected malformed frames, input flooding and command expiry using suitable instruments. Python syntax or simulated tests do not qualify the Pico runtime or pin timings. The host and MCU watchdogs are behavior layers, not physical energy interruption.

## 5. Reviewed wheel bench and floor test - still pending

Physical output can only become a future supervised bench decision after the mechanical/electrical checks above. No command in the supplied host console enables it, and the main Herbie manifest stays disabled. Do not change that main manifest to bypass a missing measurement.

For an eventual approved bench revision, lift the wheels, keep a physical motor-power cutoff immediately accessible, verify driver outputs at zero first, and start with short bounded commands. Measure actual current, direction, stop latency, reset behavior and load. Stop on binding, excess current, heating, unstable power or any unexpected movement. A disconnected motor can coast; record stopping distance as well as electrical interruption.

Only after that stage passes should an operator try a clear, level indoor floor at a measured low speed. The 0.15m/s target in Rev A is not enforced by an uncalibrated PWM percentage. No stairs, edge-following, carpet, autonomous following, unattended motion, arms or walking are covered by this release.

## 6. Record recovery before closing the project

Create a private config backup with `backup_state.py create`. Include memory only by explicit opt-in. Restore into a new directory and compare hashes; do not overwrite the only working installation. Keep the previous SD image as a separate, manually verified recovery method. Capture a bill of software versions (`python3 --version`, OS release, `pip freeze`, Ollama/model identifiers and the chosen source commit) from the actual Pi.

The evidence template remains pending until real observations exist. `readiness.py` checks completeness and hashes, not truth, competence, electrical safety or certification. It never writes firmware flags or arms motors.
