# Community and open-source engineering references

These are research resources, **not verified compatible designs**. Check license, exact component model, board revision, electrical limits, and test evidence before adapting anything.

| Resource | What to learn | Caution |
|---|---|---|
| [ROS REP-2004](https://reps.openrobotics.org/rep-2004/) | Versioning, testing, documentation, quality/maturity labels | H.E.R.B.I.E. is not claiming ROS certification or a ROS quality level |
| [KiCad documentation](https://docs.kicad.org/) | Native schematics and electrical rule checking (ERC) | ERC does not prove physical safety or correct component selection |
| [Adafruit Learning System](https://learn.adafruit.com/) | Beginner-friendly electronics and servo guides | Match exact controller logic voltage, servo supply and load |
| [SparkFun tutorials](https://learn.sparkfun.com/) | Power, wiring, connectors and embedded prototyping | Confirm board revisions and pinouts |
| [Arduino Forum](https://forum.arduino.cc/) | Community troubleshooting and motor-controller discussions | Forum advice is not an engineering sign-off |
| [Raspberry Pi forums](https://forums.raspberrypi.com/) | GPIO, power and Pi integration | Never power motors directly from GPIO |
| [ROS Discourse](https://discourse.ros.org/) | Robotics architecture and reproducible integration practices | ROS is optional and may be excessive for V1 |
| [r/robotics](https://www.reddit.com/r/robotics/) | Maker feedback and mechanical/electrical design pitfalls | Verify advice against datasheets and measurements |

## Research workflow
1. Identify one concrete design question, e.g. servo selection for measured head mass.
2. Gather manufacturer datasheets and at least one independent engineering example.
3. Compare voltage, stall current, torque, connector, communication, dimensions and safety.
4. Record citations, licenses, uncertainties and alternatives in an engineering decision record.
5. Prototype with controlled power and document actual test results before marking verified.

Do not scrape or copy third-party designs without checking licensing and attribution.
