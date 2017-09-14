rule function_humann2:
    """
    Runs HUMAnN2 pipeline using general defaults.

    Other HUMAnN2 parameters can be specified as a quoted string in
    PARAMS: HUMANN2: OTHER.

    Going to do just R1 reads for now. Because of how I've split PE vs SE
    processing and naming, still will need to make a separate rule for PE.
    """
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz",
        metaphlan_in = taxonomy_dir + "metaphlan2/joined_taxonomic_profile_max.tsv"
    output:
        genefamilies = temp("test_out/humann2/{sample}/{sample}_genefamilies.txt"),
        pathcoverage = temp("test_out/humann2/{sample}/{sample}_pathcoverage.txt"),
        pathabundance = temp("test_out/humann2/{sample}/{sample}_pathabundance.txt")
    params:
        humann2_nt_db = config['params']['humann2']["humann2_nt_db"],
        humann2_aa_db = config['params']['humann2']["humann2_aa_db"],
        other = config['params']['humann2']['other']
    threads:
        8
    log:
        func_dir + "logs/function_humann2_{sample}.log"
    benchmark:
        "benchmarks/function/function_humann2_{sample}.json"
    run:

  shell("""
        mkdir -p test_out/humann2/{wildcards.sample}/temp
        zcat {input.forward} {input.reverse} > test_out/humann2/{wildcards.sample}/temp/input.fastq

        humann2 --input test_out/humann2/{wildcards.sample}/temp/input.fastq \
        --output test_out/humann2/{wildcards.sample}/temp \
        --output-basename {wildcards.sample} \
        --nucleotide-database {params.humann2_nt_db} \
        --protein-database {params.humann2_aa_db} \
        --o-log {log} \
        --threads {threads} \
        {params.other} 2> {log} 1>&2
        """)


rule function_humann2_combine_tables:
    """
    Combines the per-sample normalized tables into a single run-wide table.

    Because HUMAnN2 takes a directory as input, first copies all the individual
    tables generated in this run to a temp directory and runs on that.
    """
    input:
        lambda wildcards: expand("test_out/humann2/{sample}/{sample}_genefamilies.txt",
               sample=samples),
        lambda wildcards: expand("test_out/humann2/{sample}/{sample}_pathcoverage.txt",
               sample=samples),
        lambda wildcards: expand("test_out/humann2/{sample}/{sample}_pathabundance.txt",
               sample=samples)
    output:
        genefamilies = "test_out/humann2/genefamilies.txt",
        pathcoverage = "test_out/humann2/pathcoverage.txt",
        pathabundance = "test_out/humann2/pathabundance.txt",
        genefamilies_cpm = "test_out/humann2/genefamilies_cpm.txt",
        pathcoverage_relab = "test_out/humann2/pathcoverage_relab.txt",
        pathabundance_relab = "test_out/humann2/pathabundance_relab.txt",
        genefamilies_cpm_strat = "test_out/humann2/genefamilies_cpm_stratified.txt",
        pathcoverage_relab_strat = "test_out/humann2/pathcoverage_relab_stratified.txt",
        pathabundance_relab_strat = "test_out/humann2/pathabundance_relab_stratified.txt",
        genefamilies_cpm_unstrat = "test_out/humann2/genefamilies_cpm_unstratified.txt",
        pathcoverage_relab_unstrat = "test_out/humann2/pathcoverage_relab_unstratified.txt",
        pathabundance_relab_unstrat = "test_out/humann2/pathabundance_relab_unstratified.txt"
    log:
        func_dir + "logs/function_humann2_combine_tables_{norm}.log"
    benchmark:
        "benchmarks/function/function_humann2_combine_tables_{norm}.json"
    run:
        with tempfile.TemporaryDirectory(dir=func_dir + "humann2") as temp_dir:
            for file in input:
                shell("cp {0} {1}/.".format(file, temp_dir))
            shell("""
                  humann2_join_tables --input test_out/humann2/ \
                  --search-subdirectories \
                  --output test_out/humann2/genefamilies.txt \
                  --file_name genefamilies 2> {log} 1>&2

                  humann2_join_tables --input test_out/humann2/ \
                  --search-subdirectories \
                  --output test_out/humann2/pathcoverage.txt \
                  --file_name pathcoverage 2>> {log} 1>&2

                  humann2_join_tables --input test_out/humann2/ \
                  --search-subdirectories \
                  --output test_out/humann2/pathabundance.txt \
                  --file_name pathabundance 2>> {log} 1>&2


                  # normalize
                  humann2_renorm_table --input test_out/humann2/genefamilies.txt \
                  --output test_out/humann2/genefamilies_cpm.txt \
                  --units cpm -s n 2>> {log} 1>&2

                  humann2_renorm_table --input test_out/humann2/pathcoverage.txt \
                  --output test_out/humann2/pathcoverage_relab.txt \
                  --units relab -s n 2>> {log} 1>&2

                  humann2_renorm_table --input test_out/humann2/pathabundance.txt \
                  --output test_out/humann2/pathabundance_relab.txt \
                  --units relab -s n 2>> {log} 1>&2


                  # stratify
                  humann2_split_stratified_table --input test_out/humann2/genefamilies_cpm.txt \
                  --output test_out/humann2 2>> {log} 1>&2

                  humann2_split_stratified_table --input test_out/humann2/pathcoverage_relab.txt \
                  --output test_out/humann2 2>> {log} 1>&2

                  humann2_split_stratified_table --input test_out/humann2/pathabundance_relab.txt \
                  --output test_out/humann2 2>> {log} 1>&2
                  """)

