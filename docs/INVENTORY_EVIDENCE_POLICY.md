# Inventory evidence and selection gates

The [canonical BOM](../bom/components.csv) currently contains four planned, unverified component IDs. [Candidate research](../bom/researched_candidates.json) does not prove acquisition or compatibility.

## Acquisition states
- `planned`: desired design role; no claim of request or purchase.
- `requested`: outreach actually sent; retain a date and reference.
- `donated-awaiting-delivery`: confirmed offer, not physically received; cite confirmation.
- `owned-verified`: item physically observed, exact manufacturer/model identified; cite a dated inventory record.
- `optional`: future upgrade, not required for V1.

**A model can be physically owned without being electrically validated.** Keep `verification_status` separate. A manufacturer's product listing alone cannot establish what is in hand.

## Evidence ledger
Use [acquisition_evidence.csv](../bom/acquisition_evidence.csv). Never put personal addresses, tracking numbers, contact emails, serial numbers, or receipts with payment details in this public repository. Use a non-sensitive reference such as `private-inventory-photo-2026-10-21` to a private record.

An `owned-verified` BOM row must have a matching `physical-inspection` ledger record with date, exact model and reviewer. A `donated-awaiting-delivery` row requires a matching `donation-confirmation` entry. A `requested` row requires `outreach-confirmation`. Unknown ownership remains planned.

## Selection vs. ownership vs. compatibility
1. **Candidate:** manufacturer-backed product researched; not selected.
2. **Selected:** documented design decision with alternatives, interface compatibility and constraints.
3. **Owned:** independently documented acquisition.
4. **Electrically verified:** selected parts and actual board revisions have checked datasheets and test evidence.
5. **Mechanically verified:** printed/assembled fit, center-of-mass and motion clearances physically measured.
6. **Build-ready:** reviewed KiCad schematic, protective devices, real physical STOP, measured power and supervised test plan.

These are independent states. Do not infer later gates from earlier ones.

## Immediate evidence to gather
Photograph the label (privately) and record exact model/revision of any Pi, controller, servo and display. Measure head mass, center of gravity and lever arms after actual components are assembled. Keep [motor-power readiness checklist](../integration/BUILD_READINESS_CHECKLIST.md) pending until real parts are selected.
