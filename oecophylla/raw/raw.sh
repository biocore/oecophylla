#!/bin/bash
set -e

conda env create --name oecophylla-raw -f raw.yaml --quiet > /dev/null
