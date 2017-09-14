#!/bin/bash
set -e

conda env create --name oecophylla-assemble -f assemble.yaml --quiet > /dev/null
