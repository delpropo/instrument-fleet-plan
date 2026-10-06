<p align="center">
  <img src="./assets/banner.svg" alt="FakeSeq-9000: example instrument type" width="100%">
</p>

<p align="center">
  <strong>A worked example of how one instrument type and its serial numbers could be recorded in the registry.</strong><br>
  All instruments, serials, logs and people here are invented.
</p>

---

## Overview

`FakeSeq-9000` is a made-up DNA sequencer. This folder holds five fake units with a cartoon duck theme.
Each unit has its own folder, named by serial number, with the same layout:

- identity, location, connection and software version history (`instrument.yaml`)
- an append-only event log (`events.yaml`)
- troubleshooting records (`resolutions/`)
- a small sample log, a checksum manifest and scan output
- helper scripts

See [`local/instrument-fleet-plan.md`](../../local/instrument-fleet-plan.md) for the design this example follows.

## Fleet

| Serial | Nickname | Location | Status | Declared software | What it illustrates |
|:--|:--|:--|:--:|:--:|:--|
| [FS9K-000417](./FS9K-000417) | daffy | Building 2, B214 | active | 4.2.1 | A repaired fault (E1042) with a resolution record |
| [FS9K-000418](./FS9K-000418) | donald | Building 2, B214 | active | 4.2.1 | A healthy unit running two assays |
| [FS9K-000455](./FS9K-000455) | daisy | Building 2, B216 | active | 4.2.1 | Version drift: the log shows 4.2.2 |
| [FS9K-000502](./FS9K-000502) | scrooge | Building 3, C101 | active | 4.1.9 | Older software, a move between buildings, a different error (E2007) |
| [FS9K-000533](./FS9K-000533) | darkwing | Building 3, C105 | repair | 4.2.1 | An open repair: repeated E1042, no resolution yet |

## Layout of a unit folder

```text
FS9K-000417/
??? instrument.yaml     per-serial facts (registry, git)
??? events.yaml         repairs, moves, part swaps (registry, git)
??? resolutions/        troubleshooting records
??? scripts/            collect_logs.sh, scan_logs.py, make_manifest.py
??? sample_logs/        tiny fake raw log (real logs live in object storage)
??? manifests/          write-once checksum manifests
??? derived/            observed.json from the log scan (rebuildable)
??? staging/            collection scratch space (git-ignored)
```

Type-level facts (baseline version, connection procedure, retention, parser, signatures) are not recorded per
serial. They would live in a type pack at `types/FakeSeq-9000/`.

## Quick start

Run in WSL with the conda environment active (see the [root README](../../README.md)):

```bash
conda activate instrument-fleet-plan
cd examples/FakeSeq-9000/FS9K-000455

python scripts/scan_logs.py        # compare observed and declared version; exits 1 on drift
python scripts/make_manifest.py    # checksum sample_logs/ into manifests/
bash scripts/collect_logs.sh --source sample_logs/ --dest staging   # dry run; add --run to copy
```

> [!NOTE]
> The scripts in each folder are identical copies, kept only to make each example self-contained. In real use
> they would live once in the platform repo.
