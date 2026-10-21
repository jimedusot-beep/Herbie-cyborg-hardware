import copy
import json
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate_manifest

class ManifestTests(unittest.TestCase):
    def test_manifest_valid(self):
        self.assertEqual(validate_manifest.validate(), [])
    def test_all_interface_ids_in_bom(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        data = json.loads((root / "integration/system-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(data["hardware_interfaces"]), {"pan", "tilt", "main_controller", "face_display"})
    def test_rejects_missing_bom_reference(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        self.assertNotIn("UNKNOWN-001", (root / "bom/components.csv").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
