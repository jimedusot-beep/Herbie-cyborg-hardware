#!/usr/bin/env python3
"""Audit self-reported optical tripwire trials; never verifies hardware safety.

This tool neither connects to electronics nor checks ADC wiring or voltage.
An exit-code 0 means only the supplied trial log passed the specified checks.
"""
import csv
import json
import math
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIALS = ROOT / "examples/mcgruber-light-beam-tripwire/beam_trial_template.csv"
COLUMNS = (
    "trial_id", "ambient_light", "expected_beam", "reported_state",
    "sensor_reading", "test_date", "evidence_reference", "notes",
)
AMBIENT = ("dim", "normal", "bright")
EXPECTED = ("clear", "blocked")
OBSERVED = ("clear", "alarm", "disconnected")
MIN_PER_CONDITION = 5


def analyze(rows):
    """Return deterministic validation and trial statistics for supplied records.

    Never treats the CSV contents as verified physical readings. External
    reviewer must inspect evidence references and equipment independently.
    """
    errors = []
    counts = Counter()
    seen_ids = set()
    false_alarms = missed_beams = disconnected = 0
    accepted = 0

    for line, row in enumerate(rows, start=2):
        if not isinstance(row, dict):
            errors.append(f"line {line}: malformed trial record")
            continue
        fields = {name: (row.get(name) or "").strip() for name in COLUMNS}
        trial_id = fields["trial_id"]
        if not trial_id:
            errors.append(f"line {line}: missing trial ID")
            continue
        if trial_id in seen_ids:
            errors.append(f"line {line}: duplicate trial ID {trial_id}")
            continue
        seen_ids.add(trial_id)
        if fields["ambient_light"] not in AMBIENT:
            errors.append(f"line {line}: invalid ambient_light")
            continue
        if fields["expected_beam"] not in EXPECTED:
            errors.append(f"line {line}: invalid expected_beam")
            continue
        if fields["reported_state"] not in OBSERVED:
            errors.append(f"line {line}: invalid reported_state")
            continue
        if not fields["evidence_reference"]:
            errors.append(f"line {line}: missing evidence_reference")
            continue
        try:
            date.fromisoformat(fields["test_date"])
        except ValueError:
            errors.append(f"line {line}: invalid test_date")
            continue
        if fields["reported_state"] != "disconnected":
            try:
                raw = float(fields["sensor_reading"])
                if not math.isfinite(raw) or raw < 0:
                    raise ValueError
            except ValueError:
                errors.append(f"line {line}: sensor_reading must be nonnegative and finite")
                continue
        elif fields["sensor_reading"]:
            try:
                raw = float(fields["sensor_reading"])
                if not math.isfinite(raw) or raw < 0:
                    raise ValueError
            except ValueError:
                errors.append(f"line {line}: invalid disconnected sensor_reading")
                continue

        accepted += 1
        counts[(fields["ambient_light"], fields["expected_beam"])] += 1
        if fields["reported_state"] == "disconnected":
            disconnected += 1
        elif fields["expected_beam"] == "clear" and fields["reported_state"] == "alarm":
            false_alarms += 1
        elif fields["expected_beam"] == "blocked" and fields["reported_state"] == "clear":
            missed_beams += 1

    coverage_gaps = [
        f"{ambient}/{expected}: {counts[(ambient, expected)]}/{MIN_PER_CONDITION} trials"
        for ambient in AMBIENT for expected in EXPECTED
        if counts[(ambient, expected)] < MIN_PER_CONDITION
    ]
    return {
        "scope": "Self-reported trial-log screening only; not electrical/physical verification",
        "valid_trial_count": accepted,
        "required_min_trials": MIN_PER_CONDITION * len(AMBIENT) * len(EXPECTED),
        "false_alarms": false_alarms,
        "missed_beams": missed_beams,
        "disconnected_trials": disconnected,
        "coverage_gaps": coverage_gaps,
        "input_errors": errors,
        "coverage_complete": not errors and not coverage_gaps,
        "physical_hardware_verified": False,
    }


def run(path=TRIALS):
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != list(COLUMNS):
                print(json.dumps({"error": "CSV header mismatch", "expected_columns": COLUMNS}))
                return 2
            report = analyze(list(reader))
    except (OSError, UnicodeError, csv.Error) as exc:
        print(json.dumps({"error": f"could not read trial log: {exc}"}))
        return 2
    print(json.dumps(report, indent=2))
    if not report["coverage_complete"]:
        return 2
    if report["false_alarms"] or report["missed_beams"] or report["disconnected_trials"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run(Path(sys.argv[1]) if len(sys.argv) > 1 else TRIALS))
