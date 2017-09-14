rule taxonomy_metaphlan2:
    """
    Runs MetaPhlan2 on a set of samples to create a joint taxonomic profile for
    input into HUMAnN2, based on the thinking that it is preferable to have a
    consistent Chocophlan reference database for the whole set of samples. This
    is especially true for shallowly sequenced samples.

    Going to do just R1 reads for now. Because of how I've split PE vs SE
    processing and naming, still will need to make a separate rule for PE.
    """
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        taxonomy_dir + "{sample}/metaphlan2/{sample}_metaphlan2_output.tsv"
    params:
        metaphlan2_dir = config['params']['metaphlan2']["metaphlan2_dir"],
        metaphlan2_env = config['envs']['metaphlan2']
    threads:
        4
    log:
        taxonomy_dir + "logs/taxonomy_metaphlan2.{sample}.log"
    benchmark:
        "benchmarks/taxonomy/taxonomy_metaphlan2.{sample}.json"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            shell("""
                  set +u; {params.metaphlan2_env}; set -u

                  zcat {input.forward} {input.reverse} > {temp_dir}/input.fastq

                  {params.metaphlan2_dir}/metaphlan2.py {temp_dir}/input.fastq \
                    --input_type fastq \
                    --mpa_pkl {params.metaphlan2_dir}/db_v20/mpa_v20_m200.pkl \
                    --bowtie2db {params.metaphlan2_dir}/db_v20/mpa_v20_m200 \
                    --nproc {threads} \
                    --tmp_dir {temp_dir} \
                    --no_map \
                    --input_type fastq > {output}  2> {log}
                  """)


rule taxonomy_combine_metaphlan2:
    """
    Combines MetaPhlan2 output for unified taxonomic profile for HUMAnN2.
    """
    input:
        expand(taxonomy_dir + "{sample}/metaphlan2/{sample}_metaphlan2_output.tsv",
               sample=samples)
    output:
        joint_prof = taxonomy_dir + "metaphlan2/joined_taxonomic_profile.tsv",
        max_prof = taxonomy_dir + "metaphlan2/joined_taxonomic_profile_max.tsv"
    threads:
        1
    params:
        humann2_env = config['envs']['humann2']
    log:
        taxonomy_dir + "logs/taxonomy_combine_metaphlan2.log"
    benchmark:
        "benchmarks/taxonomy/taxonomy_combine_metaphlan2.json"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            for file in input:
                shell("cp {0} {1}/.".format(file, temp_dir))
            shell("""
                  set +u; {params.humann2_env}; set -u

                  humann2_join_tables --input {temp_dir} --output {output.joint_prof} 2> {log} 1>&2
                  humann2_reduce_table --input {output.joint_prof} \
                  --output {output.max_prof} --function max --sort-by level 2>> {log} 1>&2
                  """)


rule metaphlan2:
    input:
        taxonomy_dir + "metaphlan2/joined_taxonomic_profile.tsv"


rule taxonomy_kraken:
    """
    Runs Kraken using general defaults.
    """
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        map = taxonomy_dir + "{sample}/kraken/{sample}_map.txt",
        report = taxonomy_dir + "{sample}/kraken/{sample}_report.txt"
    params:
        kraken_db = config['params']['kraken']['kraken_db'],
        kraken_env = config['envs']['kraken']
    threads:
        12
    log:
        taxonomy_dir + "logs/taxonomy_kraken.sample=[{sample}].log"
    benchmark:
        "benchmarks/taxonomy/taxonomy_kraken.sample=[{sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            map_base = os.path.basename(output['map'])
            report_base = os.path.basename(output['report'])

            shell("""
                  set +u; {params.kraken_env}; set -u

                  kraken {input.forward} {input.reverse} \
                    --db {params.kraken_db} \
                    --paired \
                    --fastq-input \
                    --gzip-compressed \
                    --only-classified-output \
                    --threads {threads} \
                    1> {temp_dir}/{map_base} \
                    2> {log}

                  kraken-report {temp_dir}/{map_base} \
                    --db {params.kraken_db} \
                    1> {temp_dir}/{report_base} \
                    2>> {log}

                  scp {temp_dir}/{map_base} {output.map}
                  scp {temp_dir}/{report_base} {output.report}
                  """)


