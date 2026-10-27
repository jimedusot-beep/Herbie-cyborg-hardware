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
- [Intake guide](../bom/INTAKE_GUIDE.md) reuses the existing [acquisition-evidence policy](INVENTORY_EVIDENCE_POLICY.md) and ledger without creating a second inventory.

**Decision status:** no electronics ordered, acquired, selected or bench-tested by these documents. No architecture has been approved.

## 2026-10-27: retain Be More Agent as a backup body

Owner request: keep the [Be More Agent-style Pi/screen body](../examples/be-more-agent-backup/README.md) as an alternative, not the primary expressive pan/tilt plan. Option ID `HERBIE-BACKUP-BMA-001`. Prototype CAD and namespaced candidate electronics exist. None establishes ownership, compatibility, physical validation or approval to energize.

Stationary voice/display bring-up precedes any battery or wheel work. The isolated wheel protocol and disabled-output Pico candidate do not resolve or replace the primary robot's pan/tilt protocol. All previous primary architecture decisions remain open. Promotion requires exact hardware measurements, power/stop review and supervised physical evidence.
