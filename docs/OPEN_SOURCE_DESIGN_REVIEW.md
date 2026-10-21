# Open-source robotics design review — reference, not dependency

Reviewed concepts from public open-source and instructional resources (2026-10-21). **No third-party code or schematic is copied into this repository.** Check licenses before adapting any files. Sources do not certify H.E.R.B.I.E. hardware.

| Source | Useful idea | H.E.R.B.I.E. decision |
|---|---|---|
| [ros-controls/ros2_control_demos](https://github.com/ros-controls/ros2_control_demos) | Clear separation of simulation, hardware interfaces, configuration and tests | Adopt interface separation, **not** the ROS 2 runtime for V1 |
| [irfanjamal88/Pan-Tilt-TeleOp](https://github.com/irfanjamal88/Pan-Tilt-TeleOp) | Mock driver, command sequencing, soft limits and watchdog | Keep as research patterns; do not assume its tested limits match our servos |
| [LayerDynamics/pibot](https://github.com/LayerDynamics/pibot) | Distinguish host link watchdog from on-controller watchdog; latched stop | Specify these properties for future controller, not yet implemented |
| [Adafruit servo driver with Raspberry Pi](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up) | Servo load should have appropriately rated external supply; distinguish logic VCC from servo V+ | Capture power domains **after** selecting exact models; never power servo from Pi GPIO |
| [KiCad CLI](https://docs.kicad.org/9.0/en/cli/cli.html) | Repeatable ERC checks | Add once real .kicad_sch files exist; an ERC pass cannot prove electrical safety |
| [sparkengineering/kicad-action](https://github.com/sparkengineering/kicad-action) | ERC/DRC in GitHub Actions | Evaluate only after actual KiCad documents exist |

## Design recommendations

1. **Use simulation-first:** all controllers must start with physical actuation disabled.
2. **Separate interface from transport:** the behavioral UI should not know servo pin numbers.
3. **Specify two independent stop paths:** command/timeout handling is distinct from power-interruption hardware. Browser STOP does not substitute for an actual emergency-stop device.
4. **Decide servo torque with measurements:** weigh the real head assembly and determine the lever arm; do not choose torque from STL size alone.
5. **Validate in steps:** datasheets → power budget → mechanical envelope → unpowered bench review → controlled live tests.

## Open questions

- What exact controller, motor and display models are available and electrically compatible?
- Does each head-axis mechanism rotate the intended mass without collision or cable snag?
- What happens on reboot, USB disconnection, voltage drop and lost command acknowledgements?
- What powers and physically disables servos independently of the web interface?
- Which part of 3D-vision has actual, measured mount hole dimensions?

Read all referenced repositories as **examples of engineering approaches**, not certified designs or authorized hardware instructions.
