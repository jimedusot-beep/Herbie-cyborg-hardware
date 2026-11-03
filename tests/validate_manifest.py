#!/usr/bin/env python3
"""Validate the design-only integration manifest; never authorize physical motion."""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_ROLES = {"pan", "tilt", "main_controller", "face_display"}


def validate(root=ROOT):
    errors = []
    try:
        manifest = json.loads((root / "integration/system-manifest.json").read_text(encoding="utf-8"))
        with (root / "bom/components.csv").open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames
            rows = list(reader)
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        return [f"could not read integration inputs: {exc}"]

    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]
    if not headers or "component_id" not in headers:
        errors.append("BOM missing component_id column")
        return errors
    if not rows:
        errors.append("BOM must include at least one component")

    ids = set()
    for line, row in enumerate(rows, start=2):
        cid = row.get("component_id")
        if not isinstance(cid, str) or not cid.strip():
            errors.append(f"BOM line {line}: invalid component_id")
            continue
        if cid in ids:
            errors.append(f"BOM line {line}: duplicate component_id {cid}")
        ids.add(cid)

    if manifest.get("schema_version") != "0.1.0":
        errors.append("unexpected manifest version")
    if manifest.get("status") != "design-only":
        errors.append("physical readiness must not be assumed")
    if manifest.get("motion_enabled") is not False:
        errors.append("physical motion must remain disabled in this planning manifest")
    if manifest.get("physical_emergency_stop_verified") is not False:
        errors.append("no validated hardware emergency stop is documented")

    urls = manifest.get("repository_owners")
    if not isinstance(urls, dict):
        errors.append("repository_owners must be an object")
    else:
        for role in ("brain", "body", "electronics"):
            url = urls.get(role)
            if not isinstance(url, str) or not url.startswith("https://github.com/jimedusot-beep/"):
                errors.append(f"missing owner link for {role}")

    interfaces = manifest.get("hardware_interfaces")
    if not isinstance(interfaces, dict):
        errors.append("hardware_interfaces must be an object")
        return errors
    missing = REQUIRED_ROLES - set(interfaces)
    unexpected = set(interfaces) - REQUIRED_ROLES
    if missing:
        errors.append("missing hardware interfaces: " + ", ".join(sorted(missing)))
    if unexpected:
        errors.append("unexpected hardware interfaces: " + ", ".join(sorted(unexpected)))

    for role, entry in interfaces.items():
        if not isinstance(entry, dict):
            errors.append(f"{role}: interface entry must be an object")
            continue
        component_id = entry.get("component_id")
        if not isinstance(component_id, str) or component_id not in ids:
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
