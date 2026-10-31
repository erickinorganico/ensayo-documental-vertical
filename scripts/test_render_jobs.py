"""Local smoke test: real tiny render, cache invalidation and safe installation.

Requires ffmpeg/ffprobe, no providers or network. All test files stay in a
temporary directory within private-archive and are removed after path checking.
"""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env={**os.environ, "PYTHONUTF8": "1"})


def main():
    spec = importlib.util.spec_from_file_location("jobs", REPO / "scripts/render_jobs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    scratch = REPO / "private-archive"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="smoke-", dir=scratch) as folder:
        r = Path(folder).resolve()
        assert scratch.resolve() in r.parents
        (r / "input.txt").write_text("original", encoding="utf-8")
        job = {"inputs": ["input.txt"], "command": ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
               "color=c=black:s=64x64:r=30", "-frames:v", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p", "out.mp4"],
               "output": "out.mp4", "expected_frames": 3}
        (r / "plan.json").write_text(json.dumps({"cwd": ".", "jobs": [job]}), encoding="utf-8")
        runner = [sys.executable, str(REPO / "scripts/render_jobs.py"), str(r / "plan.json")]
        p = run(runner)
        assert p.returncode == 0, p.stderr
        assert "DONE" in p.stdout
        p = run(runner)
        assert p.returncode == 0, p.stderr
        assert "REUSE" in p.stdout
        initial = hashlib.sha256((r / "out.mp4").read_bytes()).hexdigest()
        fp = mod.fingerprint(r, job)
        (r / "input.txt").write_text("modified", encoding="utf-8")
        assert mod.fingerprint(r, job) != fp
        p = run(runner)
        assert p.returncode != 0 and "Unverified/stale output preserved" in p.stderr, p.stderr
        assert hashlib.sha256((r / "out.mp4").read_bytes()).hexdigest() == initial
        assert (r / "plan.json.lock").exists()
        targets = [r / "codex/pi-ensayo-cinematografico", r / "claude/pi-ensayo-cinematografico"]
        install = [sys.executable, str(REPO / "scripts/install_style.py")]
        for t in targets:
            install += ["--target", str(t)]
        p = run(install)
        assert p.returncode == 0, p.stderr
        assert all((t / "SKILL.md").exists() for t in targets)
        (targets[0] / "SKILL.md").write_text("custom destination", encoding="utf-8")
        p = run(install)
        assert p.returncode != 0
        assert (targets[0] / "SKILL.md").read_text(encoding="utf-8") == "custom destination"
    result = {"render_real_fixture": True, "reuses_unchanged_inputs": True,
              "rejects_stale_same_duration": True, "preserves_output": True,
              "keeps_failure_lock": True, "installer_two_targets": True, "preserves_custom_skill": True}
    (scratch / "SMOKE-QA.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
