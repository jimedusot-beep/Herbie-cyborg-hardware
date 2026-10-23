"""Validate the McGruber learning-case snapshot and its unverified 3D models.

Standard library only. This does not certify fit, printability or electrical safety.
"""
import csv
import json
import subprocess
import sys
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "mcgruber-light-beam-tripwire"


def load_obj(name):
    vertices = []
    faces = []
    names = []
    first_by_part = {}
    current = None
    for line in (CASE / "models" / name).read_text(encoding="utf-8").splitlines():
        if line.startswith("o "):
            current = line[2:].strip()
            names.append(current)
        elif line.startswith("v "):
            coords = tuple(float(x) for x in line[2:].split())
            if len(coords) != 3 or not all(map(math.isfinite, coords)):
                raise ValueError("Invalid vertex in " + name)
            vertices.append(coords)
            first_by_part.setdefault(current, coords)
        elif line.startswith("f "):
            indices = tuple(int(s) for s in line[2:].split())
            if len(indices) != 3 or not all(0 < i <= len(vertices) for i in indices):
                raise ValueError("Invalid triangle in " + name)
            faces.append(indices)
    return names, first_by_part, vertices, faces


class TripwireLearningCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((CASE / "assembly_manifest.json").read_text(encoding="utf-8"))

    def test_provenance_and_provisional_claims(self):
        m = self.manifest
        self.assertEqual(m["case_study_id"], "MCG-TW-P01-CONCEPT-001")
        self.assertEqual(m["status"], "DIGITAL_CONCEPT_UNTESTED")
        self.assertEqual(m["model"]["units"], "illustrative-mm")
        self.assertEqual(m["model"]["up_axis"], "Y")
        self.assertEqual(m["provenance"]["sync_mode"], "manual-reviewed-copy")
        self.assertIn("/project-mcgruber", m["provenance"]["canonical_repo"])
        self.assertEqual(len(m["provenance"]["original_source_blob_sha"]), 40)
        self.assertEqual(len(m["provenance"]["diagram_source_blob_sha"]), 40)
        self.assertTrue(m["open_measurements"])
        for key in ("physical_dimensions_verified", "electrical_schematic_verified",
                    "hardware_tested", "fit_verified"):
            self.assertIs(m["model"][key], False, key)
        self.assertIs(m["model"]["no_hardware_control"], True)

    def test_part_ids_and_exploded_offsets(self):
        parts = self.manifest["parts"]
        self.assertEqual(len(parts), 13)
        self.assertEqual(len({p["id"] for p in parts}), 13)
        self.assertEqual({p["side"] for p in parts}, {"emitter", "receiver", "control"})
        for p in parts:
            self.assertRegex(p["id"], r"^TW-(E|R|C)-[A-Z0-9]+$")
            self.assertIs(p["fit_verified"], False)
            self.assertIsNone(p["dimensions_measured_mm"])
            for key in ("position_illustrative_mm", "explode_offset_illustrative_mm"):
                self.assertEqual(len(p[key]), 3)
                self.assertTrue(all(isinstance(x, (int, float)) and math.isfinite(x) for x in p[key]))
            self.assertTrue(p["function"])
            self.assertTrue(p["verification_needed"])
            self.assertIn(p["required"], (True, False, "conditional"))

    def test_3d_obj_models_have_separate_valid_parts_and_expected_displacements(self):
        assembled = load_obj("assembled.obj")
        exploded = load_obj("exploded.obj")
        ids = [p["id"] for p in self.manifest["parts"]]
        self.assertEqual(assembled[0], ids)
        self.assertEqual(exploded[0], ids)
        self.assertEqual(len(assembled[2]), len(exploded[2]))
        self.assertEqual(len(assembled[3]), len(exploded[3]))
        self.assertGreater(len(assembled[3]), 500)
        self.assertLess(len(assembled[3]), 10000)
        for p in self.manifest["parts"]:
            a = assembled[1][p["id"]]
            b = exploded[1][p["id"]]
            for axis in range(3):
                self.assertAlmostEqual(
                    b[axis] - a[axis],
                    p["explode_offset_illustrative_mm"][axis],
                    delta=0.0003,
                    msg=p["id"],
                )

    def test_stl_previews_contain_corresponding_triangle_meshes(self):
        obj_faces = len(load_obj("assembled.obj")[3])
        for name in ("assembled.stl", "exploded.stl"):
            text = (CASE / "models" / name).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("solid McGruberTripwireConcept\n"))
            self.assertTrue(text.rstrip().endswith("endsolid McGruberTripwireConcept"))
            self.assertEqual(text.count("facet normal "), obj_faces)
            self.assertEqual(text.count("vertex "), obj_faces * 3)
            self.assertEqual(text.count("endfacet"), obj_faces)

    def test_measurement_template_contains_only_real_part_ids_without_invented_observations(self):
        with (CASE / "measurement_intake_template.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        ids = [p["id"] for p in self.manifest["parts"]]
        self.assertEqual([row["part_id"] for row in rows], ids)
        self.assertEqual([row["component"] for row in rows],
                         [p["name"] for p in self.manifest["parts"]])
        observed = [
            "donor_item_or_purchase", "exact_part_or_revision", "acquisition_evidence",
            "width_mm", "height_mm", "depth_mm", "diameter_mm", "mount_holes_mm",
            "voltage_v", "current_ma", "sensor_beam_present", "sensor_beam_blocked",
            "instrument", "test_date", "evidence_reference", "notes",
        ]
        for row in rows:
            for field in observed:
                self.assertEqual(row[field], "", (row["part_id"], field))
            self.assertIn(row["need"], ("required", "optional", "conditional"))

    def test_reproducible_concept_geometry_and_part_transform_contract(self):
        result = subprocess.run(
            [sys.executable, str(CASE / "regenerate_models.py"), "--check"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertIn("physical fit unverified", result.stdout)
        self.assertIn("1044 illustrative triangles", result.stdout)

    def test_diagrams_are_valid_svg_and_not_executable(self):
        for filename in ("exploded-assembly.svg", "signal-flow.svg"):
            data = (CASE / "diagrams" / filename).read_text(encoding="utf-8")
            root = ET.fromstring(data)
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            self.assertNotIn("<script", data.lower())
            self.assertNotIn("javascript:", data.lower())
            self.assertNotIn("onload=", data.lower())


if __name__ == "__main__":
    unittest.main()
