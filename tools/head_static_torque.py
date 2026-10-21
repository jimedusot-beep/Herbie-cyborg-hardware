#!/usr/bin/env python3
"""Fail-closed *static tilt gravity moment* screening. NOT servo selection or hardware safety.

Only accepts dated, evidence-referenced *physical* horizontal-tilt observations.
The CSV starts empty by design; no fabricated head measurements are supplied.
A row claiming to be physical is still self-reported, not independently certified.
"""
import csv
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "integration" / "head-load-observations.csv"
G = Decimal("9.80665")
HEADERS = [
    "record_id", "axis", "assembly_revision", "pose_label", "measurement_basis",
    "moving_mass_g", "gravity_lever_arm_mm", "measurement_date", "evidence_reference",
    "notes",
]


def analyze(rows):
    """Return (physical_tilt_results, blockers) for read-only mechanical screening.

    Results contain N*m as Decimal; blockers deliberately preclude a full valid screen.
    """
    results = []
    blockers = []
    if not rows:
        return results, ["No dated physical head measurements recorded."]
    seen = set()
    for line, row in enumerate(rows, 2):
        record = (row.get("record_id") or "").strip()
        if not re.fullmatch(r"HEAD-[0-9]{3,}", record):
            blockers.append(f"line {line}: missing/invalid observation ID")
            continue
        if record in seen:
            blockers.append(f"line {line}: duplicate observation {record}")
            continue
        seen.add(record)

        if row.get("axis") != "tilt_horizontal":
            blockers.append(f"{record}: only horizontal tilt static gravity torque is screenable; pan requires dynamic/friction analysis")
            continue
        if row.get("measurement_basis") != "physical_measurement":
            blockers.append(f"{record}: CAD estimate/unknown is not a physical observation")
            continue
        if not all((row.get(key) or "").strip() for key in
                   ("assembly_revision", "pose_label", "measurement_date", "evidence_reference")):
            blockers.append(f"{record}: missing physical revision, pose, date or evidence reference")
            continue
        try:
            date.fromisoformat(row["measurement_date"])
        except ValueError:
            blockers.append(f"{record}: invalid calendar date")
            continue

        try:
            mass = Decimal((row.get("moving_mass_g") or "").strip())
            lever = Decimal((row.get("gravity_lever_arm_mm") or "").strip())
            if not mass.is_finite() or not lever.is_finite() or mass <= 0 or lever < 0:
                raise ValueError("expected finite positive mass and nonnegative lever arm")
        except (ValueError, InvalidOperation, TypeError):
            blockers.append(f"{record}: invalid or missing mass/lever; unknown is not zero")
            continue

        results.append({
            "record_id": record,
            "assembly_revision": row["assembly_revision"].strip(),
            "pose_label": row["pose_label"].strip(),
            "torque_nm": mass * G * lever / Decimal("1000000"),
        })
    return results, blockers


def screen_file(path=OBSERVATIONS):
    """Check exact CSV schema before computing; cannot validate authenticity of evidence."""
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != HEADERS:
            return [], ["Observation file header differs from expected schema."]
        return analyze(list(reader))


def main():
    results, blockers = screen_file()
    if blockers:
        print("MECHANICAL SCREEN INCOMPLETE — no build-ready torque assessment.")
        for reason in blockers:
            print(" -", reason)
    if results:
        print("STATIC TILT GRAVITY SCREEN ONLY (self-reported measurements, not reviewed):")
        for result in results:
            print(f" - {result['record_id']} {result['pose_label']}: {result['torque_nm']} N*m")
    print("No motor recommendation. Pan inertia/friction, dynamics, continuous duty, "
          "physical fit, power protection and a real motor stop are not verified.")
    return 2 if blockers or not results else 0


if __name__ == "__main__":
    raise SystemExit(main())
