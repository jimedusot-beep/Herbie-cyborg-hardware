# Intake and assessment guide — one evidence ledger

**Current known physically confirmed inventory: none.** Do not invent rows in the existing [acquisition evidence CSV](acquisition_evidence.csv). H.E.R.B.I.E. already has an [acquisition evidence policy](../docs/INVENTORY_EVIDENCE_POLICY.md) and the single [canonical BOM](components.csv). This guide explains decisions *before* applying that policy; it does **not** establish a second log, new status enum, or competing source of truth.

## Three different kinds of record

1. **Research candidate** — exact manufacturer-supported option in [researched_candidates.json](researched_candidates.json). `owned: false` means no ownership evidence. Do not interpret that file as an acquisition ledger.
2. **Functional BOM component** — `components.csv` holds intended roles (pan servo, tilt servo, main controller, face display), currently `planned` and `unverified`.
3. **Acquisition evidence** — `acquisition_evidence.csv` supports only the evidence types and model/status requirements defined in [the policy](../docs/INVENTORY_EVIDENCE_POLICY.md), tested by [the existing unit tests](../tests/test_acquisition_evidence.py). Do not claim possession from a web listing or a donated-part offer.

## Intake workflow without motor power

- **Describe the claimed part:** user-reported source (already owned, donated, salvage, refurbished), whether in hand, exact package label, model and board revision *if observable*. No shipment or personal information in this public repository.
- **Observe physical condition only with power disconnected:** corrosion, damaged insulation, loose contacts, swollen batteries, exposed mains wiring, missing markings. Quarantine suspicious batteries, chargers, loose cells and potentially energized mains items. Never charge damaged lithium batteries or try unknown supplies as a first test.
- **Compare manufacturer evidence:** identify a primary datasheet; record voltage range, logic threshold, idle/operating/stall current, connector polarity, pinout, revision and dimensions. Leave fields unknown when uncertain.
- **Distinguish identity from function:** a photographed label may support an ownership check but **not** electrical verification, successful movement or a validated safety mechanism.
- **Record evidence in the existing ledger:** only when a relevant functional BOM ID exists; comply with `physical-inspection`, `donation-confirmation`, or `outreach-confirmation` requirements. For a spare or unrelated donated device with no decided role, first document a non-sensitive candidate note or review issue rather than fabricating a BOM component match.
- **Advance only after review:** proposed bench tests require exact part numbers, unpowered continuity/polarity inspections, appropriate rated/current-limited supplies, independently reviewed motor-power interruption, and supervised testing. Do not energize based on this guide.

## Examples of truthful status language

- **Candidate:** "A Raspberry Pi model was researched; none was confirmed received."
- **Offered donation:** "Owner reported an offer; model and delivery status pending evidence."
- **In hand:** "Owner reported a board in hand; exact revision and electrical behavior not tested."
- **Tested:** only after a dated, reproducible bench record on the exact part. A single software or browser simulator test never establishes a physical demonstration.

## Current safety boundary

The [integration manifest](../integration/system-manifest.json) remains `motion_enabled: false` and `physical_emergency_stop_verified: false`. Even an item marked `owned-verified` in the existing BOM is *only* evidenced as physically identified under the policy, not safe to energize.

Related work: [controller architecture comparison](../controllers/ARCHITECTURE_OPTIONS.md), [build readiness](../integration/BUILD_READINESS_CHECKLIST.md), [separate physical safety requirements](../integration/SAFETY_REQUIREMENTS_V0.md).
