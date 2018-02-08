Oecophylla Documentation
========================

Canonically pronounced *ee-co-fill-uh*, Oecophylla is a Snakemake wrapper for shotgun sequence analysis.

Rather than being a single monolithic tool, Oecophylla is composed of a series of **modules**, each of which performs a series of related tasks on the data---examples include `qc`, `assemble`, or `taxonomy`. These modules can be independently installed, and are easy to add or change if you want to try a new analysis on an existing data set.

Because Oecophylla is written using the Snakemake bioinformatics workflow system, it inherits many of that tool's advantages, including reproducible execution, automatic updating of downstream steps after upstream modifications, and cluster-enabled parallel execution. To learn more about Snakemake, please read `the documentation <https://snakemake.readthedocs.io>`__.


Oecophylla tutorials
====================

.. toctree::
   :caption: Basic installation instructions
   :maxdepth: 2

   oecophylla-install

.. toctree::
   :caption: Running on some test data
   :maxdepth: 2

   oecophylla-basic

.. toctree::
   :caption: More about input files
   :maxdepth: 2

   oecophylla-inputs

.. toctree::
   :caption: Cluster execution
   :maxdepth: 2

   oecophylla-cluster

.. toctree::
   :caption: How to contribute
   :maxdepth: 2

   oecophylla-contributing