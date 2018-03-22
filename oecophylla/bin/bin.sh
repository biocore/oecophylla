#!/bin/bash
set -e

conda env create --name oecophylla-bin -f bin.yaml --quiet > /dev/null
