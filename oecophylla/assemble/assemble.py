rule assemble_megahit:
    """
    Run Megahit assembly on fastq
    """
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        assemble_dir + "{sample}/megahit/{sample}.contigs.fa"
    params:
        memory = 120
    threads:
        12
    log:
        assemble_dir + "logs/assemble_megahit.sample=[{sample}].log"
    benchmark:
        "benchmarks/assemble/assemble_megahit.sample=[{sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            mem_b = params.memory * 1000000000
            outdir = os.path.dirname(output[0])
            shell("""
                  #rm -r {outdir}

                  megahit -1 {input.forward} -2 {input.reverse} \
                  -m {mem_b} -t {threads} -o {temp_dir}/megahit \
                  --out-prefix {wildcards.sample} \
                  2> {log} 1>&2

                  scp {temp_dir}/megahit/{{*.log,*.fa,*.txt}} {outdir}/.
                  """)


rule assemble_metaspades:
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        assemble_dir + "{sample}/metaspades/{sample}.contigs.fa"
    log:
        assemble_dir + "logs/assemble_metaspades.sample=[{sample}].log"
    benchmark:
        "benchmarks/assemble/assemble_metaspades.sample=[{sample}].txt"
    params:
        mem=240
    threads:
        12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            outdir = os.path.dirname(output[0])
            contigs_fp = os.path.abspath(os.path.join(outdir,'contigs.fasta'))
            shell("""
                    spades.py --meta -t {threads} -m {params.mem} \
                    -1 {input.forward} -2 {input.reverse} -o {temp_dir} \
                    2> {log} 1>&2

                    scp -r {temp_dir}/{{spades.log,*.fasta,assembly_graph*,*.paths}} {outdir}/.

                    ln -s {contigs_fp} {outdir}/{wildcards.sample}.contigs.fa
                  """)


rule assemble_spades:
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        assemble_dir + "{sample}/spades/{sample}.contigs.fa"
    log:
        assemble_dir + "logs/assemble_spades.sample=[{sample}].log"
    benchmark:
        "benchmarks/assemble/assemble_spades.sample=[{sample}].txt"
    params:
        mem=240
    threads:
        12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            outdir = os.path.dirname(output[0])
            contigs_fp = os.path.abspath(os.path.join(outdir,'contigs.fasta'))
            shell("""
                    spades.py -t {threads} -m {params.mem} \
                    -1 {input.forward} -2 {input.reverse} -o {temp_dir} \
                    2> {log} 1>&2

                    scp -r {temp_dir}/{{spades.log,*.fasta,assembly_graph*,*.paths}} {outdir}/.

                    ln -s {contigs_fp} {outdir}/{wildcards.sample}.contigs.fa
                  """)


rule assemble_metaquast:
    input:
        lambda wildcards: expand(assemble_dir + "{sample}/{assembler}/{sample}.contigs.fa",
                                 assembler = config['assemblers'],
                                 sample = wildcards.sample)
    output:
        done = assemble_dir + "{sample}/metaquast/{sample}.metaquast.done"
    log:
        assemble_dir + "logs/assemble_metaquast.sample=[{sample}].log"
    threads:
        12
    benchmark:
        "benchmarks/assemble/assemble_metaquast.sample=[{sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            outdir = os.path.dirname(output.done)
            assemblies = ' '.join(input)
            shell("""
                    metaquast.py -t {threads} -o {temp_dir}/metaquast \
                    {assemblies} 2> {log} 1>&2

                    scp -r {temp_dir}/metaquast/* {outdir}/.

                    touch {output.done}
                  """)


rule assemble_quast:
    input:
        lambda wildcards: expand(assemble_dir + "{sample}/{assembler}/{sample}.contigs.fa",
                                 assembler = config['assemblers'],
                                 sample = wildcards.sample)
    output:
        done = assemble_dir + "{sample}/quast/{sample}.quast.done"
    log:
        assemble_dir + "logs/assemble_quast.sample=[{sample}].log"
    threads:
        8
    benchmark:
        "benchmarks/assemble/assemble_quast.sample=[{sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            outdir = os.path.dirname(output.done)
            assemblies = ' '.join(input)
            shell("""
                    quast.py -t {threads} -o {temp_dir}/quast \
                    {assemblies} 2> {log} 1>&2

                    scp -r {temp_dir}/quast/* {outdir}/.

                    touch {output.done}
                  """)


rule assemble_simplify_fasta_headers:
    input:
        assemble_dir + "{sample}/{assembler}/{sample}.contigs.fa"
    output:
        fasta = assemble_dir + "{sample}/{assembler}/{sample}.contigs.simple.fa",
        headers = assemble_dir + "{sample}/{assembler}/{sample}.contigs.headers.txt"
    log:
        assemble_dir + "logs/assemble_simplify_fasta_headers.sample=[{sample}].log"
    threads:
        1
    run:
        prepend = '{0}_{1}_contig_'.format(wildcards.sample,
                                           wildcards.assembler)

        simplify_headers(input[0], prepend=prepend,
                         output_fp=output.fasta, header_fp=output.headers)


rule assemble_per_sample_multiqc:
    """
    Runs multiqc for combined input files.
    """
    input:
        expand(assemble_dir + "{sample}/quast/{sample}.quast.done", sample=samples),
    output:
        assemble_dir + "multiQC_per_sample/multiqc_report.html"
    threads:
        4
    log:
        qc_dir + "logs/assemble_per_sample_multiqc.log"
    run:
        out_dir = os.path.dirname(output[0])
        shell("multiqc -f -o {out_dir} {assemble_dir}/*/quast/report.tsv 2> {log} 1>&2")


rule assemble:
    input:
        expand(assemble_dir + "{sample}/{assembler}/{sample}.contigs.fa",
               sample=samples, assembler=config['assemblers']),
        expand(assemble_dir + "{sample}/metaquast/{sample}.metaquast.done",
               sample=samples),
        expand(assemble_dir + "{sample}/quast/{sample}.quast.done",
               sample=samples),
        assemble_dir + "multiQC_per_sample/multiqc_report.html"
