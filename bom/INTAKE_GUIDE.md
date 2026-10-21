# Inventory intake: owned, donated, salvaged and refurbished parts

**Current known physical inventory: none independently confirmed.** The [intake log](intake-log.csv) contains a header and zero rows, deliberately. The authoritative [candidate BOM](components.csv) remains independent: four rows represent planned *roles*, not objects on a desk.

## What each row means

Record an intake row **only from actual owner-supplied evidence**; do not infer that a part is owned from a tutorial, photo of someone else's project, candidate controller or CAD model.

- **intake_id:** unique `INTAKE-001` etc., distinct from the functional BOM component ID.
- **source_type:** `unconfirmed`, `owned`, `donated`, `salvaged`, `refurbished`, `purchased`. This is origin, *not* an endorsement or request to buy.
- **custody_status:** `planned`, `requested`, `in-hand`, `quarantined`, `retired`. "In hand" means possession only.
- **description, manufacturer_part, revision, quantity, condition:** describe precisely; unknown values remain blank or explicitly unknown.
- **verification_stage:** `uninspected`, `visual-inspected`, `datasheet-matched`, `unpowered-checked`, `bench-demonstrated`. Stages are distinct observations, not system-level approval.
- **datasheet_url:** primary manufacturer's documentation, only when verified for the exact model and revision.
- **evidence_link:** a safe, accessible review note describing the observation or test. No personal addresses, serial numbers, passwords, Wi-Fi credentials, identifying photos or purchase account information.
- **bom_component_id:** optional link to a candidate role from `components.csv`, assigned **after** compatibility review; no duplicate second bill of materials.
- **notes:** risks, faults, missing docs, not a claim of physical safety.

## Safe intake sequence — do not energize

1. Confirm whether the part is physically in hand, in transit or merely proposed. Label any claim as user-reported until checked.
2. Inspect without power for damage, swelling, corrosion, loose pins and exposed conductors. Record concerns; **quarantine suspicious batteries, chargers and mains supplies**. Do not probe or recharge damaged lithium cells.
3. Find the exact manufacturer's part number and datasheet. A similar-looking servo or breakout is not a reliable substitute.
4. Compare voltage, current (including startup/stall), signal levels, connectors, firmware versions and dimensions against H.E.R.B.I.E.'s undecided requirements.
5. For future supervised work, design an unpowered inspection checklist and current-limited bench plan with independent motor power interruption. A board working once is not an approved motor safety system.
6. Cross-reference the authoritative BOM only after role compatibility and reviewer agreement. Preserve uncertainty.

A completed `bench-demonstrated` entry **requires real physical evidence and an exact model**, but still does **not** imply all system safety gates pass. The [intake validator](../tests/validate_intake.py) catches missing/invalid status fields; it cannot prove that a claimed test occurred.

## Recording a review example without pretending to own parts

In a pull request or scratch note, describe a **fictional practice record** explicitly as fictional. Do **not** insert fabricated owned/verified parts into the real CSV. For early learning use the [research library](../docs/RESEARCH_LIBRARY.md).

Related: [power calculations](../power/README.md), [build-readiness gates](../integration/BUILD_READINESS_CHECKLIST.md), [controller options](../controllers/ARCHITECTURE_OPTIONS.md).
