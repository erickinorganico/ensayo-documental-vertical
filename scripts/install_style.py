"""Install the cinematic skill for an agent without replacing unrelated files.

Default installs project-scoped Claude/Codex skills. Use explicit --target paths
for user-scoped Codex, Claude Personal or Claude Cliente locations.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "skills/pi-ensayo-cinematografico"


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def install(target: Path, update: bool):
    target = target.resolve()
    if target == SOURCE or SOURCE in target.parents:
        raise ValueError("Installation target must be outside source skill")
    files = [p for p in SOURCE.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    conflicts = [str(p.relative_to(SOURCE)) for p in files if (target / p.relative_to(SOURCE)).exists()
                 and digest(p) != digest(target / p.relative_to(SOURCE))]
    if conflicts and not update:
        raise FileExistsError("Changed destination files preserved; compare before --update: " + ", ".join(conflicts))
    for p in files:
        dest = target / p.relative_to(SOURCE)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and digest(p) != digest(dest):
            backup = dest.with_name(dest.name + ".before-update-" + digest(dest)[:12])
            if not backup.exists():
                shutil.copy2(dest, backup)
        shutil.copy2(p, dest)
    print(f"Installed {len(files)} files: {target}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=Path, action="append")
    ap.add_argument("--update", action="store_true", help="Back up and replace changed files of this skill only")
    args = ap.parse_args()
    targets = args.target or [REPO / ".claude/skills/pi-ensayo-cinematografico", REPO / ".agents/skills/pi-ensayo-cinematografico"]
    for target in targets:
        install(target, args.update)


if __name__ == "__main__":
    main()
