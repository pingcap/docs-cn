#!/bin/bash

set -e
# test passed for pandoc 3.11.1

# Generate html with pandoc

# Get current branch name
branch_name=$(git rev-parse --abbrev-ref HEAD)

# reg pattern for branch name
regex="release-([0-9]+\.[0-9]+)"
if [[ $branch_name =~ $regex ]]; then
    version="v${BASH_REMATCH[1]}"
else
    version="latest"
fi

date="$(date '+%Y%m%d')"
output_name="tidb-${version}-zh-manual.html"
MAINFONT="--apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'"
MONOFONT="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

pandoc \
  -N \
  --toc \
  --section-divs=true \
  -f gfm+gfm_auto_identifiers+attributes \
  -t html \
  -M document-css=true \
  --template=templates/html/template.html \
  --css=templates/html/header-print.css \
  --embed-resources=true \
  --columns=120 \
  -V author-meta="PingCAP Inc." \
  -V date-meta="${date}" \
  -V title-prefix="PingCAP" \
  -V page-prefix="TiDB ${version} 中文手册" \
  -V title="TiDB 中文手册" \
  -V author="PingCAP Inc." \
  -V date="${version}" \
  -V toc-title="目录" \
  -V mainfont="${MAINFONT}" \
  -V monofont="${MONOFONT}" \
  -V maxwidth=60em \
  -V include-after="$(cat templates/html/copyright.html)" \
  -s \
  -o .build/${output_name} \
  .build/gfm-doc.md
