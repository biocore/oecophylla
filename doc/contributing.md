# Contributing a module to *Oecophylla*

A module is a set of related Snakemake rules, along with installation instructions. 

To contribute a new module *foo*, you need a folder in `./oecophylla` that contains:

 1. **foo.rule**: a Snakemake-formatted file containing the rules for the module
 2. **foo.yaml**: a Conda environment file for installing dependencies for the module
 3. **foo.sh**: a Bash script for installing the module
 4. **README.md**: a Markdown file describing the steps performed by the module