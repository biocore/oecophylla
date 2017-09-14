#!/bin/bash
set -e

# runs setup of base environment and database installs

# create core conda env
conda env create --name oecophylla -f environment.yml

for f in $(find oecophylla -name "*.sh" -type f -print)
do
    elapsed_time=$(/usr/bin/time -f "%E" bash $f)
    echo "completed in ${elapsed_time} seconds."
done
