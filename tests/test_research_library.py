"""Static checks of the curated research index; NOT external-link or hardware verification."""
import csv
import unittest
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "RESEARCH_PROJECTS_13_24.csv"
EXPECTED = (
    ("Hackaday", "hackaday.io"),
    ("Hackster", "hackster.io"),
    ("Instructables", "instructables.com"),
    ("Printables", "printables.com"),
    ("GitLab", "gitlab.com"),
    ("Arduino Project Hub", "projecthub.arduino.cc"),
)
ALLOWED_ACCESS = {"primary_page", "indexed_page", "repository_page"}


class ResearchLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with INDEX.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cls.fields = reader.fieldnames
            cls.rows = list(reader)

    def test_schema_and_numbering(self):
        self.assertEqual(
            self.fields,
            ["number", "platform", "title", "url", "lesson",
             "access_evidence", "license_review", "reuse_status"],
        )
        self.assertEqual([int(row["number"]) for row in self.rows], list(range(13, 25)))
        self.assertEqual(len(set(row["url"] for row in self.rows)), 12)

    def test_two_references_per_portal_and_source_domains(self):
        self.assertEqual(
            Counter(row["platform"] for row in self.rows),
            Counter({name: 2 for name, _ in EXPECTED}),
        )
        for index, (platform, domain) in enumerate(EXPECTED):
            for row in self.rows[index * 2:(index + 1) * 2]:
                self.assertEqual(row["platform"], platform)
                parsed = urlparse(row["url"])
                self.assertEqual(parsed.scheme, "https")
                self.assertIn(parsed.hostname, {domain, "www." + domain})

    def test_references_remain_unapproved(self):
        for row in self.rows:
            self.assertTrue(row["title"].strip())
            self.assertTrue(row["lesson"].strip())
            self.assertIn(row["access_evidence"], ALLOWED_ACCESS)
            self.assertTrue(row["license_review"].strip())
            self.assertEqual(row["reuse_status"], "reference_only")


if __name__ == "__main__":
    unittest.main()
