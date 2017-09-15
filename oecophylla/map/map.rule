rule map_bowtie2_index:
    input:
        assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa" % config['mapping_assembler']
    output:
        touch(map_dir + "{bin_sample}/mapping/{bin_sample}.done")
    log:
        map_dir + "logs/map_bowtie2_index.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/map/map_bowtie2_index.sample=[{bin_sample}].txt"
    threads:
        12
    run:
        outdir = os.path.dirname(output[0])
        shell("bowtie2-build {input} {outdir}/{wildcards.bin_sample} 2> {log} 1>&2")


rule map_bowtie2:
    input:
        idx = map_dir + "{bin_sample}/mapping/{bin_sample}.done",
        forward = qc_dir + "{abund_sample}/filtered/{abund_sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{abund_sample}/filtered/{abund_sample}.R2.trimmed.filtered.fastq.gz"
    output:
        bam = temp(map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.bam"),
        bai = temp(map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.bam.bai")
    log:
        bowtie = map_dir + "logs/map_bowtie2.sample=[{bin_sample}].abund_sample=[{abund_sample}].bowtie.log",
        other = map_dir + "logs/map_bowtie2.sample=[{bin_sample}].abund_sample=[{abund_sample}].other.log"
    benchmark:
        "benchmarks/map/map_bowtie2.sample=[{bin_sample}].abund_sample=[{abund_sample}].txt"
    threads:
        12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            idx_base = os.path.join(os.path.dirname(input.idx),
                                    wildcards.bin_sample)
            shell("""
                    bowtie2 -x {idx_base} -p {threads} --no-unal \
                    -q -1 {input.forward} -2 {input.reverse} 2> {log.bowtie} | \
                    samtools sort -O bam -l 0 -T {temp_dir} -o {temp_dir}/out.bam 2> {log.other}

                    samtools index {temp_dir}/out.bam

                    scp {temp_dir}/out.bam {output.bam}
                    scp {temp_dir}/out.bam.bai {output.bai}
                  """)


rule map_faidx_index:
    input:
        assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa" % config['mapping_assembler']
    output:
        assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa.fai" % config['mapping_assembler']
    log:
        map_dir + "logs/map_faidx_index.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/map/map_faidx_index.sample=[{bin_sample}].txt"
    threads:
        1
    run:
        outdir = os.path.dirname(output[0])
        shell("samtools faidx {input} 2> {log} 1>&2")

rule map_cram:
    input:
        bam = map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.bam",
        ref_idx = assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa.fai" % config['mapping_assembler'],
        ref = assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa" % config['mapping_assembler']
    output:
        map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.cram"
    params:
        cram = config['params']['cram']
    log:
        map_dir + "logs/map_cram.sample=[{bin_sample}].abund_sample=[{abund_sample}].log"
    benchmark:
        "benchmarks/map/map_cram.sample=[{bin_sample}].abund_sample=[{abund_sample}].txt"
    threads:
        12
    run:
        if params.cram is None:
            params.cram = ''
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            shell("""                    
                    samtools view -@ {threads} -C -h -T {input.ref} \
                    {params.cram} {input.bam} -o {temp_dir}/output.cram 2> {log}

                    scp {temp_dir}/output.cram {output}
                  """)

rule map:
    input:
        expand(map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.cram",
               sample=samples, bin_sample=config['binning_samples'],
               abund_sample=config['abundance_samples'])