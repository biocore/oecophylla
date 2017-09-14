#!/bin/bash

# deletes all oecophylla conda environments
for e in `conda-env list | grep oecophylla | awk '{print $1}'`; do
  conda-env remove --quiet --yes --name $e > /dev/null ;
done
