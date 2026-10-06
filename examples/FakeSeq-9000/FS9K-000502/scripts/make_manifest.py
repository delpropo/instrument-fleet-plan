"""Write a manifest (file name, size, sha256) for every file in a directory.

Usage: make_manifest.py [--dir DIR] [--out-dir DIR]
The manifest is write-once: an existing file is never overwritten.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

INSTRUMENT_DIR = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=INSTRUMENT_DIR / "sample_logs")
    ap.add_argument("--out-dir", type=Path, default=INSTRUMENT_DIR / "manifests")
    args = ap.parse_args()

    info = yaml.safe_load((INSTRUMENT_DIR / "instrument.yaml").read_text())
    now = datetime.now(timezone.utc)
    manifest = {
        "schema_version": 1,
        "instrument_key": info["key"],
        "created_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": [
            {"name": p.name, "size_bytes": p.stat().st_size, "sha256": sha256(p)}
            for p in sorted(args.dir.iterdir())
            if p.is_file()
        ],
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"manifest_{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    with out.open("x") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(out)


if __name__ == "__main__":
    main()
