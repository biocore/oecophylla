rule bin_make_cov_files:
    input:
        bams = lambda wildcards: expand(map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.bam",
               bin_sample=wildcards.bin_sample,
               abund_sample=config['abundance_samples']),
        ref = assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa" % config['mapping_assembler']
    output:
        temp(bin_dir + "{bin_sample}/abundance_files/{bin_sample}_abund_list.txt")
    log:
        bin_dir + "logs/bin_make_cov_files.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/bin/bin_make_cov_files.sample=[{bin_sample}].txt"
    threads:
        12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            out_dir = os.path.dirname(output[0])
            abund_list = ''
            for bam in input.bams:
                fn = os.path.basename(bam).split('.')[0]
                shell("""
                        samtools view {bam} --threads {threads} -h | \
                        pileup.sh -Xmx8g out={temp_dir}/{fn}_pileup.txt 2> {log} 1>&2

                        awk '{{print $1"\t"$2}}' {temp_dir}/{fn}_pileup.txt | \
                        grep -v '^#' > {temp_dir}/{fn}_abund.txt
                      """)
                abund_list += os.path.join(out_dir, fn + '_abund.txt\n')

            shell("""
                    scp {temp_dir}/*.txt {out_dir}/.
                  """)
            with open(output[0],'w') as f:
                f.write(abund_list)


rule bin_run_maxbin:
    input:
        abund = bin_dir + "{bin_sample}/abundance_files/{bin_sample}_abund_list.txt",
        ref = assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa" % config['mapping_assembler']
    output: 
        bin_dir + "{bin_sample}/maxbin/{bin_sample}.summary"
    log:
        bin_dir + "logs/bin_run_maxbin.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/bin/bin_run_maxbin.sample=[{bin_sample}].txt"
    params:
        maxbin = config['params']['maxbin']
    threads:
        12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            out_base = os.path.dirname(output[0])
            if params.maxbin is None:
                params.maxbin = ''
            shell("""
                    run_MaxBin.pl -contig {input.ref} -out {temp_dir}/{wildcards.bin_sample} \
                    -abund_list {input.abund} {params.maxbin} -thread {threads} 2> {log} 1>&2

                    scp {temp_dir}/* {out_base}/.
                  """)


rule summarize_maxbin:
    input:
        bin_dir + "{bin_sample}/maxbin/{bin_sample}.summary"
    output:
        bin_dir + "{bin_sample}/maxbin/{bin_sample}_maxbin_bins.txt"
    log:
        bin_dir + "logs/summarize_maxbin.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/bin/summarize_maxbin.sample=[{bin_sample}].txt"
    threads:
        1
    run:
        bin_dir = os.path.dirname(input[0])
        bins = ''
        for file in os.listdir(bin_dir):
            if file.endswith(".fasta"):
                bin = 'Bin_' + str(file.split('.')[-2])
                with open(os.path.join(bin_dir, file),'r') as f:
                    for line in f:
                        if line.strip().startswith('>'):
                            name = line.strip()[1:]
                            bins += "{0}\t{1}\n".format(name, bin)

        with open(output[0], 'w') as out:
            out.write(bins)

rule tar_bin_cov_files:
    input:
        abund_list = bin_dir + "{bin_sample}/abundance_files/{bin_sample}_abund_list.txt",
        bin_summary = bin_dir + "{bin_sample}/maxbin/{bin_sample}_maxbin_bins.txt"
    output:
        bin_dir + "{bin_sample}/abundance_files.tar.gz"
    threads:
        1
    benchmark:
        "benchmarks/bin/tar_bin_cov_files.sample=[{bin_sample}].txt"
    run:
        abund_dir = os.path.dirname(input.abund_list)
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            shell("""
                    scp -r {abund_dir} {temp_dir}/abundance_files

                    tar -czvf {temp_dir}/abundance_files.tar.gz  {temp_dir}/abundance_files

                    scp  {temp_dir}/abundance_files.tar.gz {output}

                    rm -r {abund_dir}
                  """)

rule bin_maxbin:
    input:
        expand(bin_dir + "{bin_sample}/maxbin/{bin_sample}.summary",
               bin_sample = config['binning_samples']),
        expand(bin_dir + "{bin_sample}/abundance_files.tar.gz",
               bin_sample = config['binning_samples'])


rule bin:
    input:
        expand(bin_dir + "{bin_sample}/maxbin/{bin_sample}.summary",
               bin_sample=config['binning_samples']),
        expand(bin_dir + "{bin_sample}/abundance_files.tar.gz",
               bin_sample = config['binning_samples'])