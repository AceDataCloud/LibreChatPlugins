import importlib.util
import json
import posixpath
import re
import tempfile
import unittest
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("packer", ROOT / "scripts/pack.py")
packer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packer)


class PackageTests(unittest.TestCase):
    def test_every_archive_is_single_service_and_self_contained(self):
        with tempfile.TemporaryDirectory() as temporary:
            archives = packer.build_packages(temporary)
            self.assertEqual(len(archives), 5)
            for archive in archives:
                with self.subTest(archive=archive.name), zipfile.ZipFile(archive) as bundle:
                    names = set(bundle.namelist())
                    roots = {name.split("/")[0] for name in names}
                    self.assertEqual(len(roots), 1)
                    root = roots.pop()
                    for required in ("LICENSE", "PRIVACY.md", "README.md", "GUIDE.md",
                                     "readme/README_zh_Hans.md", "assets/tutorial/source.json",
                                     "licenses/LibreChat-MIT.txt"):
                        self.assertIn(root + "/" + required, names)
                    self.assertIn("MIT License", bundle.read(root + "/LICENSE").decode())
                    self.assertEqual(len(json.loads(bundle.read(root + "/mcp.json"))["mcpServers"]), 1)
                    self.assertEqual(len([name for name in names if name.endswith("/plugin.json")]), 1)
                    for name in names:
                        self.assertFalse(name.endswith(".env"))
                        if not name.endswith(".md"):
                            continue
                        text = bundle.read(name).decode()
                        for target in re.findall(r"\]\(([^)]+)\)", text):
                            if urlsplit(target).scheme or target.startswith("#"):
                                continue
                            target = unquote(target.split("#", 1)[0])
                            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                            self.assertTrue(resolved.startswith(root + "/"), (name, target))
                            self.assertIn(resolved, names, (name, target))
                    bundle.extractall(Path(temporary) / "installed")
                    installed = Path(temporary) / "installed" / root
                    self.assertTrue((installed / "plugin.json").is_file())
                    self.assertTrue((installed / "readme/README_zh_Hans.md").is_file())

    def test_builds_are_reproducible_and_checksums_match(self):
        import hashlib
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            left = packer.build_packages(first)
            right = packer.build_packages(second)
            self.assertEqual([p.name for p in left], [p.name for p in right])
            for a, b in zip(left, right):
                self.assertEqual(a.read_bytes(), b.read_bytes())
            for line in (Path(first) / "SHA256SUMS").read_text().splitlines():
                expected, filename = line.split("  ", 1)
                self.assertEqual(hashlib.sha256((Path(first) / filename).read_bytes()).hexdigest(), expected)
