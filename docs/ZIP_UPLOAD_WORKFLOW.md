# ZIP Upload Workflow

GitHub does not automatically extract uploaded ZIP archives. The repository therefore uses `.github/workflows/zip-ingest.yml` as a small bootstrap installer.

## One-time bootstrap

Create `.github/workflows/zip-ingest.yml` in the repository using the version included in this project archive. After it exists, the normal workflow is:

1. Upload a root-level project ZIP, for example `masterpiece_ai_v0_2.zip`.
2. GitHub Actions detects the changed ZIP.
3. The workflow extracts it, unwraps a single outer folder when present, and installs the files at repository root.
4. Existing non-ZIP project files are removed first.
5. The uploaded ZIP archives are preserved.
6. The bootstrap workflow itself is preserved.
7. The expanded project is committed and pushed automatically.

Only one root-level ZIP should be uploaded per commit.

## Important

The first bootstrap cannot be performed by the ZIP alone because GitHub only executes workflow files already present under `.github/workflows/`. Once the bootstrap workflow is installed, future project updates can be delivered as ZIP-only uploads.
