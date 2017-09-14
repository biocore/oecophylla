#!/bin/bash
set -e

function cleanup {
  if [[ $? != 0 ]]; 
  then
      echo "failed."
  fi
}
trap cleanup EXIT

# runs setup of base environment and database installs

# create core conda env
conda env create --name oecophylla -f environment.yml --quiet > /dev/null

for f in $(find oecophylla -name "*.sh" -type f -print)
do
    pushd $(dirname $f)  > /dev/null
    base=$(basename $f)
    
    echo -n "Executing $f... "
    elapsed_time=$(/usr/bin/time -f "%E" bash ${base} 2>&1 > /dev/null)
    echo "completed in ${elapsed_time}."
    
    popd > /dev/null 
done
