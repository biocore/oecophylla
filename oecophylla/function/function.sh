#!/bin/bash
set -e

echo "Executing $0..."
conda env create --name shotgun-humann2 -f shotgun-humann2.yaml --quiet
