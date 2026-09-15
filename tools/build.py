"""Validate and reproducibly package only the Kodi runtime files."""
import ast
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ADDON_ID = "plugin.audio.radiode"


def build():
    metadata = ET.parse(ROOT / "addon.xml").getroot()
    version = metadata.attrib["version"]
    assert metadata.attrib["id"] == ADDON_ID
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), version
    for name in ("addon.py", "addon_utils.py", "LICENSE.txt", "icon.png", "fanart.jpg"):
        assert (ROOT / name).is_file(), name
    files = [ROOT / name for name in (
        "addon.py", "addon_utils.py", "addon.xml", "LICENSE.txt", "changelog.txt",
        "icon.png", "fanart.jpg", "fanart_podcast.jpg")]
    files += [p for directory in ("src", "resources")
              for p in (ROOT / directory).rglob("*")
              if p.is_file() and "__pycache__" not in p.parts
              and p.suffix not in (".pyc", ".pyo")]
    for path in files:
        assert not path.is_symlink(), path
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        elif path.suffix == ".xml":
            ET.parse(path)
    output = ROOT / "dist" / f"{ADDON_ID}-{version}.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            info = zipfile.ZipInfo(f"{ADDON_ID}/{path.relative_to(ROOT).as_posix()}",
                                   date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert archive.read(f"{ADDON_ID}/addon.xml") == (ROOT / "addon.xml").read_bytes()
    print(output)
    return output, metadata


if __name__ == "__main__":
    build()
