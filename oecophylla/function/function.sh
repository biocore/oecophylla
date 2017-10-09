#!/bin/bash
set -e

conda env create --name oecophylla-humann2 -f oecophylla-humann2.yaml --quiet > /dev/null

if conda env list | grep -q '^oecophylla-shogun\s'
then
  conda env create --name oecophylla-shogun -f ../taxonomy/oecophylla-shogun.yaml --quiet > /dev/null
fi
