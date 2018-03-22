import yaml
import os
import tempfile

try:
    TMP_DIR_ROOT = config['tmp_dir_root']
    samples = config["samples"]
    trimmer = config['params']["trimmer"]
except KeyError:
    print('Error: you must pass a config file using --configfile')
    raise


# import mapping/binning yaml if present in params

try:
    with open(config['params']["binning_config"]) as f:
        bin_config = yaml.load(f)
    if bin_config is not None:
        mapping = True
except:
    mapping = False
    bin_config = {}


include: "oecophylla/util/folders.rule"

include: "oecophylla/qc/qc.rule"
include: "oecophylla/util/clean.rule"
include: "oecophylla/util/util.rule"
include: "oecophylla/util/simplify_fasta.rule"
include: "oecophylla/distance/distance.rule"
include: "oecophylla/assemble/assemble.rule"
include: "oecophylla/map/map.rule"
# include: "oecophylla/bin/bin.rule"
# include: "oecophylla/anvio/anvio.rule"
include: "oecophylla/taxonomy/taxonomy.rule"
include: "oecophylla/function/function.rule"
# include: "oecophylla/report/report.rule"

# execute the basic filesystem read combine locally, not as submitted job
localrules: raw_combine_files

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
        rules.taxonomy.input,
        # Function
        rules.function.input,
        # Map
        rules.map.input