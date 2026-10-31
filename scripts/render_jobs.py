"""Run explicit render jobs with content fingerprints, output QA and a lock.

This wrapper does not discover scene dependencies: list EVERY transitive input
or a directory containing them. Plans are local trusted executable instructions.
No implicit retries, shell expansion, downloads, media generation or publication.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fingerprint(root, job):
    records = []
    if not job.get("inputs"):
        raise ValueError("Every job needs explicit transitive inputs")
    for name in sorted(job["inputs"]):
        p = root / name
        if not p.exists():
            raise FileNotFoundError(p)
        files = sorted(x for x in p.rglob("*") if x.is_file()) if p.is_dir() else [p]
        for f in files:
            records.append([str(f.resolve()), digest(f)])
    data = {"inputs": records, "command": job["command"], "frames": job["expected_frames"],
            "runtime_versions": job.get("runtime_versions", {}), "cwd": str(root.resolve())}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def validate_output(path, frames):
    if not path.is_file():
        return False
    probe = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                            "-show_entries", "stream=nb_read_frames", "-of", "json", str(path)],
                           capture_output=True, text=True, timeout=600)
    if probe.returncode:
        return False
    try:
        count = int(json.loads(probe.stdout)["streams"][0]["nb_read_frames"])
    except (ValueError, KeyError, IndexError):
        return False
    if count != frames:
        return False
    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                            capture_output=True, timeout=600)
    return decode.returncode == 0 and not decode.stderr.strip()


def reusable(root, job, fp):
    out = root / job["output"]
    receipt = out.with_name(out.name + ".job.json")
    if not receipt.is_file() or not out.is_file():
        return False
    try:
        r = json.loads(receipt.read_text(encoding="utf-8"))
        return (r["fingerprint"] == fp and r["sha256"] == digest(out)
                and validate_output(out, job["expected_frames"]))
    except (KeyError, ValueError):
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plan", type=Path)
    ap.add_argument("--dry-run", action="store_true", help="Fingerprint inputs only, no rendering or output modification")
    args = ap.parse_args()
    plan_path = args.plan.resolve(strict=True)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    root = (plan_path.parent / plan.get("cwd", ".")).resolve(strict=True)
    jobs = plan["jobs"]
    if len({j["output"] for j in jobs}) != len(jobs):
        raise ValueError("Duplicate outputs in render plan")
    # Never allow a job output inside an input directory: that self-invalidates
    # fingerprints and risks capturing a render as its own source.
    for job in jobs:
        output = (root / job["output"]).resolve()
        for name in job["inputs"]:
            p = (root / name).resolve()
            if p == output or (p.is_dir() and p in output.parents):
                raise ValueError("Output must be outside input files/directories")
        if not isinstance(job["command"], list) or not all(isinstance(s, str) for s in job["command"]):
            raise ValueError("Command must be an argument array, not shell text")
    if args.dry_run:
        print(json.dumps([{"output": j["output"], "fingerprint": fingerprint(root, j)} for j in jobs], indent=2))
        return
    lock = plan_path.with_name(plan_path.name + ".lock")
    # An existing lock requires reconciling its PID/log before a human removes it.
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w") as f:
        json.dump({"pid": os.getpid(), "started": time.time(), "plan": str(plan_path)}, f)
    complete = False
    try:
        for job in jobs:
            fp = fingerprint(root, job)
            if reusable(root, job, fp):
                print("REUSE", job["output"], flush=True)
                continue
            out = root / job["output"]
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists():
                raise FileExistsError(f"Unverified/stale output preserved: {out}. Choose a new output or reconcile/archive it first.")
            log = out.with_name(out.name + ".log")
            with log.open("wb") as f:
                # No timeout retry: descendants must be reconciled before relaunch.
                p = subprocess.run(job["command"], cwd=root, stdout=f, stderr=subprocess.STDOUT)
            if p.returncode or not validate_output(out, job["expected_frames"]):
                raise RuntimeError(f"Job failed; inspect {log}. No automatic retry.")
            if fingerprint(root, job) != fp:
                raise RuntimeError("Inputs changed during render; output preserved but no valid receipt written")
            receipt = {"fingerprint": fp, "sha256": digest(out), "frames": job["expected_frames"],
                       "command": job["command"], "completed": time.time()}
            out.with_name(out.name + ".job.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
            print("DONE", job["output"], flush=True)
        complete = True
    finally:
        if complete:
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
