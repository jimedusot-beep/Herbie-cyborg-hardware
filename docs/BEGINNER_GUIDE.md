# H.E.R.B.I.E. beginner robotics guide

Three connected notebooks, **not three competing implementations**:

- **Brain:** [Herbie](https://github.com/jimedusot-beep/Herbie) owns AI, facial expression and simulated motion.
- **Nervous system:** [Herbie-cyborg-hardware](https://github.com/jimedusot-beep/Herbie-cyborg-hardware) owns controller research, component records, electrical diagrams, power and hardware tests.
- **Body:** [3D Vision](https://github.com/jimedusot-beep/3D-vision) owns the 3D models, prints, mounts and mechanical assembly.

Their links do not make electronics work automatically. **No motor, controller, wiring or safety mechanism is verified as built yet.** Our first lessons are reading, sorting and simulation, not energized servo control.

## Five useful concepts

- **Microcontroller (e.g. ESP32):** a small computer often used for sensors, motor-control signals and local response to failures. Precise board capabilities must be checked.
- **Single-board computer (e.g. Raspberry Pi):** a computer suited to larger software tasks such as vision and conversation. A Pi GPIO is not a motor power supply.
- **Servo:** an actuator that attempts to reach a commanded position. Torque, range, current and voltage vary by exact model; never assume generic 0–180-degree motion is mechanically safe.
- **Power rail:** a supply with a documented voltage and current capacity. A logic rail and a motor rail may need separate protection and correctly engineered reference grounding.
- **Watchdog versus STOP:** a watchdog detects communication/computer failure; a simulated/browser STOP requests software behavior. Neither substitutes for a verified physical motor-power interruption.

## Safe learning exercises (no actuation)

1. **Read the map:** open [the integration manifest](../integration/system-manifest.json). Find `motion_enabled` and `physical_emergency_stop_verified`; both must remain `false` while unverified.
2. **Classify evidence:** open [the BOM](../bom/components.csv). For each candidate, identify whether it is planned, owned, tested or unspecified. A blank part number means **not selected**.
3. **Learn from examples:** choose #13, #15 or #16 in the [numbered library](RESEARCH_LIBRARY.md). Write a five-sentence summary of one idea, an electrical/mechanical risk, and the evidence still missing.
4. **Model a failure:** on paper or in the existing Herbie *software simulator*, describe the expected response to lost communication, reboot and a duplicate movement command. Do not attach a motor. Compare the two incompatible [simulated motion protocols](MOTION_PROTOCOL_COMPARISON.md).
5. **Explore the body:** inspect [3D Vision's provisional parts](https://github.com/jimedusot-beep/3D-vision/blob/main/HERBIE_V1/PARTS.csv). Sketch where a pan/tilt axis might fit, labeling all dimensions and loads as **unknown until measured**.

## When you receive donated or salvaged parts

Do not plug them in just to see whether they work. First record the part's label, exact model/revision, visible damage or corrosion, connector shape, expected voltage and a manufacturer datasheet (if available). Keep unknown power supplies, loose lithium cells, swollen batteries, exposed mains equipment and visibly damaged devices out of beginner energized testing. Add a candidate to the BOM only with an honest acquisition/verification status, and ask for a safe controlled inspection plan before energizing.

## What comes before first motion?

Start with the [build-readiness checklist](../integration/BUILD_READINESS_CHECKLIST.md): exact selected parts, reviewed schematic, measured mass/geometry, sourced worst-case current figures, limits and fault behavior, independent motor-power interruption and supervised bench evidence. No existing illustration or outside tutorial meets these gates on H.E.R.B.I.E.'s behalf.

**Next lesson:** compare Raspberry Pi-only and Pi + ESP32 control based on actual head requirements, *without purchasing or wiring either yet*.
