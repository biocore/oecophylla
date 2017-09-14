#!/bin/bash
set -e

echo "Executing $0..."
conda env create --name shotgun-qc -f shotgun-qc.yaml --quiet
