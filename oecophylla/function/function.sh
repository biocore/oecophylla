#!/bin/bash
set -e

conda env create --name oecophylla-humann2 -f oecophylla-humann2.yaml --quiet > /dev/null

# Create the SHOGUN environment only if it hasn't already been created by the taxonomy module.
if ! conda env list | grep -q '^oecophylla-shogun\s'
then
  conda env create --name oecophylla-shogun -f ../taxonomy/oecophylla-shogun.yaml --quiet > /dev/null
  source activate oecophylla-shogun
  cd $CONDA_PREFIX/bin
  wget https://github.com/knights-lab/UTree/releases/download/v2.0c/utree-search_gg
  chmod 755 utree-search_gg
  wget https://github.com/knights-lab/BURST/releases/download/v0.99.4a/burst_linux_DB15
  chmod 755 burst_linux_DB15
fi
