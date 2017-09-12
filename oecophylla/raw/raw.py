rule raw_make_links:    
    """
    Makes symlinks from raw sequences files to the analysis directory.
    """
    input:
        forward = lambda wildcards: config["samples"][wildcards.sample]["forward"],
        reverse = lambda wildcards: config["samples"][wildcards.sample]["reverse"]
    output:
        touch(data_dir + "{sample}/{sample}_links.done")
    threads:
        1
    log:
        raw_dir + "logs/raw_make_links.sample=[{sample}].log"
    run:
        for f in input.forward + input.reverse:
            in_fp = os.path.realpath(f)
            out_fp = os.path.join(data_dir,
                                 wildcards.sample,
                                 os.path.basename(f))
            shell("ln -s {in_fp} {out_fp} 2> {log}")


rule raw_per_file_fastqc: 
    """
    Makes fastqc reports for each individual input file.
    """
    input:
        forward = lambda wildcards: config["samples"][wildcards.sample]["forward"],
        reverse = lambda wildcards: config["samples"][wildcards.sample]["reverse"]
    output:
        raw_dir + "{sample}/fastqc_per_file/{sample}_fastqc.done"
    threads:
        4
    log:
        raw_dir + "logs/raw_per_file_fastqc.sample=[{sample}].log"
    run:
        out_dir = os.path.dirname(output[0])
        in_fastqs = ' '.join(input.forward + input.reverse)
        shell("""
              fastqc --threads {threads} --outdir {out_dir} {in_fastqs} 2> {log} 1>&2

              touch {output}
              """)


rule raw_per_file_multiqc: 
    """
    Runs multiqc for set of individual input files.
    """
    input:
        expand(raw_dir + "{sample}/fastqc_per_file/{sample}_fastqc.done", sample=config['samples'])
    output:
        raw_dir + "multiQC_per_file/multiqc_report.html"
    threads:
        4
    log:
        raw_dir + "logs/raw_per_file_multiqc.log"
    run:
        out_dir = os.path.dirname(output[0])
        shell("multiqc -f -o {out_dir} {raw_dir}/*/fastqc_per_file 2> {log} 1>&2")


rule raw_combine_files:
    """
    Combines multiple input fastqs per sample into a temporary single fastq
    """
    input:
        forward = lambda wildcards: config["samples"][wildcards.sample]["forward"],
        reverse = lambda wildcards: config["samples"][wildcards.sample]["reverse"]
    output:
        forward = temp(raw_dir + "{sample}/combined_reads/{sample}.R1.fastq.gz"),
        reverse = temp(raw_dir + "{sample}/combined_reads/{sample}.R2.fastq.gz")
    threads:
        4
    log:
        raw_dir + "logs/raw_combine_files.sample=[{sample}].log"
    run:
        f_fastqs = ' '.join(input.forward)
        r_fastqs = ' '.join(input.reverse)
        shell("""
                cat {f_fastqs} > {output.forward} 2> {log}
                cat {r_fastqs} > {output.reverse} 2> {log}
              """)


rule raw_per_sample_fastqc: 
    """
    Makes fastqc reports for each individual input file.
    """
    input:
        forward = raw_dir + "{sample}/combined_reads/{sample}.R1.fastq.gz",
        reverse = raw_dir + "{sample}/combined_reads/{sample}.R2.fastq.gz"
    output:
        html = raw_dir + "{sample}/fastqc_per_sample/{sample}.R1_fastqc.html",
        zip = raw_dir + "{sample}/fastqc_per_sample/{sample}.R2_fastqc.zip"
    threads:
        4
    log:
        raw_dir + "logs/raw_per_sample_fastqc.sample=[{sample}].log"
    run:
        out_dir = os.path.dirname(output[0])
        print(out_dir)
        shell("fastqc --threads {threads} --outdir {out_dir} {input.forward} {input.reverse} 2> {log} 1>&2")


rule raw_per_sample_multiqc:
    """
    Runs multiqc for combined input files.
    """
    input:
        expand(raw_dir + "{sample}/fastqc_per_sample/{sample}.R2_fastqc.zip", sample=config['samples']),
    output:
        raw_dir + "multiQC_per_sample/multiqc_report.html"
    threads:
        4
    log:
        raw_dir + "logs/raw_per_sample_multiqc.log"
    run:
        out_dir = os.path.dirname(output[0])
        shell("multiqc -f -o {out_dir} {raw_dir}/*/fastqc_per_sample 2> {log} 1>&2")


rule raw:
    """
    Top-level rule to do raw read prep
    """
    input:
        raw_dir + "multiQC_per_file/multiqc_report.html",
        raw_dir + "multiQC_per_sample/multiqc_report.html"

