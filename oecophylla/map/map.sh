#!/bin/bash
set -e

conda env create --name shotgun-map -f map.yaml --quite > /dev/null
