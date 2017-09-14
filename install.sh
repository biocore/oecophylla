#!/bin/bash
set -e

# runs setup of base environment and database installs

# create core conda env
conda env create --name oecophylla -f environment.yml

for f in $(find oecophylla -name "*.sh" -type f -print)
do
    bash $f
done
