<img src="https://raw.githubusercontent.com/wasade/oecophylla/assets/assets/oecophylla.png">

[![Build Status](https://travis-ci.org/biocore/oecophylla.svg?branch=master)](https://travis-ci.org/biocore/oecophylla)

# Oecophylla

Canonically pronounced *ee-co-fill-uh*, Oecophylla is a Snakemake wrapper for shotgun sequence analysis.

## Installation

To install the workflow environment, run `bash install.sh` from the `oecophylla` directory.

## Test data execution

To speed development, Travis is currently only testing the validity of the module installs and checking the snakefiles syntax, by using the `--dryrun` option in Snakemake:

```
snakemake all --cores 2 --configfile config.yaml --dryrun
```

To run actual tools on a simple set of test data, run:

```bash
source activate oecophylla

oecophylla workflow --test
```

To run a particular module on test data, run:

```bash
source activate oecophylla

oecophylla workflow --test MODULE
```

## Philosophy

**Oecophylla** is a metagenomics workflow tool that wraps software for quality filtering, taxonomic and functional analysis, and assembly of metagenomes. The user provides these inputs:

* demultiplexed sequence files (Illumina)
* a sample sheet (Illumina)
* a parameters file
* an environments file

From these, Oecophylla generates a configuration file for Snakemake, which passes parameters to software tools (defined internally by modules) for the following outputs:

* sequence quality control and trimming/filtering
* taxonomic analysis
* functional analysis
* assembly of metagenomes
* mapping and binning of contigs
* assembly analysis

The software tools carrying out each of the steps are as follows:

#### I. Quality control

* [MultiQC](http://multiqc.info) - aggregates QC results from several tools
* [Atropos](https://github.com/jdidion/atropos) - read trimming and filtering

#### II. Taxonomic analysis

* [Kraken](https://ccb.jhu.edu/software/kraken/) - k-mer based taxonomic assignment of reads
* [MetaPhlAn2](http://huttenhower.sph.harvard.edu/metaphlan2) - marker gene based taxonomic assignment of reads
* [Shogun](https://github.com/knights-lab/shogun) - shallow shotgun taxonomic and functional profiling

#### III. Functional analysis

* [HUMAnN2](http://huttenhower.sph.harvard.edu/humann2) - gene family and pathway abundance (with taxonomic stratification) of reads
* [Shogun](https://github.com/knights-lab/shogun) - shallow shotgun taxonomic and functional profiling

#### IV. Assembly

##### A. Contig assembly

* [MetaSPAdes](http://bioinf.spbau.ru/en/metaspades) - metagenomic assembler
* [Megahit](http://www.metagenomics.wiki/tools/assembly/megahit) - metagenomic assembler

##### B. Mapping reads to contigs

* [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml) - fast and memory-efficient tool for aligning sequencing reads to long reference sequences

##### C. Binning contigs

* [Maxbin](https://sourceforge.net/projects/maxbin) - binning tool using an Expectation-Maximization algorithm

##### D. Analysis of assemblies and bins

* [Quast](http://bioinf.spbau.ru/quast) - evaluation of genome assemblies with or without reference genome
* [Anvi'o](http://merenlab.org/software/anvio) - analysis and visualization platform for 'omics data

<!--
##### D. (cont.)
* ["bin the bins" tool to be determined]

##### E. Downstream genome annotation
* [Prokka]() - gene calling and annotation
* []() - metabolic reconstruction
* []() - molecule prediction
-->
