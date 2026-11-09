"""Self-contained contract tests: Python stdlib only, no network access."""
import os
import tempfile
import unittest
from pathlib import Path

from stage import stage_public, validate_path


class StagePublicTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="public-devops-proof-")
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)
        self.source = self.parent / "source"
        self.source.mkdir()
        self.out = self.parent / "dist"
        (self.source / "assets").mkdir()
        (self.source / "index.html").write_text("<h1>Safe public site</h1>", encoding="utf8")
        (self.source / "assets" / "app.css").write_text("body{color:black}", encoding="utf8")

    def assets(self):
        return ["index.html", "assets/app.css"]

    def test_explicit_manifest_stages_only_declared_files(self):
        (self.source / "private-key.txt").write_text("never publish", encoding="utf8")
        size = stage_public(self.source, self.out, self.assets())
        self.assertGreater(size, 0)
        self.assertTrue((self.out / "index.html").exists())
        self.assertTrue((self.out / "assets" / "app.css").exists())
        self.assertFalse((self.out / "private-key.txt").exists())

    def test_no_extra_directory_copy_or_internal_files(self):
        (self.source / ".github").mkdir()
        (self.source / ".github" / "workflows.yml").write_text("private", encoding="utf8")
        (self.source / "README.md").write_text("private", encoding="utf8")
        stage_public(self.source, self.out, self.assets())
        self.assertFalse((self.out / ".github").exists())
        self.assertFalse((self.out / "README.md").exists())

    def test_traversal_and_absolute_paths_rejected(self):
        for bad in ["../private.html", "/etc/passwd", "assets/../index.html", "./index.html", "assets\\app.css"]:
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    validate_path(bad)

    def test_duplicate_manifest_entries_rejected(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            stage_public(self.source, self.out, ["index.html", "index.html"])

    def test_unsupported_extension_and_hidden_file_rejected(self):
        for bad in [".env", ".github/workflow.yml", "notes.md", "dump.sql", "secrets/key.p8"]:
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    validate_path(bad)

    def test_missing_file_must_fail(self):
        with self.assertRaises(FileNotFoundError):
            stage_public(self.source, self.out, ["missing.html"])

    def test_symlink_file_rejected(self):
        target = self.source / "index.html"
        link = self.source / "link.html"
        os.symlink(target, link)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            stage_public(self.source, self.out, ["link.html"])

    def test_symlink_directory_rejected(self):
        target = self.source / "assets"
        link = self.source / "aliases"
        os.symlink(target, link)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            stage_public(self.source, self.out, ["aliases/app.css"])

    def test_secret_not_copied_to_public_output(self):
        (self.source / "index.html").write_text(
            "sk_live_" + "A" * 24, encoding="utf8"
        )
        with self.assertRaisesRegex(ValueError, "Credential-like"):
            stage_public(self.source, self.out, self.assets())
        self.assertFalse(self.out.exists())

    def test_oversized_file_rejected(self):
        (self.source / "assets" / "app.css").write_bytes(b"x" * (2 * 1024 * 1024 + 1))
        with self.assertRaisesRegex(ValueError, "exceeds"):
            stage_public(self.source, self.out, self.assets())
        self.assertFalse(self.out.exists())

    def test_release_replaces_stale_artifacts(self):
        self.out.mkdir()
        (self.out / "old.html").write_text("Old cache", encoding="utf8")
        stage_public(self.source, self.out, self.assets())
        self.assertFalse((self.out / "old.html").exists())


if __name__ == "__main__":
    unittest.main()
