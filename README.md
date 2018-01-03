<img src="https://raw.githubusercontent.com/wasade/oecophylla/assets/assets/oecophylla.png">

[![Build Status](https://travis-ci.org/biocore/oecophylla.svg?branch=master)](https://travis-ci.org/biocore/oecophylla)

# Oecophylla

Canonically pronounced *ee-co-fill-uh*, Oecophylla is a Snakemake wrapper for shotgun sequence analysis.

Rather than being a single monolithic tool, Oecophylla is composed of a series of **modules**, each of which performs a series of related tasks on the data---examples include `qc`, `assemble`, or `taxonomy`. These modules can be independently installed, and are easy to add or change if you want to try a new analysis on an existing data set.

Because Oecophylla is written using the Snakemake bioinformatics workflow system, it inherits many of that tool's advantages, including reproducible execution, automatic updating of downstream steps after upstream modifications, and cluster-enabled parallel execution. To learn more about Snakemake, please read [the documentation](https://snakemake.readthedocs.io). 


## Documentation

You can find instructions on installation and use of Oecophylla at the 
[ReadTheDocs.io documentation](http://oecophylla.readthedocs.io).
