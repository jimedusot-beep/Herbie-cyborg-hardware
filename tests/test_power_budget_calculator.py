import pathlib
import sys
import unittest
from decimal import Decimal
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import power_budget

class PowerCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.valid = {
            "component_id": "MOTOR-001", "exact_model": "FictionalModel",
            "supply_nominal_v": "6", "peak_or_stall_current_a": "0.8",
            "datasheet_url": "https://example.org/datasheet", "verified": "true",
            "quantity": "2",
        }

    def test_groups_by_voltage_and_multiplies_quantity(self):
        rail, incomplete = power_budget.calculate([self.valid])
        self.assertEqual(incomplete, [])
        self.assertEqual(rail, {Decimal("6"): Decimal("1.6")})

    def test_unknown_values_cannot_be_treated_as_zero(self):
        row = dict(self.valid, peak_or_stall_current_a="", verified="false")
        rail, incomplete = power_budget.calculate([row])
        self.assertEqual(rail, {})
        self.assertEqual(len(incomplete), 1)

    def test_invalid_quantity_and_negative_current_rejected(self):
        for row in (dict(self.valid, quantity="0"), dict(self.valid, peak_or_stall_current_a="-1")):
            with self.subTest(row=row):
                rail, incomplete = power_budget.calculate([row])
                self.assertEqual(rail, {})
                self.assertTrue(incomplete)

if __name__ == "__main__":
    unittest.main()
