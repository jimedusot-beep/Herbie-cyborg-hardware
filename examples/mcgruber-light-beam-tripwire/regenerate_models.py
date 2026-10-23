#!/usr/bin/env python3
"""Rebuild/check illustrative McGruber tripwire OBJ/STL presentation assets.

The 13-part assembled.obj is the canonical *illustrative* triangle geometry
for this snapshot; assembly_manifest.json supplies part-ID explosion offsets.
Nothing here infers physical dimensions or converts concept CAD to print-ready.
Only Python's standard library is needed.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FACE_LIMIT = 100_000


def read_obj(path: Path):
    """Return part IDs, triangle vertices and the source OBJ lines.

    The checked-in OBJ is deliberately non-indexed (three fresh vertices per
    triangle), making regeneration transparent and fully deterministic.
    """
    vertices = []
    triangles = []
    parts = []
    lines = path.read_text(encoding="utf-8").splitlines()
    part_id = None
    for line in lines:
        if line.startswith("o "):
            part_id = line[2:].strip()
            if not part_id or part_id in parts:
                raise ValueError("Invalid or duplicate part object")
            parts.append(part_id)
        elif line.startswith("v "):
            if not part_id:
                raise ValueError("Vertex without object group")
            values = tuple(float(value) for value in line[2:].split())
            if len(values) != 3 or not all(math.isfinite(v) for v in values):
                raise ValueError("Non-finite or invalid OBJ vertex")
            vertices.append((part_id, values))
        elif line.startswith("f "):
            if not part_id:
                raise ValueError("Face without object group")
            indices = tuple(int(v) for v in line[2:].split())
            if len(indices) != 3 or indices != tuple(range(len(vertices)-2, len(vertices)+1)):
                raise ValueError("Expecting sequential non-indexed triangles")
            if not all(vertices[i-1][0] == part_id for i in indices):
                raise ValueError("Triangle crosses part groups")
            triangles.append((part_id, tuple(vertices[i-1][1] for i in indices)))
            if len(triangles) > FACE_LIMIT:
                raise ValueError("Excessive mesh triangle count")
        elif line and not line.startswith("#"):
            raise ValueError("Unexpected OBJ record: " + line[:50])
    if not parts or len(triangles) < len(parts):
        raise ValueError("Empty model")
    return parts, vertices, triangles


def move_triangles(triangles, offsets):
    return [(name, tuple(
        tuple(v[i] + offsets[name][i] for i in range(3)) for v in face
    )) for name, face in triangles]


def fmt(value):
    return f"{value:.4f}"


def obj_contents(parts, triangles, exploded):
    by_group = {part: [] for part in parts}
    for part, face in triangles:
        by_group[part].append(face)
    out = ["# McGruber tripwire 13-part UNMEASURED teaching model",
           "# units are illustrative-mm, Y up; NEVER use for fabrication"]
    index = 1
    for part in parts:
        out.append("o " + part)
        for face in by_group[part]:
            for vertex in face:
                out.append("v " + " ".join(fmt(v) for v in vertex))
            out.append(f"f {index} {index + 1} {index + 2}")
            index += 3
    return "\n".join(out) + "\n"


def unit_normal(face):
    a, b, c = face
    u = [b[i]-a[i] for i in range(3)]
    v = [c[i]-a[i] for i in range(3)]
    cross = (u[1]*v[2]-u[2]*v[1],
             u[2]*v[0]-u[0]*v[2],
             u[0]*v[1]-u[1]*v[0])
    n = math.sqrt(sum(x*x for x in cross))
    return tuple(x / n for x in cross) if n > 1e-12 else (0.0, 0.0, 0.0)


def stl_contents(triangles):
    out = ["solid McGruberTripwireConcept"]
    for _part, face in triangles:
        out.append("  facet normal " + " ".join(fmt(x) for x in unit_normal(face)))
        out.append("    outer loop")
        out.extend("      vertex " + " ".join(fmt(x) for x in vertex) for vertex in face)
        out.extend(("    endloop", "  endfacet"))
    out.append("endsolid McGruberTripwireConcept")
    return "\n".join(out) + "\n"


def stl_vertices(path):
    vertices = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("vertex "):
            vals = tuple(float(x) for x in line.strip().split()[1:])
            if len(vals) != 3 or not all(map(math.isfinite, vals)):
                raise ValueError("Non-finite or invalid STL coordinate")
            vertices.append(vals)
    return vertices


def verify(close_tol=0.00015):
    manifest = json.loads((ROOT / "assembly_manifest.json").read_text(encoding="utf-8"))
    parts = manifest["parts"]
    part_ids = [p["id"] for p in parts]
    if len(part_ids) != 13 or len(set(part_ids)) != 13:
        raise ValueError("Manifest must contain 13 unique part IDs")
    if manifest["status"] != "DIGITAL_CONCEPT_UNTESTED" or manifest["model"]["fit_verified"] is not False:
        raise ValueError("Cannot call these geometry files measured or verified")
    offsets = {p["id"]: tuple(p["explode_offset_illustrative_mm"]) for p in parts}
    ordered, _vertices, assembled = read_obj(ROOT / "models/assembled.obj")
    if ordered != part_ids:
        raise ValueError("Canonical assembled OBJ and manifest differ")
    moved = move_triangles(assembled, offsets)
    observed_parts, _vv, observed = read_obj(ROOT / "models/exploded.obj")
    if observed_parts != part_ids or len(observed) != len(moved):
        raise ValueError("Exploded OBJ objects/triangles differ")
    for (ap, a), (ep, e) in zip(moved, observed):
        if ap != ep:
            raise ValueError("Exploded OBJ part name mismatch")
        for p, q in zip(a, e):
            if any(abs(x-y) > close_tol for x, y in zip(p, q)):
                raise ValueError("Exploded OBJ not consistent with manifest offset: " + ap)
    for name, triangles in (("assembled", assembled), ("exploded", observed)):
        observed_stl = stl_vertices(ROOT / f"models/{name}.stl")
        expected = [vertex for _p, face in triangles for vertex in face]
        if len(observed_stl) != len(expected):
            raise ValueError("STL triangle/vertex count differs: " + name)
        for a, b in zip(observed_stl, expected):
            if any(abs(x-y) > close_tol for x, y in zip(a, b)):
                raise ValueError("STL/OBJ vertex discrepancy: " + name)
    return len(assembled)


def write_models():
    manifest = json.loads((ROOT / "assembly_manifest.json").read_text(encoding="utf-8"))
    part_ids = [p["id"] for p in manifest["parts"]]
    parts, _vv, assembled = read_obj(ROOT / "models/assembled.obj")
    if parts != part_ids or manifest["model"]["physical_dimensions_verified"]:
        raise ValueError("Refusing to generate from a mismatched or claimed-measured source")
    offsets = {p["id"]: tuple(p["explode_offset_illustrative_mm"]) for p in manifest["parts"]}
    moved = move_triangles(assembled, offsets)
    (ROOT / "models/exploded.obj").write_text(obj_contents(parts, moved, True), encoding="utf-8")
    (ROOT / "models/assembled.stl").write_text(stl_contents(assembled), encoding="utf-8")
    (ROOT / "models/exploded.stl").write_text(stl_contents(moved), encoding="utf-8")
    return len(assembled)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Non-mutating mesh consistency check")
    mode.add_argument("--write", action="store_true", help="Regenerate exploded OBJ and both STL preview files")
    args = parser.parse_args()
    count = write_models() if args.write else verify()
    print(f"PASS: {count} illustrative triangles; 13 stable part groups; physical fit unverified")
