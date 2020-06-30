#!/bin/bash
#
# In addition to verify-links.sh, this script additionally check anchors.

ROOT=$(unset CDPATH && cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
cd $ROOT

if ! which remark &>/dev/null; then
    sudo npm install -g remark-cli remark-lint breeswish/remark-lint-pingcap-docs-anchor
fi

echo "info: checking links anchors under $ROOT directory..."

remark --ignore-path .gitignore -u lint -u remark-lint-pingcap-docs-anchor . --frail --quiet
