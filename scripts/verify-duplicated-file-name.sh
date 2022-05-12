#!/bin/bash

echo $PWD

DuplicateFilename=$(find . -name '*.md' ! -name '_*.md'  | rev | cut -d'/' -f1 | rev | sort | uniq -c -d)

if [ -z "$DuplicateFilename" ]
then
  echo "No Duplicate Filenames"
else
  echo $DuplicateFilename
  exit 1
fi