#!/bin/bash
set -e

echo -n "Executing $0... "
conda env create --name shotgun-map -f map.yaml --quiet
