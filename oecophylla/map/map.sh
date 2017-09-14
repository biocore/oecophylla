#!/bin/bash
set -e

conda env create --name oecophylla-map -f map.yaml --quiet > /dev/null
