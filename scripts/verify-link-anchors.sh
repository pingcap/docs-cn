#!/bin/bash
#
# In addition to verify-links.sh, this script additionally check anchors.
#
# See https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally if you meet permission problems when executing npm install.

ROOT=$(unset CDPATH && cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
cd $ROOT

REMARK_CMD=()
if [ -x "$ROOT/node_modules/.bin/remark" ]; then
  # Prefer the repo-local pinned version (installed by `npm ci`).
  REMARK_CMD=("$ROOT/node_modules/.bin/remark")
elif command -v remark >/dev/null 2>&1; then
  # Fall back to a globally-installed version (less reproducible).
  REMARK_CMD=(remark)
else
  REMARK_CMD=(npx --no-install remark)
fi

echo "info: checking links anchors under $ROOT directory..."

"${REMARK_CMD[@]}" \
  --ignore-path .gitignore \
  --ignore-pattern '.*/**' \
  -u lint \
  -u @breeswish-org/remark-lint-pingcap-docs-anchor \
  . \
  --frail \
  --quiet
