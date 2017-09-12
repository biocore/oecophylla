#!/bin/bash

# runs setup of base environment and database installs

# create core conda env
# conda env create --name oecophylla -f environment.yml

find oecophylla -name "*.sh" -execdir bash {} \;

