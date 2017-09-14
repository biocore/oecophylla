#!/bin/bash

# deletes all oecophylla conda environments
for e in `conda-env list | awk '{print $1}' | grep oecophylla`; do
  echo "removing conda env $e"
  source deactivate
  conda-env remove --quiet --yes --name $e > /dev/null ;
done
