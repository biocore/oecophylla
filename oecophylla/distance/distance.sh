#!/bin/bash
set -e

conda env create --name oecophylla-distance -f oecophylla-distance.yaml --quiet > /dev/null
