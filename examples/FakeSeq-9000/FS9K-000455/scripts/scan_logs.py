"""Scan logs for the observed software version, assays, runs and error signatures.

Writes derived/observed.json and compares the observed version with the declared one in
instrument.yaml. Exits with status 1 if they differ (drift). Nothing in instrument.yaml is changed.

Usage: scan_logs.py [--dir DIR] [--out FILE]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

INSTRUMENT_DIR = Path(__file__).resolve().parent.parent

LINE = re.compile(r"^(?P<ts>\S+)\s+(?P<level>[A-Z]+)\s+(?P<msg>.*)$")
VERSION = re.compile(r"software_version=(?P<v>[\w.]+)")
RUN_START = re.compile(r"run_start run_id=(?P<run>\S+) assay=(?P<assay>\S+) assay_version=(?P<av>\S+)")
SIGNATURE = re.compile(r"^(?P<sig>E\d{4})\b")


def scan(log_dir: Path) -> dict:
    versions, assays, runs, signatures = [], {}, set(), {}
    for path in sorted(log_dir.glob("*.log")):
        for n, raw in enumerate(path.read_text().splitlines(), 1):
            m = LINE.match(raw)
            if not m:
                continue
            evidence = {"file": path.name, "line": n, "timestamp": m["ts"]}
            if v := VERSION.search(m["msg"]):
                versions.append({"version": v["v"], **evidence})
            if r := RUN_START.search(m["msg"]):
                runs.add(r["run"])
                assays[f"{r['assay']}@{r['av']}"] = evidence
            if m["level"] == "ERROR" and (s := SIGNATURE.match(m["msg"])):
                signatures.setdefault(s["sig"], []).append(evidence)
    return {
        "observed_version": versions[-1] if versions else None,
        "assays_seen": sorted(assays),
        "run_count": len(runs),
        "signatures": signatures,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=INSTRUMENT_DIR / "sample_logs")
    ap.add_argument("--out", type=Path, default=INSTRUMENT_DIR / "derived" / "observed.json")
    args = ap.parse_args()

    info = yaml.safe_load((INSTRUMENT_DIR / "instrument.yaml").read_text())
    declared = info["software"]["declared_version"]
    result = scan(args.dir)
    observed = result["observed_version"]
    result.update(
        instrument_key=info["key"],
        declared_version=declared,
        drift=bool(observed) and observed["version"] != declared,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")

    print(f"declared={declared} observed={observed['version'] if observed else 'unknown'} drift={result['drift']}")
    return 1 if result["drift"] else 0


if __name__ == "__main__":
    sys.exit(main())
