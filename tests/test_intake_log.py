"""Intake log validators are data-quality checks, NOT proof of physical tests."""
import csv
import pathlib
import tempfile
import unittest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate_intake


class IntakeLogTests(unittest.TestCase):
    def make_csv(self, **kwargs):
        row = dict.fromkeys(validate_intake.REQUIRED, "")
        row.update({
            "intake_id": "INTAKE-001",
            "source_type": "donated",
            "custody_status": "in-hand",
            "description": "FICTIONAL TEST RECORD ONLY",
            "quantity": "1",
            "verification_stage": "uninspected",
        })
        row.update(kwargs)
        with tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8", suffix=".csv", delete=False) as stream:
            writer = csv.DictWriter(stream, fieldnames=validate_intake.REQUIRED)
            writer.writeheader()
            writer.writerow(row)
            return pathlib.Path(stream.name)

    def test_real_log_is_valid_and_empty_until_user_evidence(self):
        self.assertEqual(validate_intake.validate(), [])
        with validate_intake.PATH.open(newline="", encoding="utf-8") as handle:
            self.assertEqual(len(list(csv.DictReader(handle))), 0)

    def test_uninspected_fictional_part_not_passed_off_as_verified(self):
        path = self.make_csv()
        try:
            self.assertEqual(validate_intake.validate(path), [])
        finally:
            path.unlink()

    def test_bench_claim_requires_part_number_and_evidence(self):
        path = self.make_csv(verification_stage="bench-demonstrated")
        try:
            self.assertTrue(any("bench evidence requires" in e for e in validate_intake.validate(path)))
        finally:
            path.unlink()

    def test_datasheet_claim_requires_exact_part_and_link(self):
        path = self.make_csv(verification_stage="datasheet-matched")
        try:
            self.assertTrue(any("datasheet matching requires" in e for e in validate_intake.validate(path)))
        finally:
            path.unlink()

    def test_planned_is_not_a_bench_demonstration(self):
        path = self.make_csv(verification_stage="bench-demonstrated", custody_status="planned",
                             manufacturer_part="FAKE-EXAMPLE", evidence_link="example")
        try:
            self.assertTrue(any("in-hand" in e for e in validate_intake.validate(path)))
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
