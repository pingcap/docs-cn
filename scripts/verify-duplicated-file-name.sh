#!/bin/bash

echo $PWD

DuplicateFilename=$(awk -F'/' '{
  f = $NF
  a[f] = f in a? a[f] RS $0 : $0
  b[f]++ }
  END{for(x in b)
        if(b[x]>1)
          printf "Duplicate Filename: %s\n%s\n",x,a[x] }' <(find . ! -path '*/.git/*' ! -path '*/media/*' ! -name '_*.md' -type f ))

if [ -z "$DuplicateFilename" ]
then
  echo "No Duplicate Filenames"
else
  echo $DuplicateFilename
  exit 1
fi