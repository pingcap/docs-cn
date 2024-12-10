#!/bin/bash

set -e
# test passed for pandoc 3.11.1

pandoc \
  -f gfm+gfm_auto_identifiers \
  -t gfm+gfm_auto_identifiers-yaml_metadata_block \
  -o .build/gfm-doc-pre.md \
  .build/full-doc.md
