#!/bin/bash

echo "<html><body><h1>List of unknown words per file</h1>"
echo "<ul>"

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
      count=$(tr -cd " \n" <<< $unknowns | wc -c)
      echo "<li>$f ($count)</li>"
      echo "<ul>"
      echo "<li>"
      echo "$(sed 's/ /<\/li><li>/g' <<< $unknowns)"
      echo "</li>"
      echo "</ul>"
    fi 
  fi
done

echo "</ul>"
echo "</body></html>"
