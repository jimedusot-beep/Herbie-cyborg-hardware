import csv
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAPPING = ROOT / "integration/cad-electronics-compatibility.json"
BOM = ROOT / "bom/components.csv"
# Known identifiers from the body repository at the time of this integration review.
# These are NOT measurements or a replacement for the mechanical canonical source.
BODY_PART_IDS = {f"HBR-{n:03d}" for n in range(1, 19)}

def validate(data, rows):
    errors = []
    bom_ids = {r["component_id"] for r in rows}
    mapped = set()
    for entry in data["entries"]:
        cid = entry["component_id"]
        if cid in mapped:
            errors.append(f"duplicate component {cid}")
        mapped.add(cid)
        if cid not in bom_ids:
            errors.append(f"unknown component {cid}")
        if entry["mounting_verified"] is not False:
            errors.append(f"unsupported mounting verification {cid}")
        if entry["power_requirements_verified"] is not False:
            errors.append(f"unsupported power verification {cid}")
        if entry["exact_dimensions_mm"] is not None or entry["mass_g"] is not None:
            errors.append(f"unknown measurements should be null: {cid}")
        for part in entry["provisional_cad_parts"]:
            if part not in BODY_PART_IDS:
                errors.append(f"invalid CAD part {part}")
        if not entry["open_measurements"]:
            errors.append(f"no missing measurements listed: {cid}")
    if mapped != bom_ids:
        errors.append("BOM/mapping component ID mismatch")
    if data["status"] != "conceptual-unverified":
        errors.append("mapping must remain unverified until measured")
    return errors

class CompatibilityMappingTests(unittest.TestCase):
    def test_repo_mapping(self):
        data = json.loads(MAPPING.read_text(encoding="utf-8"))
        with BOM.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(data["schema_version"], "0.1.0")
        self.assertEqual(validate(data, rows), [])
    def test_rejects_false_fit(self):
        data = json.loads(MAPPING.read_text(encoding="utf-8"))
        data["entries"][0]["mounting_verified"] = True
        with BOM.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(validate(data, rows))
    def test_rejects_unrecognized_cad_part(self):
        data = json.loads(MAPPING.read_text(encoding="utf-8"))
        data["entries"][0]["provisional_cad_parts"].append("HBR-999")
        with BOM.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(validate(data, rows))
if __name__ == "__main__":
    unittest.main()
