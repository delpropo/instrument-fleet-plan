# FakeSeq-9000 / FS9K-000418 (example instrument)

A fake instrument ("donald", a made-up DNA sequencer) showing what one serial number's folder could hold.
Everything here is invented. See `local/instrument-fleet-plan.md` for the design.

| Path | What it is | Where it belongs in the plan |
|---|---|---|
| `instrument.yaml` | Per-serial identity, location, connection, declared software version and history, hardware | Registry repo (git) |
| `events.yaml` | Append-only log of repairs, moves, part swaps | Registry repo (git) |
| `resolutions/` | Troubleshooting records: symptom, evidence, root cause, fix, verification | Registry/type pack (git) |
| `scripts/` | Helper scripts for this instrument (see below) | Illustration only: shared code should live once in the platform repo, not per serial |
| `sample_logs/` | Tiny fake raw log | Object storage in real use (`<type>/<serial>/<date>/`), not git |
| `manifests/` | Write-once manifest of stored files with checksums | Beside the data in object storage |
| `derived/observed.json` | Output of the log scan: observed version, assays, signatures, drift flag | Derived index; rebuildable |
| `staging/` | Where `collect_logs.sh` copies files (git-ignored) | Temporary |

Type-level facts (baseline version, connection procedure, retention, parser, signatures) are not here; they go in `types/FakeSeq-9000/`.

## Scripts

Run in WSL with the conda environment active (`conda activate instrument-fleet-plan`), from this folder:

```bash
python scripts/scan_logs.py                                         # observed vs declared version; exit 1 on drift
python scripts/make_manifest.py                                     # checksums for sample_logs/ into manifests/
bash scripts/collect_logs.sh --source sample_logs/ --dest staging   # dry run; add --run to copy
```

`collect_logs.sh` builds the real source (`user@host:path`) from `instrument.yaml` when `--source` is not given.
It never overwrites existing files, so re-running is safe. `scan_logs.py` never edits `instrument.yaml`; a
version change is a reviewed update to that file.
