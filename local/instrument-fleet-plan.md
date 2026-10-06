# Instrument fleet data platform: plan and decision rationale (v3)

Status: planning only, no implementation started. Date: 2026-09-30.

## Goal
Collect logs, connection info, and instrument state for ~100 instrument types with dozens of units each (thousands total, 1-10 TB/month combined). Assays are owned by others; we only need enough assay information to tag and correlate logs and results.

## Requirements captured (from user)
- Repo-based source of truth for the instruments themselves.
- Logs stored outside git; some logs are enormous (e.g., DNA sequencers), so they need reduction to small, useful summaries.
- Scan logs to confirm software versions; record version changes over time.
- Assay reference kept in a separate location; flag assays seen in logs that are missing from the reference.
- Names: type + serial + optional friendly nickname + generic naming by assay category (7+ categories).
- Collection is pull-to-server, then update repo from what was collected.
- Retention: raw kept until class decommissioned then archived; huge raw deleted after a period with data-owner approval.
- Must scale, and be usable by other trained teams later.

## Scope
- Included: logs, registry, parsers, retention, drift and unknown-assay flagging, dashboard.
- Excluded: sequencer result data (handled elsewhere), assay content and analysis, regulatory validation (data is proprietary, not regulated).

## Architecture and the reasoning behind each choice

1. Registry repo (git) = source of truth for instruments.
   - Holds instrument.yaml and an events log per unit (per-serial facts only: serial, nickname, location, declared software version and change history, repairs, moves).
   - Type-level facts (baseline version, connection procedure, retention policy, manual-to-version map) live in the type packs (items 2 and 15), not here.
   - Why git: it is small text, needs history and review, and software updates are rare, so a reviewed PR per change fits. Thousands of small YAML files are fine in one repo.
   - Why one registry rather than per-type repos: 100 repos would drift from their template and make cross-type questions ("which units run version X") hard. One registry gives one place to validate (schema CI, including checking each unit against its type pack) and query.

2. Platform + type packs repo (git) = code and type knowledge.
   - Shared pipeline core, parser plugin contract, and one types/<type>/ type pack per instrument type with tests and small sample logs, CODEOWNERS per folder.
   - Why separate from the registry: type packs change when log formats or software change; instrument records change on hardware or software events at one unit. Mixing them ties two unrelated change rates together.
   - Why not a repo per type by default: split a type out only if it has a different owner, access rule, or release cadence. This keeps the door open without paying the cost up front.

3. Bulk log storage = object storage (S3-compatible), outside git.
   - Path convention type/serial/date. Raw is write-once. Lifecycle tiering moves older data to cheaper tiers.
   - Why: git history only grows and gets slow at GB-TB scale; object storage is built for it and has lifecycle rules. Chosen because no storage constraint exists yet.

4. Manifests beside the data instead of a pointer file in git.
   - The ingest script writes one small write-once manifest per run (instrument key, file names, checksums, sizes, dates).
   - Why not a git pointer: thousands of commits per day and a noisy history. Why not a growing file: object storage cannot append. Ingestion is the only writer, so it already knows what was added and no new-file detector is needed.
   - A periodic reconcile job compares the storage listing to the manifests to catch anything that arrived another way.

5. Derived index (SQLite/Parquet first, Postgres later) for queries and the dashboard.
   - Why derived: it can be deleted and rebuilt from manifests, so it is never a second source of truth. Start light to reduce operations burden for a small team.

6. Reduction of huge logs in stages (per type).
   - Raw: kept a set period after a verified parse, then deleted.
   - Essentials extract: small lossless extract (version lines, errors, run IDs, timestamps), kept forever.
   - Digest: common envelope (instrument key, run ID, dates, observed software version, assay ID/version, status, error counts) plus a type-specific payload; records schema and parser versions. Kept forever.
   - Tombstone: for each deleted file (checksum, size, date, policy), so it is provable what existed.
   - Why: raw size is the cost driver; the value is in a small structured summary. Keeping an essentials extract protects against a parser bug found after raw is gone.

