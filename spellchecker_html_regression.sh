#!/bin/bash

FAILURE=0

###
### Read command line args
### 
### In case of one arg:
###  compare given commit id with origin/devel
###
### In case of two args:
###  compare given commit ids with each other
###
if [[ $# -eq 0 ]]
then
  echo "Supply at least the reference commit to check"
  exit 1
fi

OLD_COMMIT="origin/devel"
NEW_COMMIT="$1"

if [[ $# -eq 2 ]]
then
  OLD_COMMIT="$1"
  NEW_COMMIT="$2"
fi

###
### Create HTML report
### 
### 1. Construct submodule paths
### 2. For each *.rst file f:
### 2.a. If f is not in any submodule folder:
### 2.a.i. Spellcheck it and add to the HTML if not empty
###

echo "<html><body><h1>List of unknown words per file</h1>"
echo "Comparing $OLD_COMMIT..$NEW_COMMIT:"
echo "<ul>"

SUBMODULE_PATHS=$(git submodule --quiet foreach git rev-parse --show-toplevel)
for f in $(find . -type f -name "*.rst")
do
  full_path_file="$(readlink -f $f)"
  in_subfolder="false"
  for p in $SUBMODULE_PATHS
  do
    full_path_folder=$(readlink -f $p)
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
      count="$(tr -cd " \n" <<< $unknowns | wc -c)"
      file_diff="$(git diff -U0 --no-color $OLD_COMMIT $NEW_COMMIT $f | grep "^+[^+]" --color=never | cut -c2-)"
      diff_unknowns="$(echo $file_diff | aspell list | sort -u)"
      intro_count=0
      list_out=""
      for word in $unknowns
      do
        # The diff contains unknown words
        if [[ $(grep -q -w $word <<< $diff_unknowns) ]]
        then
          old_words="$(git show $OLD_COMMIT:$f | aspell list | sort -u)"
          if [[ $(grep -q -w $word <<< $old_words) ]]
          then
            # We already know about this wrong spelling
            list_out="$list_out<li>$word</li>"
          else
            # This is a newly introduced unknown word
            let intro_count+=1
            FAILURE=1
            list_out="$list_out<li><b><big><font color="red">$word</font></big></b></li>"
          fi
        else
          list_out="$list_out<li>$word</li>"
        fi
      done
      # Construct the file summary
      if (( intro_count > 0 ))
      then
        echo "<li>$f ($count/<b><font color="red">+$intro_count</font></b>)</li>"
      else
        echo "<li>$f ($count)</li>"
      fi
      echo "<ul>"
      echo "$list_out"
      echo "</ul>"
    fi 
  fi
done

echo "</ul>"
echo "</body></html>"

exit $FAILURE
