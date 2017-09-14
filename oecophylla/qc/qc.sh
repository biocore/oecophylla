#!/bin/bash
set -e

echo -n "Executing $0... "
conda env create --name shotgun-qc -f shotgun-qc.yaml --quiet
