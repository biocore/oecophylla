
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
        metaphlan_in = tax_dir + "metaphlan2/joined_taxonomic_profile_max.tsv"
    output:
        genefamilies = func_dir + "{sample}/humann2/{sample}_genefamilies.biom",
        pathcoverage = func_dir + "{sample}/humann2/{sample}_pathcoverage.biom",
        pathabundance = func_dir + "{sample}/humann2/{sample}_pathabundance.biom"
    params:
        metaphlan_dir = config['params']['humann2']["metaphlan_dir"],
        humann2_nt_db = config['params']['humann2']["humann2_nt_db"],
        humann2_aa_db = config['params']['humann2']["humann2_aa_db"],
        humann2_env = config['humann2_env'],
        other = config['params']['humann2']['other']
    threads:
        8
    log:
        func_dir + "logs/function_humann2_{sample}.log"
    benchmark:
        "benchmarks/function/function_humann2_{sample}.json"
    run:
        with tempfile.TemporaryDirectory(dir=TMP_DIR_ROOT) as temp_dir:
            shell("""
                  set +u; {params.humann2_env}; set -u

                  zcat {input.forward} {input.reverse} > {temp_dir}/input.fastq

                  humann2 --input {temp_dir}/input.fastq \
                  --output {temp_dir}/{wildcards.sample} \
                  --output-basename {wildcards.sample} \
                  --nucleotide-database {params.humann2_nt_db} \
                  --protein-database {params.humann2_aa_db} \
                  --taxonomic-profile {input.metaphlan_in} \
                  --metaphlan {params.metaphlan_dir} \
                  --o-log {log} \
                  --threads {threads} \
                  --output-format biom {params.other} 2> {log} 1>&2


                  scp {temp_dir}/{wildcards.sample}/{wildcards.sample}_genefamilies.biom {output.genefamilies}
                  scp {temp_dir}/{wildcards.sample}/{wildcards.sample}_pathcoverage.biom {output.pathcoverage}
                  scp {temp_dir}/{wildcards.sample}/{wildcards.sample}_pathabundance.biom {output.pathabundance}
                  """)


rule function_humann2_renorm_tables:
    """
    Renormalizes HUMAnN2 per-sample tables, per recommendation in the HUMAnN2
    website. 

    Counts-per-million (cpm) or Relative Abundance (Relabund) can be specified
    as a list in the PARAMS: HUMANN2: NORMS variable in the config file.
    """
    input:
        genefamilies = func_dir + "{sample}/humann2/{sample}_genefamilies.biom",
        pathcoverage = func_dir + "{sample}/humann2/{sample}_pathcoverage.biom",
        pathabundance = func_dir + "{sample}/humann2/{sample}_pathabundance.biom"
    output:
        genefamilies = func_dir + "{sample}/humann2/{sample}_genefamilies_{norm}.biom",
        pathcoverage = func_dir + "{sample}/humann2/{sample}_pathcoverage_{norm}.biom",
        pathabundance = func_dir + "{sample}/humann2/{sample}_pathabundance_{norm}.biom"
    threads:
        1
    params:
        humann2_env = config['humann2_env']
    log:
        func_dir + "logs/function_humann2_renorm_tables_{sample}_{norm}.log"
    benchmark:
        "benchmarks/function/function_humann2_renorm_tables_{sample}_{norm}.json"
    run:
        shell("""
              set +u; {params.humann2_env}; set -u

              humann2_renorm_table --input {input.genefamilies} \
              --output {output.genefamilies} \
              --units {wildcards.norm} 2> {log} 1>&2

              humann2_renorm_table --input {input.pathcoverage} \
              --output {output.pathcoverage} \
              --units {wildcards.norm} 2>> {log} 1>&2

              humann2_renorm_table --input {input.pathabundance} \
              --output {output.pathabundance} \
              --units {wildcards.norm} 2>> {log} 1>&2
              """)


rule function_humann2_combine_tables:
    """
    Combines the per-sample normalized tables into a single run-wide table. 

    Because HUMAnN2 takes a directory as input, first copies all the individual
    tables generated in this run to a temp directory and runs on that.
    """
    input:
        lambda wildcards: expand(func_dir + "{sample}/humann2/{sample}_genefamilies_{norm}.biom",
               sample=samples, norm=wildcards.norm),
        lambda wildcards: expand(func_dir + "{sample}/humann2/{sample}_pathcoverage_{norm}.biom",
               sample=samples, norm=wildcards.norm),
        lambda wildcards: expand(func_dir + "{sample}/humann2/{sample}_pathabundance_{norm}.biom",
               sample=samples, norm=wildcards.norm)
    output:
        genefamilies = func_dir + "humann2/combined_genefamilies_{norm}_all.biom",
        pathcoverage = func_dir + "humann2/combined_pathcoverage_{norm}_all.biom",
        pathabundance = func_dir + "humann2/combined_pathabundance_{norm}_all.biom"
    log:
        func_dir + "logs/function_humann2_combine_tables_{norm}.log"
    params:
        humann2_env = config['humann2_env']
    benchmark:
        "benchmarks/function/function_humann2_combine_tables_{norm}.json"
    run:
        with tempfile.TemporaryDirectory(dir=func_dir + "humann2") as temp_dir:
            for file in input:
                shell("cp {0} {1}/.".format(file, temp_dir))
            shell("""
                  set +u; {params.humann2_env}; set -u

                  humann2_join_tables --input {temp_dir} \
                  --output {output.genefamilies} \
                  --file_name genefamilies 2> {log} 1>&2

                  humann2_join_tables --input {temp_dir} \
                  --output {output.pathcoverage} \
                  --file_name pathcoverage 2>> {log} 1>&2

                  humann2_join_tables --input {temp_dir} \
                  --output {output.pathabundance} \
                  --file_name pathabundance 2>> {log} 1>&2

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


rule humann2:
    """
    Rule to do Humann2
        - metaphlan2_sample_pe
        - combine_metaphlan
        - humann2_sample_pe
        - humann2_combine_tables
        - humann2_remove_unmapped
        - humann2_split_stratified_tables
    """
    input:
        expand(# individual normed bioms
               func_dir + "{sample}/humann2/{sample}_genefamilies_{norm}.biom",
               norm = config['params']['humann2']['norms'],
               sample = samples),
        expand(# stratified
               func_dir + "humann2/stratified/combined_genefamilies_{norm}_{mapped}_unstratified.biom",
               norm = config['params']['humann2']['norms'],
               mapped=['all','mapped'])



rule function:
    """
    Rule to do Humann2
        - metaphlan2_sample_pe
        - combine_metaphlan
        - humann2_sample_pe
        - humann2_combine_tables
        - humann2_remove_unmapped
        - humann2_split_stratified_tables
    """
    input:
        expand(# individual normed bioms
               func_dir + "{sample}/humann2/{sample}_genefamilies_{norm}.biom",
               norm = config['params']['humann2']['norms'],
               sample = samples),
        expand(# stratified
               func_dir + "humann2/stratified/combined_genefamilies_{norm}_{mapped}_unstratified.biom",
               norm = config['params']['humann2']['norms'],
               mapped=['all','mapped'])