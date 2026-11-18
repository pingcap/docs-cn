#!/bin/bash
#
# In addition to verify-links.sh, this script additionally check anchors.
#
# Install the pinned local tools with `npm ci --ignore-scripts --include=dev`.

ROOT=$(unset CDPATH && cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT" || exit 1

# Require the repo-local version installed from package-lock.json.
if [ ! -x "$ROOT/node_modules/.bin/remark" ]; then
    echo "error: local remark is missing or not executable. Run npm ci --ignore-scripts --include=dev." >&2
    exit 1
fi
REMARK_CMD=("$ROOT/node_modules/.bin/remark")

echo "info: checking links anchors under $ROOT directory..."

"${REMARK_CMD[@]}" \
  --ignore-path .gitignore \
  --ignore-pattern '.*/**' \
  -u lint \
  -u @breeswish-org/remark-lint-pingcap-docs-anchor \
  . \
  --frail \
  --quiet
