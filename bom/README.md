# Bill of materials

`components.csv` is a **planning inventory**, not proof of ownership or compatibility. Replace blank manufacturer part numbers only after selection. Status values: `owned-verified`, `donated-awaiting-delivery`, `requested`, `planned`, `optional`. Maintain exact voltage/current ratings, dimensions, and supplier evidence when known. Do not duplicate the authoritative BOM in the other repositories.

## Intake versus authoritative BOM

The [intake log](intake-log.csv) and [guide](INTAKE_GUIDE.md) describe physical items as reported/observed and their evidence. The intake log starts with **no entries** because ownership or receipt has not been confirmed. It is *not* the BOM and does not select a system architecture. A reviewed part can be linked to a BOM component ID only after its exact identity, electrical limits and intended role have been assessed. Never convert an item to `owned-verified` merely because it was donated or powered on once.
