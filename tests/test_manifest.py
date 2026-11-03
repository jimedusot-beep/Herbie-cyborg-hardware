import copy
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate_manifest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ManifestTests(unittest.TestCase):
    def modified_result(self, new_manifest, bom=None):
        with tempfile.TemporaryDirectory() as work:
            root = pathlib.Path(work)
            (root / "integration").mkdir()
            (root / "bom").mkdir()
            (root / "integration/system-manifest.json").write_text(
                json.dumps(new_manifest), encoding="utf-8"
            )
            (root / "bom/components.csv").write_text(
                bom if bom is not None else (ROOT / "bom/components.csv").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            return validate_manifest.validate(root)

    def current_manifest(self):
        return json.loads((ROOT / "integration/system-manifest.json").read_text(encoding="utf-8"))

    def test_manifest_valid(self):
        self.assertEqual(validate_manifest.validate(), [])

    def test_all_interface_ids_in_bom(self):
        data = self.current_manifest()
        self.assertEqual(set(data["hardware_interfaces"]), validate_manifest.REQUIRED_ROLES)

    def test_rejects_missing_bom_reference(self):
        data = self.current_manifest()
        data["hardware_interfaces"]["pan"]["component_id"] = "UNKNOWN-001"
        self.assertTrue(any("non-BOM" in msg for msg in self.modified_result(data)))

    def test_rejects_nonobject_manifest_without_exception(self):
        self.assertIn("manifest must be a JSON object", self.modified_result([]))

    def test_rejects_missing_and_extra_roles(self):
        data = self.current_manifest()
        del data["hardware_interfaces"]["tilt"]
        errors = self.modified_result(data)
        self.assertTrue(any("missing hardware interfaces" in e for e in errors))
        data["hardware_interfaces"]["secret_motor"] = copy.deepcopy(data["hardware_interfaces"]["pan"])
        self.assertTrue(any("unexpected hardware interfaces" in e for e in self.modified_result(data)))

    def test_rejects_malformed_interfaces_and_owners(self):
        for field, invalid in (("repository_owners", []), ("hardware_interfaces", [])):
            with self.subTest(field=field):
                data = self.current_manifest()
                data[field] = invalid
                self.assertTrue(self.modified_result(data))
        data = self.current_manifest()
        data["hardware_interfaces"]["pan"] = []
        self.assertTrue(any("must be an object" in e for e in self.modified_result(data)))

    def test_rejects_unhashable_component_id_without_exception(self):
        data = self.current_manifest()
        data["hardware_interfaces"]["pan"]["component_id"] = ["CTRL-MAIN-001"]
        self.assertTrue(any("non-BOM" in e for e in self.modified_result(data)))

    def test_rejects_missing_or_duplicate_bom_ids(self):
        data = self.current_manifest()
        self.assertTrue(any("component_id column" in e for e in
                            self.modified_result(data, "description,quantity\nController,1\n")))
        bom = (ROOT / "bom/components.csv").read_text(encoding="utf-8")
        duplicate = bom + bom.splitlines()[1] + "\n"
        self.assertTrue(any("duplicate component_id" in e for e in
                            self.modified_result(data, duplicate)))

    def test_rejects_false_actuation_or_fit(self):
        data = self.current_manifest()
        data["motion_enabled"] = True
        data["physical_emergency_stop_verified"] = True
        data["hardware_interfaces"]["tilt"]["physical_fit"] = "verified"
        errors = self.modified_result(data)
        self.assertTrue(any("motion must remain disabled" in e for e in errors))
        self.assertTrue(any("no validated hardware emergency stop" in e for e in errors))
        self.assertTrue(any("must not claim measured physical fit" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
