import csv
import pathlib
import unittest
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOM = ROOT / "bom/components.csv"
EVIDENCE = ROOT / "bom/acquisition_evidence.csv"
HEADERS = ["component_id","evidence_type","evidence_reference","observed_date","exact_model","reviewed_by","notes"]
REQUIRED = {"owned-verified":"physical-inspection","donated-awaiting-delivery":"donation-confirmation","requested":"outreach-confirmation"}

def validate(rows, evidence):
    errors = []
    ids = {r["component_id"] for r in rows}
    for e in evidence:
        if e["component_id"] not in ids:
            errors.append("evidence references unknown component")
        if e["evidence_type"] not in set(REQUIRED.values()):
            errors.append("invalid evidence type")
        for field in ("evidence_reference", "observed_date", "reviewed_by"):
            if not e[field].strip():
                errors.append("evidence missing " + field)
        try:
            date.fromisoformat(e["observed_date"])
        except ValueError:
            errors.append("invalid evidence date")
        if e["evidence_type"] == "physical-inspection" and not e["exact_model"].strip():
            errors.append("physical inspection missing exact model")
    for r in rows:
        expected = REQUIRED.get(r["acquisition_status"])
        if expected and not any(e["component_id"] == r["component_id"] and e["evidence_type"] == expected and (expected != "physical-inspection" or e["exact_model"] == r["manufacturer_part"]) for e in evidence):
            errors.append("unsupported acquisition status: " + r["component_id"])
    return errors

class EvidenceTests(unittest.TestCase):
    def test_repository_evidence(self):
        with BOM.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        with EVIDENCE.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assertEqual(reader.fieldnames, HEADERS)
            evidence = list(reader)
        self.assertEqual(validate(rows,evidence),[])
    def test_rejects_unsubstantiated_ownership(self):
        rows = [{"component_id":"CTRL-MAIN-001","acquisition_status":"owned-verified","manufacturer_part":"Pi 4B"}]
        self.assertTrue(validate(rows,[]))
    def test_rejects_mismatched_model(self):
        rows = [{"component_id":"CTRL-MAIN-001","acquisition_status":"owned-verified","manufacturer_part":"Pi 4B"}]
        evidence = [{"component_id":"CTRL-MAIN-001","evidence_type":"physical-inspection","evidence_reference":"private-record","observed_date":"2026-10-21","exact_model":"Other board","reviewed_by":"owner","notes":""}]
        self.assertTrue(validate(rows,evidence))
    def test_rejects_undated_donation(self):
        rows = [{"component_id":"SERVO-HEAD-PAN-001","acquisition_status":"donated-awaiting-delivery","manufacturer_part":""}]
        evidence = [{"component_id":"SERVO-HEAD-PAN-001","evidence_type":"donation-confirmation","evidence_reference":"private-record","observed_date":"","exact_model":"","reviewed_by":"owner","notes":""}]
        self.assertTrue(validate(rows,evidence))

if __name__ == "__main__":
    unittest.main()
