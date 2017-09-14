#!/bin/bash
set -e

conda env create --name oecophylla-map -f map.yaml --quite > /dev/null
