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

## Replit, STEAM and maker community workflow

- [Replit Git/GitHub version control](https://docs.replit.com/replit-workspace/workspace-features/version-control): Replit can import GitHub projects and work with branches, but a Replit workspace is **not** the source of truth. Prefer branch + PR against the three existing repositories, with no automatic overwriting of `main`. Two similarly named Replit Herbie apps were found; their synchronization and code state have **not been independently confirmed**. Do not merge or publish either based on name alone.
- [ROS 2 simulation interface documentation](https://docs.ros.org/en/ros2_packages/jazzy/api/gazebo_ros2_control/generated/classgazebo__ros2__control_1_1GazeboSystemInterface.html): distinguishes simulated systems from physical hardware interfaces. Adopt the **conceptual boundary** without adding ROS 2 or Gazebo as a required dependency for a beginner's first prototype.
- [KiCad community schematic discussion](https://forum.kicad.info/t/i-need-help-configuring-symbols-to-satisfy-the-electrical-rules-checker/65486): share the complete KiCad project when seeking review, not just a screenshot. Community members explicitly warn that ERC catches schematic connection mistakes, **not circuit-design faults**.
- [KiCad community Git design-diff discussion](https://forum.kicad.info/t/kicad-with-some-basic-git-version-comparisons/67362): compare changes between schematic revisions and gate ERC/DRC when real circuit/PCB files exist; do not pretend there are meaningful KiCad tests for empty placeholders.

### Education-first contribution ladder

1. **Observe:** read the project map, label unknown parts and take notes; no circuit changes.
2. **Model:** create a simulated expression, movement or CAD joint; include a test and identify its limits.
3. **Measure:** log part numbers, dimensions and datasheets, distinguishing estimates from physical readings.
4. **Review:** propose a small GitHub PR with evidence and explain the change in plain English.
5. **Build:** only after a separately reviewed schematic, power budget, physical stop plan and supervised bench checklist.

### Where to ask for help

- GitHub issues in this repository: focused reviews with exact parts, expected vs. actual behavior and links.
- [KiCad community forum](https://forum.kicad.info/): schematic symbol/ERC interpretation and review after actual KiCad files exist.
- [Arduino Forum](https://forum.arduino.cc/): beginner-friendly servo control and power/grounding discussions; verify advice against manufacturer datasheets.
- [Raspberry Pi forums](https://forums.raspberrypi.com/): GPIO electrical limitations and controller interface questions.
- [Adafruit learning community](https://forums.adafruit.com/): board-specific guidance if an Adafruit driver is selected.
- [Hackaday.io](https://hackaday.io/): documented prototype build logs, failures and peer feedback.

**Participation status:** These are research and recommended community channels. Apart from the [public GitHub feedback issue #2](https://github.com/jimedusot-beep/Herbie-cyborg-hardware/issues/2), no post, answer, endorsement or design review is claimed on these third-party forums.

### Contributor question template

Provide: goal; selected model/revision; source datasheet; actual measured voltage/current/dimensions (or `unknown`); the smallest schematic or code example; what you tried; expected result; actual result; exact fault message; and the specific decision you want reviewed. Remove account details, credentials and identifying photos.
