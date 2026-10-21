"""Deterministic offline tests of a static gravity formula; no hardware is exercised."""
import csv
import pathlib
import sys
import tempfile
import unittest
from decimal import Decimal

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import head_static_torque as torque


class HeadStaticTorqueTests(unittest.TestCase):
    def fictional_example(self, **changes):
        """Fictional physics numbers, never a statement about H.E.R.B.I.E.'s head."""
        row = {
            "record_id": "HEAD-001",
            "axis": "tilt_horizontal",
            "assembly_revision": "FICTIONAL-TEST",
            "pose_label": "example-only",
            "measurement_basis": "physical_measurement",
            "moving_mass_g": "500",
            "gravity_lever_arm_mm": "40",
            "measurement_date": "2026-10-21",
            "evidence_reference": "FICTIONAL UNIT TEST — NOT PHYSICAL EVIDENCE",
            "notes": "fictional math fixture",
        }
        row.update(changes)
        return row

    def test_repository_measurement_file_is_header_only(self):
        with torque.OBSERVATIONS.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, torque.HEADERS)
            self.assertEqual(list(reader), [])
        self.assertEqual(torque.screen_file()[0], [])
        self.assertTrue(torque.screen_file()[1])

    def test_math_example_is_correct_but_not_a_rating(self):
        results, blockers = torque.analyze([self.fictional_example()])
        self.assertEqual(blockers, [])
        self.assertEqual(results[0]["torque_nm"], Decimal("0.196133000"))

    def test_rejects_cad_estimate_as_physical_evidence(self):
        results, blockers = torque.analyze(
            [self.fictional_example(measurement_basis="cad_estimate")])
        self.assertEqual(results, [])
        self.assertTrue(any("not a physical" in b for b in blockers))

    def test_missing_measurement_is_not_zero(self):
        for row_change in (
            {"moving_mass_g": ""},
            {"gravity_lever_arm_mm": ""},
            {"moving_mass_g": "NaN"},
            {"gravity_lever_arm_mm": "Infinity"},
            {"moving_mass_g": "-20"},
            {"gravity_lever_arm_mm": "-1"},
        ):
            with self.subTest(change=row_change):
                self.assertTrue(torque.analyze([self.fictional_example(**row_change)])[1])

    def test_zero_lever_is_math_zero_but_not_a_safety_pass(self):
        results, blockers = torque.analyze(
            [self.fictional_example(gravity_lever_arm_mm="0")])
        self.assertEqual(blockers, [])
        self.assertEqual(results[0]["torque_nm"], Decimal("0E-11"))

    def test_pan_not_misrepresented_by_a_zero_gravity_result(self):
        results, blockers = torque.analyze(
            [self.fictional_example(axis="pan_vertical")])
        self.assertEqual(results, [])
        self.assertTrue(any("pan requires" in b for b in blockers))

    def test_rejects_duplicate_ids_and_missing_evidence(self):
        a = self.fictional_example()
        self.assertTrue(any("duplicate" in b for b in torque.analyze([a, a])[1]))
        self.assertTrue(torque.analyze([self.fictional_example(evidence_reference="")])[1])

    def test_rejects_invalid_date_and_missing_revision(self):
        self.assertTrue(torque.analyze([self.fictional_example(measurement_date="2026-02-30")])[1])
        self.assertTrue(torque.analyze([self.fictional_example(assembly_revision="")])[1])

    def test_rejects_wrong_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "observations.csv"
            path.write_text("mass_g,torque_nm\n500,0\n", encoding="utf-8")
            self.assertTrue(torque.screen_file(path)[1])


if __name__ == "__main__":
    unittest.main()
