import os
import tempfile

configfile: "config.yaml"

ENV = config["env"]

shell.prefix("set +u; " + ENV + "; set -u; ")

TMP_DIR_ROOT = config['tmp_dir_root']

samples = config["samples"]

trimmer = config["trimmer"]

snakefiles = os.path.join(config["software"]["snakemake_folder"],
                          "bin/snakefiles/")

include: snakefiles + "util/simplify_fasta.py"

include: snakefiles + "raw/raw.py"
include: snakefiles + "qc/qc.py"
include: snakefiles + "mash/mash.py"
include: snakefiles + "assemble/assemble.py"
include: snakefiles + "map/map.py"
include: snakefiles + "bin/bin.py"
include: snakefiles + "anvio/anvio.py"
include: snakefiles + "tax/tax.py"
include: snakefiles + "function/function.py"
include: snakefiles + "report/report.py"
include: snakefiles + "util/folders.py"
include: snakefiles + "util/cleanv"
include: snakefiles + "util/test.py"
include: snakefiles + "util/util.py"


rule all:
    # raw
    input:
        raw_dir + "multiQC_per_file/multiqc_report.html",
        raw_dir + "multiQC_per_sample/multiqc_report.html",
    # QC
        expand(qc_dir + "{sample}/{trimmer}_trimmed/{sample}.trimmed.R1.fastq.gz", sample=samples, trimmer=trimmer),
        expand(qc_dir + "{sample}/{trimmer}_trimmed/{sample}.trimmed.R2.fastq.gz", sample=samples, trimmer=trimmer),
        expand(qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz", sample=samples),
        expand(qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz", sample=samples),
        qc_dir + "multiQC_per_sample/multiqc_report.html",
    # Assembly
        expand(assemble_dir + "{sample}/{assembler}/{sample}.contigs.fa",
               sample=samples, assembler=config['assemblers']),
        expand(assemble_dir + "{sample}/metaquast/{sample}.metaquast.done",
               sample=samples),
        expand(assemble_dir + "{sample}/quast/{sample}.quast.done",
               sample=samples),
    # Mapping
        # expand(map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.cram",
        #        sample=samples, bin_sample=config['binning_samples'],
        #        abund_sample=config['abundance_samples']),
    # Binning
        expand(bin_dir + "{bin_sample}/maxbin/{bin_sample}.summary",
               bin_sample=config['binning_samples']),
        expand(bin_dir + "{bin_sample}/abundance_files.tar.gz",
               bin_sample = config['binning_samples']),
    # Anvio
        expand(anvio_dir + "{bin_sample}/{bin_sample}_samples-summary_CONCOCT.tar.gz",
               bin_sample=config['binning_samples']),
        expand(anvio_dir + "{bin_sample}/{bin_sample}.db.anvi_add_maxbin.done",
               bin_sample=config['binning_samples']),
    # Taxonomy
        tax_dir + "metaphlan2/joined_taxonomic_profile.tsv",
        tax_dir + "kraken/combined_profile.tsv",
        tax_dir + "shogun/combined_profile.tsv",
    # Function
        expand(# individual normed bioms
               func_dir + "{sample}/humann2/{sample}_genefamilies_{norm}.biom",
               norm = config['params']['humann2']['norms'],
               sample = samples),
        expand(# stratified
               func_dir + "humann2/stratified/combined_genefamilies_{norm}_{mapped}_unstratified.biom",
               norm = config['params']['humann2']['norms'],
               mapped=['all','mapped']),
    # Mash
        expand(mash_dir + '{sample}/mash/{sample}.msh',
               sample=samples),
        expand(mash_dir + '{sample}/mash/{sample}.refseq.txt',
               sample=samples),
        mash_dir + 'combined_analysis/mash.dist.dm',
        mash_dir + 'combined_analysis/mash.dist.p'
