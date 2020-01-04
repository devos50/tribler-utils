#!/bin/bash

SUBMODULE_PATHS=$(git submodule --quiet foreach git rev-parse --show-toplevel)
for f in $(find . -type f -name "*.rst")
do
  full_path_file="$(readlink -f $f)"
  in_subfolder="false"
  for p in $SUBMODULE_PATHS
  do
    full_path_folder="$(readlink -f $p)"
    if [[ $full_path_file == $full_path_folder* ]]
    then
      in_subfolder="true"
    fi
  done
  if [[ $in_subfolder == "false" ]]
  then
    unknowns="$(aspell list < $f | sort -u)"
    if [[ $unknowns ]]
    then
      echo ">> Unknown words in $f:"
      echo $unknowns
    fi 
  fi
done
