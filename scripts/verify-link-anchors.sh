#!/bin/bash
#
# In addition to verify-links.sh, this script additionally check anchors.
#
# See https://github.com/glenpike/npm-g_nosudo if you meet permission problems when executing npm install.

ROOT=$(unset CDPATH && cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
cd $ROOT

npm install -g remark-cli remark-lint breeswish/remark-lint-pingcap-docs-anchor

echo "info: checking links anchors under $ROOT directory..."

remark --ignore-path .gitignore -u lint -u remark-lint-pingcap-docs-anchor . --frail --quiet
