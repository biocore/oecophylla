#!/bin/bash
set -e

function cleanup {
  if [[ $? != 0 ]]; 
  then
      echo "failed."
  fi
}
trap cleanup EXIT

# runs setup of base environment

# create core conda env
conda env create --name oecophylla -f environment.yml

source activate oecophylla

pip install -e .