rule function_humann2_remove_unmapped:
    """
    By default, HUMAnN2 includes the un-annoated reads (either unmapped in the
    first step of the pipeline or not matched in the translated alignment step)
    in the output files. In my experience, this causes relatively small
    differences in run quality (e.g. different read lengths) to have huge
    effects on the evaluated outcome, as the overall proportion of unmatched
    reads varies by run, and the compositionality of the data then causes large
    fluctuations in the count estimates of the annotated genes and pathways.

    To remove this problem, this rule renormalizes the combined tables after
    extracting unmatched read categories.
    """
    input:
        genefamilies = func_dir + "humann2/combined_genefamilies_{norm}_all.biom",
        pathcoverage = func_dir + "humann2/combined_pathcoverage_{norm}_all.biom",
        pathabundance = func_dir + "humann2/combined_pathabundance_{norm}_all.biom"
    output:
        genefamilies = func_dir + "humann2/combined_genefamilies_{norm}_mapped.biom",
        pathcoverage = func_dir + "humann2/combined_pathcoverage_{norm}_mapped.biom",
        pathabundance = func_dir + "humann2/combined_pathabundance_{norm}_mapped.biom"
    threads:
        1
    params:
        humann2_env = config['humann2_env']
    log:
        func_dir + "logs/function_humann2_remove_unmapped_{norm}.log"
    benchmark:
        "benchmarks/function/function_humann2_remove_unmapped_{norm}.json"
    run:
        shell("""
              set +u; {params.humann2_env}; set -u

              humann2_renorm_table --input {input.genefamilies} \
              --output {output.genefamilies} \
              --units {wildcards.norm} -s n 2> {log} 1>&2

              humann2_renorm_table --input {input.pathcoverage} \
              --output {output.pathcoverage} \
              --units {wildcards.norm} -s n 2>> {log} 1>&2

              humann2_renorm_table --input {input.pathabundance} \
              --output {output.pathabundance} \
              --units {wildcards.norm} -s n 2>> {log} 1>&2
              """)


rule function_humann2_split_stratified_tables:
    """
    Splits the grouped tables into separate grouped taxonomy-stratified and un-
    stratified tables for downstream analysis. Does this for both the combined
    tables including unmatched reads (*_all) and those excluding unmatched
    reads (*_mapped).

    The un-stratified tables should then be directly useful for downstream
    analysis in e.g. beta diversity.
    """
    input:
        genefamilies = func_dir + "humann2/combined_genefamilies_{norm}_{mapped}.biom",
        pathcoverage = func_dir + "humann2/combined_pathcoverage_{norm}_{mapped}.biom",
        pathabundance = func_dir + "humann2/combined_pathabundance_{norm}_{mapped}.biom"
    output:
        genefamilies = func_dir + "humann2/stratified/combined_genefamilies_{norm}_{mapped}_stratified.biom",
        pathcoverage = func_dir + "humann2/stratified/combined_pathcoverage_{norm}_{mapped}_stratified.biom",
        pathabundance = func_dir + "humann2/stratified/combined_pathabundance_{norm}_{mapped}_stratified.biom",
        genefamilies_unstrat = func_dir + "humann2/stratified/combined_genefamilies_{norm}_{mapped}_unstratified.biom",
        pathcoverage_unstrat = func_dir + "humann2/stratified/combined_pathcoverage_{norm}_{mapped}_unstratified.biom",
        pathabundance_unstrat = func_dir + "humann2/stratified/combined_pathabundance_{norm}_{mapped}_unstratified.biom"
    threads:
        1
    params:
        humann2_env = config['humann2_env']
    log:
        func_dir + "logs/function_humann2_split_stratified_tables_{norm}_{mapped}.log"
    benchmark:
        "benchmarks/function/function_humann2_split_stratified_tables_{norm}_{mapped}.json"
    run:
        out_dir = os.path.dirname(output[0])
        shell("""
              set +u; {params.humann2_env}; set -u

              humann2_split_stratified_table --input {input.genefamilies} \
              --output {out_dir} 2> {log} 1>&2

              humann2_split_stratified_table --input {input.pathcoverage} \
              --output {out_dir} 2>> {log} 1>&2

              humann2_split_stratified_table --input {input.pathabundance} \
              --output {out_dir} 2>> {log} 1>&2
              """)
