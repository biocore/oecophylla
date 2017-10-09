<img src="https://raw.githubusercontent.com/wasade/oecophylla/assets/assets/oecophylla.png">

[![Build Status](https://travis-ci.org/biocore/oecophylla.svg?branch=master)](https://travis-ci.org/biocore/oecophylla)

# Oecophylla

Canonically pronounced *ee-co-fill-uh*, Oecophylla is a Snakemake wrapper for shotgun sequence analysis.

Rather than being a single monolithic tool, Oecophylla is composed of a series of **modules**, each of which performs a series of related tasks on the data---examples include `qc`, `assemble`, or `taxonomy`. These modules can be independently installed, and are easy to add or change if you want to try a new analysis on an existing data set.

Because Oecophylla is written using the Snakemake bioinformatics workflow system, it inherits many of that tool's advantages, including reproducible execution, automatic updating of downstream steps after upstream modifications, and cluster-enabled parallel execution. To learn more about Snakemake, please read [the documentation](https://snakemake.readthedocs.io). 


## Installation

### Installing Oecophylla

To install the workflow environment, download the Oecophylla repository from GitHub:

```bash
git clone https://github.com/biocore/oecophylla.git
```

Then, run `bash install.sh` from the `oecophylla` directory.

This will execute the following commands: 

```bash
conda env create --name oecophylla -f environment.yml

source activate oecophylla

pip install -e .
```

### Installing modules

The code to execute module commands is all located in the Oecophylla repository. The actual tools called by these modules, however, must be installed separately in their own environemnts. 

Oecophylla can install these per-module environments automatically using Conda. To see a list of modules available to install, make sure you are in the Oecophylla conda environment, and then execute:

```bash
oecophylla install --avail
```

You can install all of these modules by executing:

```bash
oecophylla install all
```

Fair warning: installing all modules will take a  bit of time. 

To install a specific set of modules, you can specify them directly as positional arguments. For example:

```bash
oecophylla install qc taxonomy
```

will install the `qc` and `taxonomy` module Conda environments.

### Test data execution

We have included a minimal set of example data and test databases sufficient to execute a test run of the workflow. 

To run these test data, you will need to first install the test databases:

```bash
oecophylla install --tests
```

You can then run the test data on any module that you have installed, specifying only the desired output directory and the module to test:

```bash
oecophylla workflow --test -o test_out qc taxonomy
```

## Basic tutorial

For this tutorial, we'll analyze a pair of shallowly sequenced  microbiome samples distributed with the repository. They are located in `oecophylla/test_data/test_reads`.

This tutorial essentially duplicates the automatic execution of test data above, walking you through each step. 

### Gather inputs

We need three inputs to execute:

1. **Input reads directory**: `oecophylla/test_data/test_reads`
2. **Parameters file**: `oecophylla/test_data/params.yaml`
3. **Environment file**: `oecophylla/test_data/envs.yaml`

The *input reads* should be the gzipped raw demultiplexed Illumina reads, with filenames conforming to the Illumina bcl2fastq standard (e.g. sample_S102_L001_R1_001.fastq.gz). 

The *environment file* simply lists the commands necessary to invoke the correct environment for each module. The included example file specifies the commands necessary for the Oecophylla-installed Conda environments, but these can be changed if, for example, you have appropriate environments specified as modules on a cluster.

The *parameters file* specifies the parameters for each tool being executed, including paths to the relevant databases.

Information from these three files is combined by Oecophylla into a single `config.yaml` configuration file and placed in the output directory of a run. This serves as complete record of the settings chosen for execution of a run, as well as instructions for restarting or extending the processing on a dataset for subsequent invokations of Oecophylla. 

### Run QC with Oecophylla

To run a simple workflow, executing read trimming and QC summaries, run the following from the Oecophylla directory:

```
oecophylla workflow \
--input_dir test_data/test_reads \
--params test_data/params.yaml \
--envs test_data/envs.yaml \
--output_dir test_output qc
```
Then go get a cup of coffee. 

...

When you come back, you will find a directory called `test_output`. 

Inside of `test_output` will be the configuration file `config.yaml`.

Also inside of `test_output` will be a folder called `results`. This contains... well, you know.

Take a look at the file `test_out/results/qc/multiQC_per_sample/multiqc_report.html`. This is a portable HTML-based summary of the FastQC quality information from each of your samples. 

### Run additional modules

Now that you have initiated an Oecophylla run, you can call subsequent modules without providing paths for the three above inputs. Simply providing the output directory and module to execute will be enough: Oecophylla will find the config.yaml file in the output directory, and pick up where it left off. 

To continue with the `taxonomy` and `function` modules on the previous outputs, you can now simply run:

```bash
oecophylla workflow --output_dir test_output taxonomy function
```

Oecophylla will find the outputs from the `qc` module, using these cleaned reads as inputs to the next steps.

### Results

The `results` directory will contain a separate folder for each module in the analysis workflow. 

These modules each will list per-sample outputs---for example, trimmed reads or assembled contigs---in per-sample directories within the module directory. 

Combined outputs---for example, the MultiQC summaries or combined biom table taxonomic summaries---will be found in their own dictories within the primary module directory.