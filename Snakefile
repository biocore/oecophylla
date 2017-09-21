import os
import tempfile


try:
    TMP_DIR_ROOT = config['tmp_dir_root']
    samples = config["samples"]
    trimmer = config["trimmer"]
except KeyError:
    print('Error: you must pass a config file using --configfile')
    raise

include: "oecophylla/util/folders.rule"

include: "oecophylla/raw/raw.rule"
include: "oecophylla/qc/qc.rule"
include: "oecophylla/util/clean.rule"
include: "oecophylla/util/test.rule"
include: "oecophylla/util/util.rule"
include: "oecophylla/util/simplify_fasta.rule"
include: "oecophylla/distance/mash.rule"
include: "oecophylla/distance/sourmash.rule"
include: "oecophylla/assemble/assemble.rule"
# include: "oecophylla/map/map.rule"
include: "oecophylla/bin/bin.rule"
# include: "oecophylla/anvio/anvio.rule"
include: "oecophylla/taxonomy/taxonomy.rule"
# include: "oecophylla/function/function.rule"
# include: "oecophylla/report/report.rule"

rule all:
    input:
        # raw
        rules.raw.input,
        # QC
        rules.qc.input,
        # Assembly
        rules.assemble.input,
        # Distance
        rules.mash.input,
        rules.sourmash.input,
        # Taxonomy
        rules.taxonomy.input
