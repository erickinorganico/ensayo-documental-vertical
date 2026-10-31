"""Check package integrity, local links and an optional approved Dune master."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills/pi-ensayo-cinematografico"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dossier", type=Path)
    args = ap.parse_args()
    errors = []
    for md in SKILL.rglob("*.md"):
        txt = md.read_text(encoding="utf-8-sig")
        for link in re.findall(r"\]\(([^\s)]+)\)", txt):
            if re.match(r"[a-z]+:|#", link):
                continue
            if not (md.parent / link.split("#")[0]).exists():
                errors.append(f"Broken link {md.relative_to(REPO)}: {link}")
    reference = json.loads((SKILL / "references/DUNE-V4-APROBADO.json").read_text(encoding="utf-8"))
    brief = json.loads((SKILL / "assets/brief.json").read_text(encoding="utf-8"))
    if brief["authorization"]["paid_media"] or brief["authorization"]["publish"]:
        errors.append("Template must not imply paid media/publication authorization")
    if args.dossier:
        for item in reference["preserved_files"]:
            file = args.dossier / item["path"]
            if not file.is_file():
                errors.append(f"Missing reference: {item['path']}")
                continue
            if item.get("sha256"):
                h = hashlib.sha256()
                with file.open("rb") as f:
                    for block in iter(lambda: f.read(1024 * 1024), b""):
                        h.update(block)
                if h.hexdigest() != item["sha256"]:
                    errors.append(f"Reference changed: {item['path']}")
    for path in ["RECETAS-VISUALES.md", "RECETAS-AUDIO.md", "RENDER-Y-RECUPERACION.md"]:
        if not (SKILL / "references" / path).is_file():
            errors.append(f"Missing Claude recipe: {path}")
    print(json.dumps({"ok": not errors, "errors": errors, "local_media_checked": bool(args.dossier)}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
