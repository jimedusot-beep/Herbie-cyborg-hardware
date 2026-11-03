"""Synthetic-only tests; no physical sensor readings in this repository."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from tripwire_bench_audit import AMBIENT, COLUMNS, EXPECTED, analyze, run


def synthetic_trials():
    return [
        {
            "trial_id": f"synthetic-{ambient}-{beam}-{n}",
            "ambient_light": ambient,
            "expected_beam": beam,
            "reported_state": "alarm" if beam == "blocked" else "clear",
            "sensor_reading": "123",
            "test_date": "2026-11-02",
            "evidence_reference": "SYNTHETIC-UNIT-TEST-NOT-HARDWARE",
            "notes": "",
        }
        for ambient in AMBIENT for beam in EXPECTED for n in range(5)
    ]


class TripwireBenchAuditTests(unittest.TestCase):
    def test_header_only_template_is_incomplete(self):
        report = analyze([])
        self.assertFalse(report["coverage_complete"])
        self.assertEqual(len(report["coverage_gaps"]), 6)
        self.assertFalse(report["physical_hardware_verified"])

    def test_synthetic_perfect_coverage_is_not_physical_verification(self):
        report = analyze(synthetic_trials())
        self.assertTrue(report["coverage_complete"])
        self.assertEqual(report["valid_trial_count"], 30)
        self.assertEqual(report["false_alarms"], 0)
        self.assertEqual(report["missed_beams"], 0)
        self.assertFalse(report["physical_hardware_verified"])

    def test_false_alarm_missed_detection_and_disconnected_counted(self):
        rows = synthetic_trials()
        rows[0]["reported_state"] = "alarm"  # expected clear
        blocked = next(row for row in rows if row["expected_beam"] == "blocked")
        blocked["reported_state"] = "clear"
        rows[2]["reported_state"] = "disconnected"
        rows[2]["sensor_reading"] = ""
        report = analyze(rows)
        self.assertTrue(report["coverage_complete"])
        self.assertEqual(report["false_alarms"], 1)
        self.assertEqual(report["missed_beams"], 1)
        self.assertEqual(report["disconnected_trials"], 1)

    def test_rejects_duplicates_missing_evidence_and_invalid_sensor(self):
        rows = synthetic_trials()
        rows[1]["trial_id"] = rows[0]["trial_id"]
        rows[2]["evidence_reference"] = ""
        rows[3]["sensor_reading"] = "nan"
        rows[4]["sensor_reading"] = "-0.2"
        report = analyze(rows)
        self.assertEqual(len(report["input_errors"]), 4)
        self.assertFalse(report["coverage_complete"])

    def test_rejects_malformed_row_and_invalid_enums(self):
        rows = [None, dict(synthetic_trials()[0])]
        rows[1]["ambient_light"] = "daylight-ish"
        report = analyze(rows)
        self.assertEqual(len(report["input_errors"]), 2)

    def test_cli_rejects_header_only_and_detected_errors(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "trials.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                csv.DictWriter(handle, fieldnames=COLUMNS).writeheader()
            self.assertEqual(run(path), 2)
            rows = synthetic_trials()
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            self.assertEqual(run(path), 0)
            rows[0]["reported_state"] = "alarm"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            self.assertEqual(run(path), 1)


if __name__ == "__main__":
    unittest.main()
