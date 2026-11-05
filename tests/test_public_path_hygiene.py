"""Fail a public-repository CI check when obvious private pathnames are tracked.

This is not a content/commit-history secret scan. .gitignore alone is insufficient:
it can be bypassed with git add -f, and it does not untrack earlier commits.
"""
from pathlib import PurePosixPath
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DIRS = {"secrets", "private", "private-data", "local-evidence", "bench-evidence", "receipts"}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".sqlite", ".sqlite3"}


def sensitive_tracked_path(raw):
    parts = PurePosixPath(raw.replace("\\", "/")).parts
    if not parts:
        return False
    name = parts[-1].lower()
    if any(part.lower() in PRIVATE_DIRS for part in parts[:-1]):
        return True
    if (name == ".env" or name.startswith(".env.")) and name != ".env.example":
        return True
    if any(name.endswith(suffix) for suffix in PRIVATE_SUFFIXES):
        return True
    return (
        (len(parts) >= 2 and parts[0] == "bom" and name.startswith("private-") and name.endswith(".csv"))
        or (len(parts) >= 2 and parts[0] == "integration" and name.startswith("private-") and name.endswith(".csv"))
    )


class PublicPathHygieneTests(unittest.TestCase):
    def test_no_tracked_private_file_paths(self):
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
        )
        tracked = [p.decode("utf-8") for p in result.stdout.split(b"\0") if p]
        private_paths = [p for p in tracked if sensitive_tracked_path(p)]
        self.assertEqual(
            private_paths, [],
            "Tracked private paths require removal, history review and possibly key rotation"
        )

    def test_guard_examples(self):
        for path in (".env", "config/.env.production", "secrets/token.json",
                     "private-data/measurements.csv", "receipts/receipt.pdf",
                     "bom/private-acquisition.csv", "integration/private-run.csv",
                     "cert/server.pem"):
            with self.subTest(path=path):
                self.assertTrue(sensitive_tracked_path(path))
        for path in (".env.example", "bom/components.csv",
                     "integration/system-manifest.json", "docs/BEGINNER_GUIDE.md",
                     "examples/tripwire/model.stl"):
            with self.subTest(path=path):
                self.assertFalse(sensitive_tracked_path(path))


if __name__ == "__main__":
    unittest.main()
