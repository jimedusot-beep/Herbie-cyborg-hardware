import json
import pathlib
import unittest
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "bom" / "researched_candidates.json"

class ResearchCandidateTests(unittest.TestCase):
    def test_candidate_catalog_is_research_only(self):
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "0.1.0")
        self.assertEqual(data["purpose"], "research-only")
        self.assertIs(data["physical_compatibility_verified"], False)
        self.assertIs(data["ownership_confirmed"], False)
        items = data["candidates"]
        self.assertGreaterEqual(len(items), 6)
        ids = [item["id"] for item in items]
        self.assertEqual(len(ids), len(set(ids)))
        for item in items:
            with self.subTest(id=item["id"]):
                for key in ("id", "category", "model", "voltage", "interface", "source", "notes"):
                    self.assertTrue(item[key], f"{item['id']} missing {key}")
                self.assertEqual(item["decision"], "candidate")
                self.assertIs(item["owned"], False)
                parsed = urlparse(item["source"])
                self.assertEqual(parsed.scheme, "https")
                self.assertTrue(parsed.netloc)
    def test_serial_smart_servos_not_described_as_rc_pwm(self):
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
        for item in data["candidates"]:
            if item["category"] == "smart-servo":
                self.assertIn("serial", item["interface"].lower())
                self.assertIn("not a direct", item["interface"].lower())
    def test_sources_are_manufacturer_or_primary(self):
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
        trusted = ("raspberrypi.com", "adafruit.com", "pololu.com", "espressif.com", "robotis.us", "robotis.com")
        for item in data["candidates"]:
            domain = urlparse(item["source"]).hostname or ""
            self.assertTrue(any(domain == d or domain.endswith("." + d) for d in trusted), domain)

if __name__ == "__main__":
    unittest.main()
