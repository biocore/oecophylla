#!/bin/bash
set -e

echo -n "Executing $0... "
conda env create --name shotgun-humann2 -f shotgun-humann2.yaml --quiet
