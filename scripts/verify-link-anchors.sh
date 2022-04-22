#!/bin/bash
#
# In addition to verify-links.sh, this script additionally check anchors.
#
# See https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally if you meet permission problems when executing npm install.

ROOT=$(unset CDPATH && cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
cd $ROOT

yarn add remark-cli@9.0.0 remark-lint@8.0.0 @breeswish-org/remark-lint-pingcap-docs-anchor@1.1.1

echo "info: checking links anchors under $ROOT directory..."

yarn remark --ignore-path .gitignore -u lint -u @breeswish-org/remark-lint-pingcap-docs-anchor . --frail --quiet