rule taxonomy_kraken_combine_reports:
    """
    Combines the per-sample taxonomic profiles into a single run-wide table.
    """
    input:
        expand(taxonomy_dir + "{sample}/kraken/{sample}_map.txt", sample=samples)
    output:
        report = taxonomy_dir + "kraken/combined_profile.tsv"
    params:
        kraken_db = config['params']['kraken']["kraken_db"],
        kraken_env = config['envs']['kraken']
    log:
        taxonomy_dir + "logs/taxonomy_kraken_combine_reports.log"
    benchmark:
        "benchmarks/taxonomy/taxonomy_kraken_combine_reports.txt"
    run:
        shell("""
              set +u; {params.kraken_env}; set -u

              kraken-mpa-report {input} \
                --db {params.kraken_db} \
                --header-line \
                | sed '1 s/.map.txt//g' 1> {output.report} \
                2> {log}
              """)


rule kraken:
    input:
        taxonomy_dir + "kraken/combined_profile.tsv"


rule taxonomy_shogun:
    """
    Runs SHOGUN to infer taxonomic composition of sample.
    """
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        taxon_counts = taxonomy_dir + "{sample}/shogun/{sample}.taxon_counts.tsv"
    params:
        shogun = config['params']['shogun'],
        shogun_env = config['envs']['shogun']
    threads:
        2
    log:
        taxonomy_dir + "logs/taxonomy_shogun.sample=[{sample}].log"
    benchmark:
        "benchmarks/taxonomy/taxonomy_shogun.sample=[{sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            shell("""
                  set +u; {params.shogun_env}; set -u

                  # convert and merge fastq's into fasta
                  seqtk seq -A {input.forward} > {temp_dir}/{wildcards.sample}.fna
                  seqtk seq -A {input.reverse} >> {temp_dir}/{wildcards.sample}.fna

                  # run shogun
                  shogun_utree_lca.py {params.shogun} \
                  --threads {threads} \
                  --input {temp_dir} \
                  --output {temp_dir} \
                  2> {log} 1>&2

                  # parse output
                  echo '#'SampleID$'\t'{wildcards.sample} > {output.taxon_counts}
                  cat {temp_dir}/taxon_counts.csv | \
                  tail -n+2 | tr "," "\\t" >> {output.taxon_counts}
                  """)


rule taxonomy_shogun_combine_tables:
    """
    Combines the per-sample normalized tables into a single run-wide table.
    """
    input:
        expand(taxonomy_dir + "{sample}/shogun/{sample}.taxon_counts.tsv",
               sample=samples)
    output:
        report = taxonomy_dir + "shogun/combined_profile.tsv"
    log:
        taxonomy_dir + "logs/taxonomy_shogun_combine_tables.log"
    benchmark:
        "benchmarks/taxonomy/taxonomy_shogun_combine_tables.txt"
    run:
        taxa, samples = {}, []
        for file in input:
            with open(file, 'r') as f:
                sample = f.readline().strip().split('\t')[1]
                samples.append(sample)
                for line in f:
                    taxon, count = line.strip().split('\t')
                    if taxon in taxa:
                        taxa[taxon][sample] = count
                    else:
                        taxa[taxon] = {sample: count}
        with open(output[0], 'w') as f:
            f.write('#SampleID\t%s\n' % '\t'.join(samples))
            for taxon in sorted(taxa):
                row = [taxon]
                for sample in samples:
                    if sample in taxa[taxon]:
                        row.append(taxa[taxon][sample])
                    else:
                        row.append('0.0')
                f.write('%s\n' % '\t'.join(row))
        with open(log[0], 'w') as f:
            f.write('Successfully merged counts of %d taxa from %d samples.\n'
                    % (len(taxa), len(samples)))


rule shogun:
    input:
        taxonomy_dir + "shogun/combined_profile.tsv"


rule taxonomy:
    input:
        taxonomy_dir + "metaphlan2/joined_taxonomic_profile.tsv",
        taxonomy_dir + "kraken/combined_profile.tsv",
        taxonomy_dir + "shogun/combined_profile.tsv"


