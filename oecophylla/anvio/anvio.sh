#!/bin/bash
set -e

conda env create --name oecophylla-anvio -f anvio.yaml --quiet > /dev/null
