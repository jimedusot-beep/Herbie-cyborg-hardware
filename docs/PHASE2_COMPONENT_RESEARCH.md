# Phase 2 — Datasheet-backed electronics options (research only)

**2026-10-21. No hardware selected, purchased, physically measured or wired by this review.** Canonical planned component IDs remain in [bom/components.csv](../bom/components.csv); researched products are **not** BOM ownership entries. [Machine-readable candidates](../bom/researched_candidates.json) is an independent comparison of options, not an alternate inventory.

## Recommended decision sequence

**For the first simple two-axis prototype:** compare a Raspberry Pi 4B host with a PCA9685 RC servo driver **or** a Pololu Micro Maestro 6, plus two appropriately sized *standard positional RC servos*. Both options require a separate appropriately rated motor supply, mechanical checks and a physically independent way to remove motor power. Do not use GPIO as a motor power output.

**For more sophisticated feedback:** compare two DYNAMIXEL XL330-M288-T or XC330-M288-T units. These are smart **TTL serial** servos, not drop-in substitutes for RC PWM servos on a PCA9685/Maestro. They need a compatible serial interface, correct power and different mechanical mounts.

**For more local control:** an ESP32-S3 can implement a dedicated motor-control layer, but that increases firmware/testing work. A microcontroller by itself does not guarantee watchdogs, safe movement limits or emergency-stop behavior.

## Datasheet findings

| Candidate | Evidence | Key constraints | Open issue |
| --- | --- | --- | --- |
| Raspberry Pi 4 Model B | [Official brief](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-product-brief.pdf) | 5 V DC, minimum 3 A input; 40-pin GPIO | Verify actual unit, accessories and logic power budget; no direct motor drive |
| Adafruit PCA9685 board | [Adafruit pinout](https://learn.adafruit.com/16-channel-pwm-servo-driver/pinouts) and [Pi wiring guide](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up) | I²C, 16 PWM channels; VCC logic separate from servo V+ | No inherent position feedback or autonomous watchdog; OE disables signals, not power |
| Pololu Micro Maestro 6 | [Manufacturer guide](https://www.pololu.com/docs/0J40/all) | 6 channels; USB/TTL; separate servo supply supported | Validate loss-of-link behavior, mechanical envelope, compatibility and host software |
| ESP32-S3 | [Espressif datasheet](https://documentation.espressif.com/esp32_s3_datasheet_en.pdf) | Chip rails typically 3.3 V; board-specific input varies | Exact dev board, firmware and watchdog design undecided |
| ROBOTIS XL330-M288-T | [ROBOTIS specs](https://robotis.us/products/dynamixel-xl330-m288-t) | 3.7–6.0 V; 5 V stall 0.52 N·m/1.47 A; 20×34×26 mm, 18 g | TTL serial interface, physical mount, rated/continuous torque |
| ROBOTIS XC330-M288-T | [ROBOTIS specs](https://docs.robotis.com/docs/dxl/model_reference/x_series/xc_series/xc330-m288/) | 3.7–6.0 V; 5 V stall 0.93 N·m/1.80 A; 20×34×26 mm, 23 g | Same interface/mount questions; greater stall current |

**Do not combine incompatible protocols:** PCA9685 and Maestro generate conventional RC servo pulses. DYNAMIXEL TTL devices require their own serial bus protocol. Do not assume electrical interchangeability because all products are called “servo controllers”.

## Why we are not picking a servo yet

We still need the actual head mass, center of gravity, axis lever arms, travel range, duty cycle, motion speed, collision clearances, mounting geometry and safe sustained torque. Manufacturer **stall** ratings describe short-term limits and cannot be used as continuous operating ratings. The existing CAD parts are preliminary and not physically measured.

For a worst-case static gravity load, `tau = m * 9.81 * r` N·m (mass in kg, perpendicular lever arm in m); this does not cover acceleration, bearing friction, gear fatigue or continuous operation. **The pan and tilt axes may have different load conditions.**

## Power and failure safety

- Motor power is separate from Raspberry Pi GPIO; select supply voltage/current from the exact actuator and measure loaded startup/peak behavior.
- Where logic and actuator circuits exchange non-isolated signals, establish an appropriate shared signal reference/ground per board manufacturer documentation. This does not mean connecting unlike positive supply rails.
- I²C output enable or a browser STOP **does not remove motor power**. Independently design, review and test a physical motor-power interruption method.
- Consider fuse selection, reverse-polarity protection, cable routing, local watchdog, reboot behavior and stale-command rejection only after actual components are chosen.

## Selection gates

1. Confirm physical inventory with exact labels/photos, no assumptions.
2. Record head mass and mounting dimensions, or label CAD estimates clearly.
3. Compare two candidate architectures with torque and power calculations.
4. Select specific servo/controller/supply models and authoritative pinouts.
5. Draft KiCad schematic and run ERC; peer review is still required.
6. Perform unpowered checks, then supervised low-voltage bench testing with independent motor interruption.

## Community reference projects

- [ROS 2 control demos](https://github.com/ros-controls/ros2_control_demos) demonstrate separation of simulated and physical interfaces; **do not add ROS 2 as a dependency yet**.
- [Adafruit Learning System](https://learn.adafruit.com/16-channel-pwm-servo-driver/hooking-it-up) explains servo supply separation.
- [Pololu Maestro documentation](https://www.pololu.com/docs/0J40/all) gives examples of serial control and speed limiting.
- [ROBOTIS e-Manual](https://docs.robotis.com/) documents smart actuator protocols and measurements.

See [community review issue #2](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/issues/2). None of these communities has approved the H.E.R.B.I.E. electrical design.
