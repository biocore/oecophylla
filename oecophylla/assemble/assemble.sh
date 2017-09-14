#!/bin/bash
set -e

conda env create --name shotgun-assemble -f assemble.yaml --quite > /dev/null
