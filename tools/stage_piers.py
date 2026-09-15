"""Stage one addon and update only Piers catalogue files in a local checkout."""
import hashlib
from html import escape
from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

from build import ADDON_ID, ROOT, build


def index(directory):
    entries = sorted(p.name + ("/" if p.is_dir() else "")
                     for p in directory.iterdir() if p.name != "index.html")
    links = "\n".join(f'<a href="{escape(e, quote=True)}">{escape(e)}</a>' for e in entries)
    (directory / "index.html").write_text(
        '<!doctype html>\n<html><body>\n' + links + '\n</body></html>\n', encoding="utf-8")


def stage(target):
    package, metadata = build()
    channel = target.resolve() / "piers"
    catalogue_path = channel / "addons.xml"
    # Require an existing valid catalogue. Keep every other entry intact.
    original = catalogue_path.read_text(encoding="utf-8")
    catalogue = ET.fromstring(original)
    assert catalogue.tag == "addons"
    ids = [node.attrib["id"] for node in catalogue]
    assert len(ids) == len(set(ids)), "Duplicate catalogue IDs"
    version = metadata.attrib["version"]
    previous = next((node for node in catalogue if node.attrib["id"] == ADDON_ID), None)
    if previous is not None:
        old = previous.attrib["version"]
        assert re.fullmatch(r"\d+\.\d+\.\d+", old), "Review existing version format"
        assert tuple(map(int, version.split('.'))) >= tuple(map(int, old.split('.'))), "Downgrade refused"
    destination = channel / ADDON_ID
    existing = destination / package.name
    if existing.exists():
        assert existing.read_bytes() == package.read_bytes(), "Version already published with different content"
    elif previous is not None and previous.attrib["version"] == version:
        raise RuntimeError("Existing version has no matching ZIP; review before publication")
    # Match the single addon element without rewriting unrelated XML formatting.
    pattern = re.compile(r'<addon\b[^>]*\bid=[\"\']' + re.escape(ADDON_ID)
                         + r'[\"\'][^>]*>.*?</addon>', re.DOTALL)
    fragment = ET.tostring(metadata, encoding="unicode")
    if previous is not None:
        updated, count = pattern.subn(lambda _: fragment, original)
        assert count == 1
    else:
        assert original.count('</addons>') == 1
        updated = original.replace('</addons>', fragment + '\n</addons>')
    check = ET.fromstring(updated)
    assert [ET.tostring(n) for n in check if n.attrib['id'] != ADDON_ID] == [
        ET.tostring(n) for n in catalogue if n.attrib['id'] != ADDON_ID]
    destination.mkdir(exist_ok=True)
    shutil.copyfile(package, existing)
    for name in ("addon.xml", "icon.png", "fanart.jpg", "changelog.txt", "LICENSE.txt"):
        shutil.copyfile(ROOT / name, destination / name)
    catalogue_path.write_text(updated, encoding="utf-8")
    (channel / "addons.xml.md5").write_text(
        hashlib.md5(catalogue_path.read_bytes()).hexdigest(), encoding="ascii")
    index(destination)
    index(channel)
    print(f"Staged {ADDON_ID} {version} in {channel}")


if __name__ == "__main__":
    stage(Path(sys.argv[1]))
