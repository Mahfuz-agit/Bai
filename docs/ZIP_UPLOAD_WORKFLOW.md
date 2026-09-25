# ZIP Upload Workflow

Upload a project ZIP at repository root. `zip-ingest.yml` preserves itself, extracts the archive, removes old project files, then commits with `GH_PAT`.

The `GH_PAT` repository secret must be a classic PAT with `repo` and `workflow` scopes.
