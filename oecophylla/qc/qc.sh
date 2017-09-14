#!/bin/bash
set -e

conda env create --name shotgun-qc -f shotgun-qc.yaml --quite > /dev/null
