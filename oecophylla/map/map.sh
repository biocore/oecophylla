#!/bin/bash
set -e

echo "Executing $0..."
conda env create --name shotgun-map -f map.yaml --quiet
