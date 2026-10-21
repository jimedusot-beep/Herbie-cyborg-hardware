# Engineering decisions (ADRs)

Use one record per major decision: problem, requirements, options considered, source links, chosen design, tradeoffs, compatibility checks, safety review, and test evidence. Initial pending decisions:

1. Pi-only versus Pi + ESP32/Arduino motion control.
2. Exact pan/tilt servo models after measuring head mass and lever arms.
3. Separate regulated logic and motor power domains.
4. Physical motor-power interruption and emergency-stop strategy.
5. Stable versioned controller command protocol.

All remain **open**, not approved or physically validated.
