#!/usr/bin/env python3
"""Validate provenance and status claims in the empty-by-default intake log.

A passing check does not verify possession, ownership, tests, or safe electronics.
"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "bom" / "intake-log.csv"
REQUIRED = (
    "intake_id", "source_type", "custody_status", "description",
    "manufacturer_part", "revision", "quantity", "condition",
    "verification_stage", "datasheet_url", "evidence_link",
    "bom_component_id", "notes",
)
SOURCE_TYPES = {"unconfirmed", "owned", "donated", "salvaged", "refurbished", "purchased"}
CUSTODY = {"planned", "requested", "in-hand", "quarantined", "retired"}
STAGES = {"uninspected", "visual-inspected", "datasheet-matched",
          "unpowered-checked", "bench-demonstrated"}


def validate(path=PATH):
    errors = []
    with pathlib.Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(REQUIRED):
            return ["intake log header differs from schema"]
        rows = list(reader)
    ids = set()
    for row_num, row in enumerate(rows, 2):
        key = row.get("intake_id") or ""
        if not re.fullmatch(r"INTAKE-[0-9]{3,}", key):
            errors.append(f"line {row_num}: invalid intake ID")
        if key in ids:
            errors.append(f"line {row_num}: duplicate intake ID")
        ids.add(key)
        if row.get("source_type") not in SOURCE_TYPES:
            errors.append(f"line {row_num}: invalid source type")
        if row.get("custody_status") not in CUSTODY:
            errors.append(f"line {row_num}: invalid custody status")
        if row.get("verification_stage") not in STAGES:
            errors.append(f"line {row_num}: invalid verification stage")
        if not (row.get("description") or "").strip():
            errors.append(f"line {row_num}: description required")
        try:
            if int(row.get("quantity") or "") < 1:
                raise ValueError()
        except ValueError:
            errors.append(f"line {row_num}: positive integer quantity required")
        if row.get("verification_stage") == "bench-demonstrated":
            if row.get("custody_status") != "in-hand":
                errors.append(f"line {row_num}: bench evidence requires in-hand status")
            if not (row.get("manufacturer_part") or "").strip() or not (row.get("evidence_link") or "").strip():
                errors.append(f"line {row_num}: bench evidence requires exact part and test reference")
        if row.get("verification_stage") == "datasheet-matched":
            if not (row.get("manufacturer_part") or "").strip() or not (row.get("datasheet_url") or "").strip():
                errors.append(f"line {row_num}: datasheet matching requires exact part and datasheet")
    return errors


if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print("ERROR:", problem)
    print(f"Intake log: {'FAIL' if problems else 'PASS'} (not physical verification)")
    sys.exit(bool(problems))
