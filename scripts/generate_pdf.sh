#!/bin/bash

set -e
# test passed in pandoc 1.19.1

MAINFONT="WenQuanYi Micro Hei"
MONOFONT="WenQuanYi Micro Hei Mono"

# MAINFONT="Tsentsiu Sans HG"
# MONOFONT="Tsentsiu Sans Console HG"

#_version_tag="$(date '+%Y%m%d').$(git rev-parse --short HEAD)"
_version_tag="$(date '+%Y%m%d')"

# default version: `pandoc --latex-engine=xelatex doc.md -s -o output2.pdf`
# used to debug template setting error

# add docs versions
# generate PDF for each version
docs_versions=(dev v3.0 v2.1) 

for i in "${docs_versions[@]}"
do
   echo "$i"
   version="$i/doc.md"
   echo "$version"
   output_path="$i/output.pdf"

   pandoc -N --toc --smart --latex-engine=xelatex \
    --template=templates/template.tex \
    --listings \
    --columns=80 \
    -V title="TiDB 中文手册" \
    -V author="PingCAP Inc." \
    -V date="${_version_tag}" \
    -V CJKmainfont="${MAINFONT}" \
    -V mainfont="${MAINFONT}" \
    -V sansfont="${MAINFONT}" \
    -V monofont="${MONOFONT}" \
    -V geometry:margin=1in \
    -V include-after="\\input{templates/copyright.tex}" \
    $version -s -o $output_path
done