"""Build self-contained, deterministic one-service LibreChat release archives."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def bundled_guide(text, current, version):
    """Keep image/onboarding links local; pin source-only links to this release."""
    def replace(match):
        target = match.group(1)
        if urlsplit(target).scheme or target.startswith(("#", "/")):
            return match.group(0)
        resolved = Path(current).parent / target.split("#", 1)[0]
        parts = []
        for part in resolved.parts:
            if part == "..":
                parts.pop()
            elif part != ".":
                parts.append(part)
        relative = "/".join(parts)
        if relative == "README.md":
            return match.group(0).replace(target, "../GUIDE.md")
        if relative.startswith("plugins/"):
            return match.group(0).replace(
                target,
                f"https://github.com/AceDataCloud/LibreChatPlugins/tree/v{version}/{relative}",
            )
        return match.group(0)
    return re.sub(r"\]\(([^)]+)\)", replace, text)


def package_contents(service, source_root=ROOT):
    directory = source_root / "plugins" / service["slug"]
    manifest = json.loads((directory / "plugin.json").read_text())
    version = manifest["version"]
    contents = {
        str(source.relative_to(directory)): source.read_bytes()
        for source in sorted(directory.rglob("*")) if source.is_file()
    }
    contents["README.md"] = contents["README.md"].decode().replace(
        "../../README.md", "GUIDE.md",
    ).replace("../../readme/README_zh_Hans.md", "readme/README_zh_Hans.md").encode()
    for filename in ("LICENSE", "PRIVACY.md"):
        contents[filename] = (source_root / filename).read_bytes()
    contents["GUIDE.md"] = bundled_guide(
        (source_root / "README.md").read_text(), "README.md", version,
    ).encode()
    contents["readme/README_zh_Hans.md"] = bundled_guide(
        (source_root / "readme/README_zh_Hans.md").read_text(),
        "readme/README_zh_Hans.md", version,
    ).encode()
    for image in sorted((source_root / "assets/tutorial").iterdir()):
        if image.is_file():
            contents["assets/tutorial/" + image.name] = image.read_bytes()
    contents["licenses/LibreChat-MIT.txt"] = (source_root / "scripts/upstream/LICENSE").read_bytes()
    return manifest, contents


def build_packages(output, source_root=ROOT):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for service in json.loads((source_root / "services.json").read_text()):
        manifest, contents = package_contents(service, source_root)
        name, version = manifest["name"], manifest["version"]
        archive = output / f"{name}-{version}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for relative, data in sorted(contents.items()):
                entry = zipfile.ZipInfo(name + "/" + relative, (2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                bundle.writestr(entry, data)
        artifacts.append(archive)
    checksums = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in sorted(artifacts)
    )
    (output / "SHA256SUMS").write_text(checksums)
    return artifacts


if __name__ == "__main__":
    for artifact in build_packages(ROOT / "dist"):
        print(artifact.name)
