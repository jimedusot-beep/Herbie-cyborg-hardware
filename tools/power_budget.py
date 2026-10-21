#!/usr/bin/env python3
"""Conservative voltage-rail current screening; NOT a power supply recommendation."""
import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "power" / "POWER_BUDGET_TEMPLATE.csv"

def calculate(rows):
    """Return voltage-rail sums or incomplete-row reasons. All components must be verified."""
    totals = defaultdict(lambda: Decimal("0"))
    incomplete = []
    for row in rows:
        cid = row.get("component_id", "<unknown>")
        required = ("exact_model", "supply_nominal_v", "peak_or_stall_current_a", "datasheet_url")
        if row.get("verified") != "true" or any(not row.get(field) for field in required):
            incomplete.append(f"{cid}: exact datasheet-backed ratings not verified")
            continue
        try:
            volts = Decimal(row["supply_nominal_v"])
            amps = Decimal(row["peak_or_stall_current_a"])
            qty = int(row["quantity"])
            if not volts.is_finite() or not amps.is_finite() or volts <= 0 or amps <= 0 or qty <= 0:
                raise ValueError
        except (ValueError, InvalidOperation, TypeError):
            incomplete.append(f"{cid}: invalid voltage, current or quantity")
            continue
        totals[volts] += amps * qty
    return dict(totals), incomplete

def main():
    with SOURCE.open(newline="", encoding="utf-8") as stream:
        totals, incomplete = calculate(list(csv.DictReader(stream)))
    if incomplete:
        print("POWER BUDGET INCOMPLETE — no validated supply current estimate available.")
        for message in incomplete:
            print("-", message)
        print("Enter exact part numbers and datasheet ratings; never treat blank current as zero.")
        return 2
    for voltage, peak_current in sorted(totals.items()):
        print(f"{voltage} V rail: {peak_current} A summed peak/stall nameplate current")
    print("SCREENING ONLY: verify transient behavior, regulator margins, fusing and measurements separately.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
