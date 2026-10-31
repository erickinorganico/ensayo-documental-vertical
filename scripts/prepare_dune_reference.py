"""Create public reference measurements and selected implementation examples.

Run only against the original dossier. No media or provider credentials are copied.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[1]
EXPECTED = "fac351572ac33b6d4fdaacef7811ea181762c588d4fd093d9f93f74a68233da8"


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dossier", type=Path, required=True)
    args = ap.parse_args()
    d = args.dossier.resolve(strict=True)
    hf = d / "produccion-hyperframes-v2"
    master = hf / "renders/Dune-v5-HyperFrames-v4.mp4"
    if sha(master) != EXPECTED:
        raise ValueError("Approved master hash mismatch")
    paths = [master, d / "voz-v5-v4/assets/voz-erick-original.mp3",
             d / "musica-elevenlabs-r2/DUNE-r2-vocal-muestra45s.mp3",
             d / "musica-elevenlabs-r2/music__20261031_110232.mp3",
             d / "musica-elevenlabs-r2/music__20261031_112450.mp3",
             d / "musica-elevenlabs-r2/DUNE-r2-completa-cama490s.wav",
             hf / "assets/fonts/Montserrat-Black.ttf", hf / "assets/fonts/OFL-Montserrat.txt",
             hf / "index.html", hf / "renders/QA-HF-v4.json"]
    record = {
        "style": "pi-ensayo-cinematografico", "version": "1.0.0",
        "approval_date": "2026-10-31", "timezone": "America/Tijuana",
        "approval_scope": "Dune v5 HyperFrames v4: guion, audiovisual, musica; referencia para videos serios de PI",
        "human_quote": "ME ENCANTÓ! Finalmente el video perfecto tanto en guion, audiovisual, musica, etc.",
        "preserved_files": [{"path": str(p.relative_to(d)).replace('\\', '/'), "sha256": sha(p), "bytes": p.stat().st_size} for p in paths],
        "measurements": json.loads((hf / "renders/QA-HF-v4.json").read_text(encoding="utf-8-sig")),
        "versions_observed": {"hyperframes": "0.8.223", "tesseract": "0.4.0", "tts_model": "eleven_v4", "music_model": "music_v2"},
        "music": {"sample_real_seconds": [0, 40], "crossfade_seconds": [40, 45], "bed_seconds": 490,
                  "reference_uploaded": False, "conditioning": "local analysis informed textual prompt",
                  "ducking_for_this_bed_only": {"speech": 0.22, "pause": 0.9, "pivot": 0.05, "dialogue": 0.03}},
        "media_in_public_repo": "Montserrat Black and OFL only; no film, narration or music",
        "limits": ["Approximate within-phrase timing, no completed ASR alignment", "Three clipped samples in long music source, attenuation cannot restore them", "Final true peak -0.8 exceeds original -1 target by 0.2dB", "Trailer dark intervals retained; no continuous frame-by-frame human inspection claimed", "Third-party movie clips not licensed CC or certified fair use"]
    }
    target = REPO / "skills/pi-ensayo-cinematografico/references/DUNE-V4-APROBADO.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    examples = REPO / "examples/dune-v4"
    examples.mkdir(parents=True, exist_ok=True)
    exported = []
    for name in ["particulas.py", "segmentar.py", "render-v4.ps1", "ensamblar_v4.py"]:
        src = hf / "herramientas" / name
        dest = examples / name
        dest.write_bytes(src.read_bytes().replace(b'\r\n', b'\n'))
        exported.append({"path": name, "source_relative_to_dossier": str(src.relative_to(d)).replace('\\', '/'), "source_sha256": sha(src), "normalization": "CRLF to LF only", "sha256": sha(dest)})
    (examples / "SOURCE-MANIFEST.json").write_text(json.dumps({"context": "historical implementation, requires original project inputs; not standalone renderer", "files": exported}, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    print(json.dumps({"reference_files": len(paths), "examples": len(exported), "master_verified": True}))


if __name__ == "__main__":
    main()
