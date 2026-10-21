# Engineering decisions (ADRs)

Use one record per major decision: problem, requirements, options considered, source links, chosen design, tradeoffs, compatibility checks, safety review, and test evidence. Initial pending decisions:

1. Pi-only versus Pi + ESP32/Arduino motion control.
2. Exact pan/tilt servo models after measuring head mass and lever arms.
3. Separate regulated logic and motor power domains.
4. Physical motor-power interruption and emergency-stop strategy.
5. Stable versioned controller command protocol.

All remain **open**, not approved or physically validated.

## Evaluation workspace (still pending)

- [Controller architecture comparison](../controllers/ARCHITECTURE_OPTIONS.md) compares Pi + PCA9685, Pi + ESP32 and MCU-only strategies without a selected model.
- [Controller decision worksheet](../controllers/DECISION_WORKSHEET.md) lists missing measurements and approval gates.
- [Safety requirements V0](../integration/SAFETY_REQUIREMENTS_V0.md) defines review targets, not an implemented stop system.
- [Intake log](../bom/INTAKE_GUIDE.md) supports donated/salvaged/owned part records while preserving the authoritative candidate BOM.

**Decision status:** no electronics ordered, acquired, selected or bench-tested by these documents. No architecture has been approved.
