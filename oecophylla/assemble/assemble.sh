#!/bin/bash
set -e

conda env create --name oecophylla-assemble -f assemble.yaml --quite > /dev/null
