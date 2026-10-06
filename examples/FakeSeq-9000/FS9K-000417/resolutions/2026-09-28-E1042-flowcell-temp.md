# E1042 flowcell temperature out of range

- **Instrument:** FakeSeq-9000/FS9K-000417
- **Date:** 2026-09-28
- **Software version at the time:** 4.2.1 (observed in log, matches declared)
- **Symptom:** run R-20260928-001 paused at cycle 150; flowcell temperature 24.9C against a 22.0C limit.
- **Evidence:** `sample_logs/fakeseq_20260928.log` lines 4-5 (sha256 in `manifests/`).
- **Root cause:** failing Peltier module in the flowcell stage.
- **Fix:** replaced the flowcell stage module (FC-88201 -> FC-88213). Logged in `events.yaml`.
- **Verification:** run R-20260928-002 completed with status=ok.
- **Signature:** E1042 (add to the type pack's signature list if not already present).
