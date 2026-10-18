"""Install a selected reviewed package without overwriting an existing installation."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(service, target):
    catalog = json.loads((ROOT / "services.json").read_text())
    valid = {item["slug"] for item in catalog}
    if service not in valid:
        raise ValueError("Unknown service")
    source = ROOT / "plugins" / service
    manifest = json.loads((source / "plugin.json").read_text())
    target = Path(target).expanduser()
    target.mkdir(parents=True, exist_ok=True)
    dest = target / manifest["name"]
    if dest.exists():
        raise FileExistsError("Plugin already exists; review and replace it manually, preserving plugin data")
    shutil.copytree(source, dest)
    return dest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service")
    parser.add_argument("--plugin-dir", required=True)
    args = parser.parse_args()
    print(install(args.service, args.plugin_dir))
    print("Restart the LibreChat instance, then sign in to the service MCP. No API request was sent.")
