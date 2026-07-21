#!/bin/bash

echo $PWD

DuplicateFilename=$(
  find . \
    -path './node_modules' -prune -o \
    -name '*.md' \
    ! -name '_*.md' \
    ! -name 'SKILL.md' \
    ! -name 'README.md' \
    -print | rev | cut -d'/' -f1 | rev | sort | uniq -c -d
)

if [ -z "$DuplicateFilename" ]
then
  echo "No Duplicate Filenames"
else
  echo $DuplicateFilename
  exit 1
fi