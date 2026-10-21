import csv
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOM = ROOT / "bom/components.csv"
BUDGET = ROOT / "power/POWER_BUDGET_TEMPLATE.csv"

class PowerBudgetTests(unittest.TestCase):
    def test_budget_matches_bom_ids(self):
        with BOM.open(newline="", encoding="utf-8") as f:
            components = {r["component_id"]: r for r in csv.DictReader(f)}
        with BUDGET.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), len({r["component_id"] for r in rows}), "duplicate budget component ID")
        self.assertEqual(set(components), {r["component_id"] for r in rows}, "budget and BOM differ")
        for row in rows:
            with self.subTest(component=row["component_id"]):
                self.assertEqual(int(row["quantity"]), int(components[row["component_id"]]["quantity"]))
                self.assertIn(row["verified"], {"true", "false"})
                self.assertIn(row["measurement_or_estimate"], {"unknown", "datasheet", "measured"})
                for key in ("supply_nominal_v", "idle_current_a", "operating_current_a", "peak_or_stall_current_a"):
                    value = row[key]
                    if value:
                        self.assertGreater(float(value), 0.0)
                if row["verified"] == "true":
                    self.assertTrue(row["exact_model"] and row["datasheet_url"])
                    self.assertTrue(all(row[k] for k in ("supply_nominal_v", "operating_current_a", "peak_or_stall_current_a")))
                    self.assertNotEqual(row["measurement_or_estimate"], "unknown")
                if not row["exact_model"]:
                    self.assertEqual(row["verified"], "false", "unselected models cannot be verified")

if __name__ == "__main__":
    unittest.main()
