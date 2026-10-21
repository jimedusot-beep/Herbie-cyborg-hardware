import pathlib
import tempfile
import unittest
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate_bom

class InventoryTests(unittest.TestCase):
    def test_repository_inventory(self):
        self.assertEqual(validate_bom.validate(), [])

    def test_expected_component_ids(self):
        data = (pathlib.Path(__file__).resolve().parents[1] / "bom/components.csv").read_text()
        self.assertIn("SERVO-HEAD-PAN-001", data)
        self.assertIn("SERVO-HEAD-TILT-001", data)

if __name__ == "__main__":
    unittest.main()
