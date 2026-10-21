#!/usr/bin/env python3
"""Validate the provisional H.E.R.B.I.E. electronics inventory (stdlib only)."""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "bom" / "components.csv"
REQUIRED = ("component_id", "description", "manufacturer_part", "quantity", "acquisition_status", "electrical_rating", "mounting_reference", "verification_status")
STATUSES = {"owned-verified", "donated-awaiting-delivery", "requested", "planned", "optional"}
def validate():
    errors = []
    with PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(REQUIRED):
            errors.append("BOM column names/order differ from schema")
        rows = list(reader)
    if not rows:
        errors.append("BOM must not be empty")
    ids = set()
    for line, row in enumerate(rows, 2):
        cid = row.get("component_id") or ""
        if not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+", cid):
            errors.append(f"line {line}: invalid component ID {cid!r}")
        if cid in ids:
            errors.append(f"line {line}: duplicate ID {cid}")
        ids.add(cid)
        if row.get("acquisition_status") not in STATUSES:
            errors.append(f"line {line}: invalid acquisition status")
        try:
            if int(row.get("quantity") or "") < 1:
                raise ValueError
        except ValueError:
            errors.append(f"line {line}: quantity must be positive integer")
        if not row.get("description"):
            errors.append(f"line {line}: description missing")
        if row.get("verification_status") == "verified" and not row.get("manufacturer_part"):
            errors.append(f"line {line}: verified part requires manufacturer model")
    return errors
if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print("ERROR:", problem)
    print(f"BOM validation: {'FAIL' if problems else 'PASS'}")
    sys.exit(bool(problems))
