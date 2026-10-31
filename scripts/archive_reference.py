"""Index local Dune inputs and freeze editable sources; never upload media.

Uses only the Python standard library. Target must be new to avoid replacing a freeze.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

EXCLUDED = {".git", "node_modules", "__pycache__", "_render", ".hyperframes", ".almacen"}
SOURCE_EXT = {".html", ".css", ".js", ".mjs", ".py", ".ps1", ".json", ".srt", ".txt", ".md", ".tsrct"}
EXPECTED_MASTER = "fac351572ac33b6d4fdaacef7811ea181762c588d4fd093d9f93f74a68233da8"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def collect(dossier: Path):
    roots = ["produccion-hyperframes-v2", "produccion-tesseract-v1", "voz-v5-v4", "musica-elevenlabs-r2", "clips-codex",
             "produccion-hyperframes-v2/.almacen/tesseract-arrakis"]
    for root in roots:
        folder = dossier / root
        if not folder.exists():
            raise FileNotFoundError(folder)
        for path in sorted(folder.rglob("*")):
            # The archived Arrakis native project is an intentional dependency,
            # unlike historical rendered caches under the rest of .almacen.
            skip = EXCLUDED - {".almacen"} if root.endswith("tesseract-arrakis") else EXCLUDED
            if path.is_file() and not set(path.relative_to(dossier).parts).intersection(skip):
                yield path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dossier", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    dossier = args.dossier.resolve(strict=True)
    master = dossier / "produccion-hyperframes-v2/renders/Dune-v5-HyperFrames-v4.mp4"
    if digest(master) != EXPECTED_MASTER:
        raise ValueError("Master differs from approved v4; refusing to label this archive approved")
    out = args.out.resolve()
    # Never recurse into our own output, nor replace an earlier freeze.
    out.mkdir(parents=True, exist_ok=False)
    entries = []
    with zipfile.ZipFile(out / "fuentes-editables.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in collect(dossier):
            if out == path or out in path.parents:
                continue
            rel = path.relative_to(dossier)
            entries.append({"path": rel.as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)})
            # Avoid caches/log transcripts and huge generated particle/mask-frame text.
            if path.suffix.lower() in SOURCE_EXT and "renders" not in rel.parts and (path.suffix.lower() == ".tsrct" or path.stat().st_size <= 10 * 1024 * 1024):
                archive.write(path, rel.as_posix())
        for pattern in ("ENTREGA*json", "APROBACION*json", "CONTINUACION*md", "ORDEN*json"):
            for path in sorted(dossier.glob(pattern)):
                archive.write(path, path.name)
    manifest = {"kind": "private-local-reference", "master_sha256": EXPECTED_MASTER,
                "dossier": str(dossier), "media_embedded_in_zip": False,
                "excluded_dirs": sorted(EXCLUDED), "files": entries,
                "note": "Media remain at indexed paths. ZIP alone is not a standalone reproducible project."}
    (out / "manifest-private.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"files": len(entries), "source_zip_bytes": (out / "fuentes-editables.zip").stat().st_size,
                      "manifest": str(out / "manifest-private.json"), "master_verified": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
