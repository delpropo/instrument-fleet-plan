# instrument-fleet-plan

Planning notes for the instrument fleet data platform. See `local/` for the problem statement.

See the [example instrument registry](examples/Instrument-Registry/README.md) for
fictional per-unit records, naming conventions, and a generated master instrument list.

## Environment setup (WSL + conda)

All commands run in WSL (Ubuntu), not in Windows PowerShell. The repo is at
`/mnt/c/Users/delpr/github/instrument-fleet-plan`. Conda is installed at `~/miniconda3` and is not on PATH by default.

### Use the environment

```bash
~/miniconda3/bin/conda init bash   # once, then restart the shell
conda activate instrument-fleet-plan
```

### Recreate it from scratch

```bash
cd /mnt/c/Users/delpr/github/instrument-fleet-plan
conda env create -f environment.yml
```

If this fails with `CondaToSNonInteractiveError`, conda is checking the Anaconda `defaults` channels even though
`environment.yml` uses `nodefaults`. Either:

- accept the Terms of Service yourself (only if you agree to them):
  ```bash
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
  ```
- or bypass `defaults` by creating the environment directly (this is how it was first built):
  ```bash
  conda create -n instrument-fleet-plan --override-channels -c conda-forge python=3.12 pip -y
  ```

`conda env create` does not accept `--override-channels`/`-c`; those only work with `conda create`.

### Adding packages

1. Add the package to `dependencies:` in `environment.yml` (use `pip:` for PyPI-only packages).
2. Apply it: `conda env update -n instrument-fleet-plan -f environment.yml --prune`
3. Commit the updated `environment.yml`.

Keep `environment.yml` as the source of truth; do not install packages ad hoc without recording them there.

### Remove the environment

```bash
conda env remove -n instrument-fleet-plan
```
