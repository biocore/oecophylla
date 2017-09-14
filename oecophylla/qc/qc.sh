#!/bin/bash
set -e

conda env create --name oecophylla-qc -f oecophylla-qc.yaml --quite > /dev/null
