#!/usr/bin/env python3
"""Validate a provisional integration manifest using the Python standard library."""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
def validate(root=ROOT):
    errors = []
    try:
        manifest = json.loads((root / "integration/system-manifest.json").read_text(encoding="utf-8"))
        with (root / "bom/components.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, ValueError) as exc:
        return [str(exc)]
    ids = {r["component_id"] for r in rows}
    if manifest.get("schema_version") != "0.1.0":
        errors.append("unexpected manifest version")
    if manifest.get("status") != "design-only":
        errors.append("physical readiness must not be assumed")
    if manifest.get("motion_enabled") is not False:
        errors.append("physical motion must remain disabled in this planning manifest")
    if manifest.get("physical_emergency_stop_verified") is not False:
        errors.append("no validated hardware emergency stop is documented")
    urls = manifest.get("repository_owners", {})
    for role in ("brain", "body", "electronics"):
        if not str(urls.get(role, "")).startswith("https://github.com/jimedusot-beep/"):
            errors.append(f"missing owner link for {role}")
    interfaces = manifest.get("hardware_interfaces", {})
    if not interfaces:
        errors.append("no hardware interfaces")
    for role, entry in interfaces.items():
        if entry.get("component_id") not in ids:
            errors.append(f"{role} references non-BOM component")
        if entry.get("physical_fit") != "not-tested":
            errors.append(f"{role} must not claim measured physical fit")
        cad = entry.get("cad_part_id")
        if cad is not None and (not isinstance(cad, str) or not cad.startswith("HBR-")):
            errors.append(f"{role} has invalid CAD ID")
    return errors

if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print("ERROR:", failure)
    print("manifest:", "FAIL" if failures else "PASS")
    sys.exit(bool(failures))
