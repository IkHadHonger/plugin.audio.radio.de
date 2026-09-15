"""Allocate a release version by comparing the built package to Piers."""
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from build import ROOT, ADDON_ID, build


def read_version(path):
    root = ET.parse(path).getroot()
    assert root.attrib["id"] == ADDON_ID
    value = root.attrib["version"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", value), value
    return tuple(map(int, value.split(".")))


def prepare(target):
    package, _ = build()
    manifest = ROOT / "addon.xml"
    source = read_version(manifest)
    published_manifest = target / "addon.xml"
    if not published_manifest.exists():
        return True, False
    published = read_version(published_manifest)
    if source < published:
        raise RuntimeError("Source version is older than Piers; update main before retrying")
    if source > published:
        return True, False
    existing = target / package.name
    if not existing.exists():
        raise RuntimeError("Published ZIP missing; review repository consistency")
    if package.read_bytes() == existing.read_bytes():
        return False, False
    next_version = ".".join(map(str, (*source[:2], source[2] + 1)))
    text = manifest.read_text(encoding="utf-8")
    text, count = re.subn(
        r'(<addon\b[^>]*\bversion=")[^"]+(")',
        lambda match: match[1] + next_version + match[2], text, count=1)
    assert count == 1
    manifest.write_text(text, encoding="utf-8")
    assert read_version(manifest) == (*source[:2], source[2] + 1)
    print("Automatic addon version: " + next_version)
    return True, True


if __name__ == "__main__":
    publish, bumped = prepare(Path("repo-silvo/piers") / ADDON_ID)
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"publish={str(publish).lower()}\n")
        output.write(f"bumped={str(bumped).lower()}\n")
    if not publish:
        print("Addon package unchanged; no release needed.")