7. Version tracking: declared vs observed.
   - Declared version lives in instrument.yaml with change history (git history plus a changelog list). Observed version comes from the log scan with evidence (file, timestamp, line). A mismatch is a drift flag.
   - Why: separating the two shows when reality differs from the record. Updates are rare, so any drift flag is meaningful. Auto-record with evidence and review afterward (user's choice); never overwrite silently, keep the prior value.
   - Risk: it is not yet known whether every type logs its version. Discovery in Phase 1 decides; fallback is a periodic manual or vendor-query check.

8. Assay reference registry, separate and synced from the owners.
   - Entries are versioned and immutable, marked active or retired, with a snapshot date stored alongside results.
   - Unknown assays are ingested and flagged, never blocking collection.
   - Why: assays go stale and are owned elsewhere. Immutable versions keep old results interpretable; not blocking prevents data loss.

9. Naming.
   - Immutable key = type + serial (a serial alone may collide across vendors). Nickname is an editable alias only. The 7+ assay categories are derived tags computed from assays actually run.
   - Why: nicknames can be reassigned or run out at thousands of units; instruments run several assays and the mix changes, so category cannot be part of an ID or path. No spaces in file names.

10. Collection: pull to a central server, copy all raw centrally, then parse (user's choice).
   - Idempotent with per-instrument watermark and retries; drop folder for manual USB exports.
   - Trade-off: huge logs cross the network before reduction. Mitigate with bandwidth limits and stream-parsing; a type can later switch to parse-near-source without changing the rest.

11. Retention and deletion.
   - Raw kept until the class is decommissioned then archived, tiered to cold storage in the meantime because 1-10 TB/month reaches hundreds of TB over years.
   - Huge raw deleted only by an owner-approved per-type policy, only after a verified parse and a minimum period. Approval is recorded with the policy.
   - Why: deletion is irreversible and a parser bug can only be fixed while raw exists.

12. Parser and software-version coupling.
   - Each parser declares the software version range it understands. Unknown format or version raises a flag and keeps the raw file; never fails silently.

13. Portability: no lock-in (added after review).
   - Principle: everything is plain, open, self-describing files (Markdown, YAML, JSON/JSONL, CSV/Parquet, gzip/zstd, tar). No proprietary database, vendor storage feature, or AI service holds truth. Any index, search, dashboard, or AI output is derived and rebuildable from the files.
   - Storage is a configurable root path and all references are relative to it. S3-compatible object storage becomes optional (this revises item 3). Tiering, checksums, and retention are our own scripts, not vendor lifecycle rules.
   - Why: tools and AI are changing fast. If all context is recorded, any layer can be replaced later without migrating the data.
   - Context recorded with the data: schema_version on every file, parser and tool versions, collection time and source, checksums, retention policy and approval, and a short decision log (what was decided and why).
   - LLMs are readers, not writers of truth. AI-generated summaries or answers are labeled as derived (model, date, inputs) and never overwrite the registry or manifests. Embeddings or vector indexes are rebuildable caches.
   - Risks: many small files strain shared file systems, so pack each run's logs into one compressed archive plus its manifest. Without vendor tiering, cold-storage moves and integrity checks are scripts we maintain. "Keep everything" at 1-10 TB/month is costly, so it applies to small data and to the context (digest, essentials, tombstone) of huge raw files.

14. Troubleshooting knowledge per type, built like parsers (added after review).
   - Each type gets a troubleshooting folder next to its parser: a symptom-organized guide, known error signatures (pattern, meaning, software versions it applies to, fix, manual citation), a manual index (source, revision, page), and links to past investigation records.
   - Parsers tag events with signature IDs, so digests record which signatures fired. "Which instruments hit signature X" becomes a query and gives the troubleshooter a starting point.
   - Manuals: binaries stay in file storage with checksums and a manifest; extracted text is searchable. The type definition maps manual revisions to software versions, because guidance for the wrong version misleads.
   - Resolution records: symptom, evidence (log references with checksums), root cause, fix, verification, plus an event-log entry in the registry for the instrument (repair, part swap, move). Hardware events are tracked separately from software versions.
   - Documentation copies (wiki, Google Doc, Obsidian) are generated from the git markdown, read-only, and stamped with the commit. Git stays the source of truth, and a drift check flags direct edits. The Equipment-Management repo already works this way: symptom-organized troubleshooting, investigation records, and a manuals corpus.
   - Search: raw logs are outside git and can be huge or deleted, so a single-repo search covers small derived artifacts in git plus a rebuildable full-text index of digests and essentials. A wrapper can reach into storage for recent raw. Grep across TB of raw is not workable.

15. Layout decision (confirmed): a per-type "type pack" folder.
   - types/<type>/ holds type.yaml (baseline version, connection, retention, manual-to-version map), parser/, troubleshooting/, signatures, and manual manifests, so a troubleshooter needs one checkout. The registry keeps only per-serial instance facts and event logs.
   - Rule: type-level facts (same for every unit of a type) go in the type pack; per-serial facts go in the registry. The registry's schema CI checks each unit against its type pack (for example, that its declared version is one the type supports).
   - Why: parser and troubleshooting content change together (a new log format needs new signatures) and are needed together. If a type needs separate access or ownership, its folder can move to its own repo unchanged.
   - Cost accepted: the registry depends on the type packs for validation (cross-repo access to maintain), and reviewers of a type pack change must understand both parser code and type facts.

## Phases
1. Foundations (blocks the rest): sample logs from every type (versions, assay tags, sizes); define schemas (instrument.yaml, type.yaml, manifest, digest envelope); choose storage and hosting; confirm retention with data owners.
2. Skeleton (depends on 1): registry repo with schema CI (including validation against type packs) and add-an-instrument template (parallel with) platform repo with plugin contract, type-pack template, test harness, scaffold command; storage with path convention, tiering, write-once.
3. Ingestion and reduction (depends on 2): pull/stage/checksum/store/manifest; parse to digest and essentials; retention job with tombstones; compare step (drift, unknown assay, reviewable instrument.yaml change); index builder and reconcile job.
4. Pilot, UI, scale (depends on 3): pilot on a small-log type, a huge-log type, and a manual-export type; dashboard (fleet versions, drift, unknown assays, storage per type); contributor guide for teams.

## Verification
1. Ingest a file twice: one stored copy, one manifest entry.
2. Delete the index and rebuild from manifests: result matches.
3. Unknown log format: raw kept, flag raised.
4. Retention run: raw deleted only after verified parse, tombstone written.
5. PR that breaks the schema is rejected by CI.
6. Change a declared version in a test instrument: scan flags drift and produces a commit with evidence.
7. Result with an assay missing from the registry: ingested and flagged.
8. Change a nickname or category: no key or path changes.
9. Simulated 10 TB/month load: ingest throughput and tiering hold.
10. Portability check: delete every index, dashboard, and search cache, then rebuild from the files alone. Nothing may be lost.
11. Every data file has a schema_version and can be read with standard tools (no vendor software).
12. Pilot troubleshooting: replay one real past incident per pilot type. The signature catalog and manual index should lead a person to the documented fix.
13. A generated documentation copy is stamped with its commit, and a direct edit to it is flagged by the drift check.

## Open items
- Storage and hosting choice (S3-compatible suggested; nothing constrains it yet).
- Whether each type's logs contain software version and assay ID/version (Phase 1 discovery).
- Per-type retention periods and owner approvals.
- Assay reference source and sync method; assay tag format.
- Access control per type or team.
- Dashboard scope and tooling.
- Decide whether logs or manuals may be sent to external AI services (proprietary data policy).
- Manual redistribution rights and where manual binaries live.
- Pack format for small-file runs (e.g., tar.zst) and the file-count limits of the chosen storage.
- Who writes and reviews signature catalogs and resolution records.
