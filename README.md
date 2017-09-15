<img src="https://raw.githubusercontent.com/wasade/oecophylla/assets/assets/oecophylla.png">

[![Build Status](https://travis-ci.org/biocore/oecophylla.svg?branch=master)](https://travis-ci.org/biocore/oecophylla)

# Oecophylla

Canonically pronounced *ee-co-fill-uh*, it is a Snakemake wrapper for shotgun sequence analysis.

## Installation

To install the workflow environment, run `bash install.sh` from the `oecophylla` directory.

## Test data execution

To speed development, Travis is currently only testing the validity
of the module installs and checking the snakefiles syntax, by using the `--dryrun` option in snakemake:

```
snakemake all --cores 2 --configfile config.yaml --dryrun
```

To run actual tools on a simple set of test data, run:

```bash
source activate oecophylla

snakemake all --cores 2 --configfile config.yaml
```

## Philosophy

**Oecophylla** is a metagenomics workflow tool that wraps software for quality filtering, taxonomic and functional analysis, and assembly of metagenomes. The user provides these inputs:

* demultiplexed sequence files (Illumina)
* a sample sheet (Illumina)
* a parameters file
* an environments file

From these, Oecophylla generates a configuration file for Snakemake, which passes parameters to software tools (defined by modules) for the following outputs:

* sequence quality control and trimming/filtering
* taxonomic analysis
* functional analysis
* assembly of metagenomes
* mapping and binning of contigs
* assembly analysis

The software tools carrying out each of the steps are as follows:

#### I. Quality control

* [MultiQC](http://multiqc.info)
* [Atropos]()

#### II. Taxonomic analysis

* [Kraken](https://ccb.jhu.edu/software/kraken/)
* [MetaPhlAn2](http://huttenhower.sph.harvard.edu/metaphlan2)
* [Shogun]()

#### III. Functional analysis

* [HUMAnN2](http://huttenhower.sph.harvard.edu/humann2)
* [Shogun]()

#### IV. Assembly

##### A. Contig assembly

* [MetaSPAdes](http://bioinf.spbau.ru/en/metaspades)
* [Megahit](http://www.metagenomics.wiki/tools/assembly/megahit)
* [Quast](http://bioinf.spbau.ru/quast)

##### B. Mapping and binning

* [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml)
* [Maxbin](https://sourceforge.net/projects/maxbin)

##### C. Assembly analysis

* [Anvi'o](http://merenlab.org/software/anvio)

