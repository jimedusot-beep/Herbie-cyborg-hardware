# Controller choice: evidence and review worksheet

**Decision:** OPEN. No selected controller, no purchased/owned verified device, no physical bench evidence.

| Question | Required evidence | Current status |
|---|---|---|
| Are any Pi/ESP32/driver boards actually in hand? | [Acquisition evidence ledger](../bom/acquisition_evidence.csv) and [policy](../docs/INVENTORY_EVIDENCE_POLICY.md) with exact markings/revision | **Unknown** |
| Which face/AI tasks must run locally? | [Herbie software](https://github.com/jimedusot-beep/Herbie) runtime requirements and benchmarks | **Not measured for target board** |
| What is head mass/torque/travel requirement? | Measured CAD assembly mass, CG, lever arms, clearances from [3D Vision](https://github.com/jimedusot-beep/3D-vision) | **Unknown** |
| What two servo models fit and meet duty cycle? | Exact manufacturer datasheets and tests | **Unknown** |
| What supplies and protection are needed? | [Power worksheet](../power/POWER_BUDGET_TEMPLATE.csv) with worst-case current evidence | **Incomplete** |
| What communications link and protocol version? | Hardware-specific spec, lost-link tests and approvals | **Open** |
| How are faults and physical power interruption handled? | Reviewed schematic, [safety requirements](../integration/SAFETY_REQUIREMENTS_V0.md), supervised test | **Not designed or demonstrated** |
| What does recovery do after STOP/reset? | Simulated tests ensuring recovery never unexpectedly moves motors | **Undecided** |
| What is the cost or donation availability? | Actual supplier/source evidence; no assumed prices | **Unknown** |

## Decision gates

- **Gate 1:** collect real available-part and body requirements.
- **Gate 2:** compare Option A and B with datasheets, fault handling and an independent power-disable plan.
- **Gate 3:** select an architecture in a documented ADR reviewed by the project owner.
- **Gate 4:** create and review KiCad schematics, then controlled bench tests with motor power initially absent.
- **Gate 5:** physical actuation requires passing [build-readiness gates](../integration/BUILD_READINESS_CHECKLIST.md); software simulation success alone does not satisfy them.

No gate checked by creating this worksheet.
