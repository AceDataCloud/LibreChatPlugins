import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
OUT.mkdir(exist_ok=True)
for service in json.loads((ROOT / "services.json").read_text()):
    directory = ROOT / "plugins" / service["slug"]
    manifest = json.loads((directory / "plugin.json").read_text())
    output = OUT / (manifest["name"] + "-" + manifest["version"] + ".zip")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(directory.rglob("*")):
            if source.is_file():
                archive.write(source, Path(manifest["name"]) / source.relative_to(directory))
    print(output.name)
