#!/bin/bash
#
# This script is used to verify links in markdown docs.
#
# - External links are ignored in CI because these links may go down out of our contorl.
# - Anchors are ignored
# - Internal links conventions
#   - Links starting with '/media/' are relative to site root
#   - Links starting with one or two dots are relative to the directory in which files reside
#   - Other links are relative to the root of the version directory (e.g. v1.0, v2.0, v3.0)
# - When a file was moved, all other references are required to be updated for now, even if alias are given
#   - TODO relaxing this requirement?
#

ROOT=$(unset CDPATH && cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
cd $ROOT

if ! which markdown-link-check &>/dev/null; then
    sudo npm install -g markdown-link-check@3.7.3
fi

CONFIG_TMP=$(mktemp)

trap 'rm -f $CONFIG_TMP' EXIT

# TODO fix later
IGNORE_DIRS=(v1.0 v2.0 v2.1 v2.1-legacy)

function in_array() {
    local i=$1
    shift
    local a=("${@}")
    local e
    for e in "${a[@]}"; do
        [[ "$e" == "$i" ]] && return 0;
    done
    return 1
}

# Check all directories starting with 'v\d.*' and dev.
error_files=0
error_output=""
for d in dev $(ls -d v[0-9]*); do
    if in_array $d "${IGNORE_DIRS[@]}"; then
        echo "info: directory $d skipped"
        continue
    fi
    echo "info: checking links under $d directory..."
    sed \
        -e "s#<ROOT>#$ROOT#g" \
        -e "s#<DOC_ROOT>#$ROOT/$d#g" \
        scripts/markdown-link-check.tpl > $CONFIG_TMP
    cat $CONFIG_TMP
    for f in $(find "$d" -type f -name '*.md'); do
        echo markdown-link-check --config "$CONFIG_TMP" "$f" -q
        output=$(markdown-link-check --config "$CONFIG_TMP" "$f" -q)
        if [ $? -ne 0 ]; then
            ((error_files++))
            error_output+="$output"
        fi
        echo "$output"
    done
done

echo ""
if [ $error_files -gt 0 ]; then
    echo "error: $error_files files have invalid links (or alias links which are recommended to be replaced with latest one), please fix them!"
    echo ""
    echo "=== ERROR REPORT == ":
    echo "$error_output"
    exit 1
else
    echo "info: all files are ok!"
fi
