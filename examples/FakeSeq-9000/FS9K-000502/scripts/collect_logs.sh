#!/usr/bin/env bash
# Pull raw logs from this instrument into a staging directory. Dry run unless --run is given.
# Usage: collect_logs.sh [--run] [--source SRC] [--dest DIR]
#   --source  override the remote path (default is built from instrument.yaml); a local directory works for testing
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTRUMENT_DIR="$(dirname "$HERE")"
RUN=0
SOURCE=""
DEST="$INSTRUMENT_DIR/staging"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run) RUN=1; shift ;;
    --source) SOURCE="$2"; shift 2 ;;
    --dest) DEST="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

yaml_get() { python -c "import sys,yaml;d=yaml.safe_load(open(sys.argv[1]))['connection'];print(d[sys.argv[2]])" "$INSTRUMENT_DIR/instrument.yaml" "$1"; }

if [[ -z "$SOURCE" ]]; then
  SOURCE="$(yaml_get username)@$(yaml_get hostname):$(yaml_get log_path)"
fi

mkdir -p "$DEST"
OPTS=(-a --itemize-changes --checksum)
[[ $RUN -eq 0 ]] && OPTS+=(--dry-run) && echo "DRY RUN (use --run to copy)"

# Raw files are copied as-is and never modified; existing files are skipped so re-runs are idempotent.
rsync "${OPTS[@]}" --ignore-existing "$SOURCE" "$DEST/"
