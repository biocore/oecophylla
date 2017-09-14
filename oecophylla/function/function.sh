#!/bin/bash
set -e

conda env create --name shotgun-humann2 -f shotgun-humann2.yaml --quiet > /dev/null
