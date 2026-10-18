import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("installer", Path(__file__).parents[1] / "scripts/install.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InstallTests(unittest.TestCase):
    def test_single_service_and_existing_install_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = module.install("suno", temp)
            self.assertEqual([x.name for x in Path(temp).iterdir()], ["suno-by-acedatacloud"])
            config = json.loads((dest / "mcp.json").read_text())
            self.assertEqual(len(config["mcpServers"]), 1)
            with self.assertRaises(FileExistsError):
                module.install("suno", temp)
            self.assertTrue((dest / "plugin.json").is_file())

    def test_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                module.install("../suno", temp)
            self.assertEqual(list(Path(temp).iterdir()), [])
