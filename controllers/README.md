# Controller research — no board selected

H.E.R.B.I.E.'s AI software is in [Herbie](https://github.com/jimedusot-beep/Herbie); this repository owns the future electrical controller, wiring and physical tests.

- [Compare architecture options](ARCHITECTURE_OPTIONS.md): Raspberry Pi + dedicated PWM driver, Raspberry Pi + ESP32, or MCU-only experimental controller.
- [Decision worksheet](DECISION_WORKSHEET.md): measurements and criteria before selection.
- [Safety requirements](../integration/SAFETY_REQUIREMENTS_V0.md): required behavior, not implemented.
- [Motion protocol comparison](../docs/MOTION_PROTOCOL_COMPARISON.md): two incompatible simulated formats; **neither** is a physical control protocol.

Even if a Raspberry Pi 4B or ESP32 is discussed as a candidate, **no actual model, servo, power source or motor-control link is approved**. Every physical motion path stays disabled.
