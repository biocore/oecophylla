ANVIO_ENV = config['anvi_env']

rule anvi_gen_contigs_database:
    input:
        assemble_dir + "{bin_sample}/%s/{bin_sample}.contigs.simple.fa" % config['mapping_assembler']
    output:
        db = anvio_dir + "{bin_sample}/{bin_sample}.db",
        h5 =  anvio_dir + "{bin_sample}/{bin_sample}.h5",
        done = touch(anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done")
    threads:
        4
    log:
        anvio_dir + "logs/anvi_gen_contigs_database.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_gen_contigs_database.sample=[{bin_sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            dbname = os.path.basename(output.db)
            h5name = os.path.basename(output.h5)
            shell("""
                    set +u; {ANVIO_ENV}; set -u

                    anvi-gen-contigs-database -f {input} -o {temp_dir}/{dbname} 2> {log} 1>&2

                    scp {temp_dir}/{dbname} {output.db}
                    scp {temp_dir}/{h5name} {output.h5}
                  """)

rule anvi_run_hmms:
    input:
        anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done"
    output:
        touch(anvio_dir + "{bin_sample}/{bin_sample}.db.run-hmms.done")
    threads:
        12
    log:
        anvio_dir + "logs/anvi_run_hmms.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_run_hmms.sample=[{bin_sample}].txt"
    run:
        db = os.path.join(os.path.dirname(input[0]),wildcards.bin_sample + '.db')
        shell("""
                set +u; {ANVIO_ENV}; set -u

                anvi-run-hmms -c {db} --num-threads {threads} 2> {log} 1>&2
              """)

rule anvi_export_gene_calls:
    input:
        anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done",
        anvio_dir + "{bin_sample}/{bin_sample}.db.run-hmms.done"
    output:
        anvio_dir + "{bin_sample}/{bin_sample}.gene-calls.fa"
    log:
        anvio_dir + "logs/anvi_export_gene_calls.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_export_gene_calls.sample=[{bin_sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            out_name = os.path.basename(output[0])
            db = os.path.join(os.path.dirname(input[0]),wildcards.bin_sample + '.db')
            shell("""
                    set +u; {ANVIO_ENV}; set -u

                    anvi-get-dna-sequences-for-gene-calls -c {db} -o {temp_dir}/{out_name} 2> {log} 1>&2

                    scp {temp_dir}/{out_name} {output}
                  """)

rule anvi_run_centrifuge:
    input:
        fa=anvio_dir + "{bin_sample}/{bin_sample}.gene-calls.fa",
        db_done = anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done"
    output:
        hits=anvio_dir + "{bin_sample}/centrifuge_hits.tsv",
        report=anvio_dir + "{bin_sample}/centrifuge_report.tsv",
        done=touch(anvio_dir + "{bin_sample}/{bin_sample}.db.added_centrifuge.done")
    log:
        anvio_dir + "logs/anvi_run_centrifuge.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_run_centrifuge.sample=[{bin_sample}].txt"
    params:
        centrifuge_base=config['resources']['centrifuge_base'],
        centrifuge_models=config['resources']['centrifuge_models']
    threads: 12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            hits_name = os.path.basename(output.hits)
            report_name = os.path.basename(output.report)
            db_dir = os.path.dirname(input.db_done)
            db = os.path.join(db_dir, wildcards.bin_sample + '.db')
            db_name = os.path.basename(db)
            shell("""
                    set +u; {ANVIO_ENV}; set -u

                    export CENTRIFUGE_BASE={params.centrifuge_base}
                    centrifuge -f --threads {threads} \
                    -x {params.centrifuge_models} \
                    {input.fa} \
                    -S {temp_dir}/{hits_name} \
                    --report-file {temp_dir}/{report_name}

                    scp {temp_dir}/{hits_name} {output.hits}
                    scp {temp_dir}/{report_name} {output.report}

                    cd {db_dir}

                    anvi-import-taxonomy -c {db_name} \
                    -i centrifuge_report.tsv centrifuge_hits.tsv \
                    -p centrifuge
                  """)

rule anvi_profile:
    input:
        bam = map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.bam",
        bai = map_dir + "{bin_sample}/mapping/{bin_sample}_{abund_sample}.bam.bai",
        db_done = anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done",
        centrifute_done = anvio_dir + "{bin_sample}/{bin_sample}.db.added_centrifuge.done"
    output:
        aux=anvio_dir + "{bin_sample}/{bin_sample}.{abund_sample}.bam-ANVIO_PROFILE/AUXILIARY-DATA.h5",
        prof=anvio_dir + "{bin_sample}/{bin_sample}.{abund_sample}.bam-ANVIO_PROFILE/PROFILE.db",
        log=anvio_dir + "{bin_sample}/{bin_sample}.{abund_sample}.bam-ANVIO_PROFILE/RUNLOG.txt"
    log:
        anvio_dir + "logs/anvi_profile.sample=[{bin_sample}].abund_sample=[{abund_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_profile.sample=[{bin_sample}].abund_sample=[{abund_sample}].txt"
    threads: 12
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            prof_dir = os.path.dirname(output.prof)
            db_dir = os.path.dirname(input.db_done)
            db = os.path.join(db_dir,wildcards.bin_sample + '.db')
            shell("""
                    set +u; {ANVIO_ENV}; set -u

                    scp {input.bam} {temp_dir}/{wildcards.bin_sample}_{wildcards.abund_sample}.bam
                    scp {input.bai} {temp_dir}/{wildcards.bin_sample}_{wildcards.abund_sample}.bam.bai

                    anvi-profile -i {temp_dir}/{wildcards.bin_sample}_{wildcards.abund_sample}.bam \
                    --num-threads {threads} --write-buffer-size 1000 \
                    -c {db} \
                    --skip-SNV-profiling \
                    --overwrite-output-destinations \
                    -o {temp_dir}/out

                    scp {temp_dir}/out/* {prof_dir}/.
                  """)

rule anvi_merge:
    input:
        profiles=lambda wildcards: expand(anvio_dir + "{bin_sample}/{bin_sample}.{abund_sample}.bam-ANVIO_PROFILE/PROFILE.db",
                        bin_sample=wildcards.bin_sample,
                        abund_sample=config['abundance_samples']),
        db_done = anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done",
        centrifuge_done=anvio_dir + "{bin_sample}/{bin_sample}.db.added_centrifuge.done",
        hmms_done=anvio_dir + "{bin_sample}/{bin_sample}.db.run-hmms.done"
    output:        
        aux=anvio_dir + "{bin_sample}/SAMPLES_MERGED/AUXILIARY-DATA.h5",
        prof=anvio_dir + "{bin_sample}/SAMPLES_MERGED/PROFILE.db",
        runlog=anvio_dir + "{bin_sample}/SAMPLES_MERGED/RUNLOG.txt",
        samps=anvio_dir + "{bin_sample}/SAMPLES_MERGED/SAMPLES.db"
    log:
        anvio_dir + "logs/anvi_merge.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_merge.sample=[{bin_sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            merge_dir = os.path.dirname(output.prof)
            db = os.path.join(os.path.dirname(input.db_done),wildcards.bin_sample + '.db')
            shell("""
                    set +u; {ANVIO_ENV}; set -u

                    anvi-merge {input.profiles} \
                    -o {temp_dir}/SAMPLES_MERGED \
                    -c {db} \
                    -W

                    scp -r {temp_dir}/SAMPLES_MERGED/* {merge_dir}/.
                  """)

rule anvi_add_maxbin:
    input:
        bins = bin_dir + "{bin_sample}/maxbin/{bin_sample}_maxbin_bins.txt",
        prof = anvio_dir + "{bin_sample}/SAMPLES_MERGED/PROFILE.db",
        db_done = anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done"
    output:
        touch(anvio_dir + "{bin_sample}/{bin_sample}.db.anvi_add_maxbin.done")
    log:
        anvio_dir + "logs/anvi_add_maxbin.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_add_maxbin.sample=[{bin_sample}].txt"
    run:
        db = os.path.join(os.path.dirname(input.db_done),wildcards.bin_sample + '.db')
        shell("""
                set +u; {ANVIO_ENV}; set -u

                anvi-import-collection -p {input.prof} \
                -c {db} \
                -C "MaxBin2" \
                --contigs-mode \
                {input.bins}
              """)


rule anvi_summarize:
    input:
        prof = anvio_dir + "{bin_sample}/SAMPLES_MERGED/PROFILE.db",
        db_done = anvio_dir + "{bin_sample}/{bin_sample}.anvi_gen_contigs_database.done"
    output:
        tar = anvio_dir + "{bin_sample}/{bin_sample}_samples-summary_CONCOCT.tar.gz",
        report = anvio_dir + "{bin_sample}/{bin_sample}_samples-summary_CONCOCT.html",
        txt = anvio_dir + "{bin_sample}/{bin_sample}_samples-summary_CONCOCT.txt"
    log:
        anvio_dir + "logs/anvi_summarize.sample=[{bin_sample}].log"
    benchmark:
        "benchmarks/anvio/anvi_summarize.sample=[{bin_sample}].txt"
    run:
        with tempfile.TemporaryDirectory(dir=find_local_scratch(TMP_DIR_ROOT)) as temp_dir:
            db = os.path.join(os.path.dirname(input.db_done),wildcards.bin_sample + '.db')
            shell("""
                    set +u; {ANVIO_ENV}; set -u

                    anvi-summarize -p {input.prof} \
                    -c {db} \
                    -o {temp_dir}/{wildcards.bin_sample}_samples-summary_CONCOCT \
                    -C CONCOCT

                    scp {temp_dir}/{wildcards.bin_sample}_samples-summary_CONCOCT/general_bins_summary.txt {output.txt}
                    scp {temp_dir}/{wildcards.bin_sample}_samples-summary_CONCOCT/index.html {output.report}
                    
                    tar -czvf {temp_dir}/{wildcards.bin_sample}_samples-summary_CONCOCT.tar.gz {temp_dir}/{wildcards.bin_sample}_samples-summary_CONCOCT

                    scp {temp_dir}/{wildcards.bin_sample}_samples-summary_CONCOCT.tar.gz {output.tar}
                  """)


rule anvio:
    input:
        expand(anvio_dir + "{bin_sample}/{bin_sample}_samples-summary_CONCOCT.tar.gz",
               bin_sample=config['binning_samples']),
        expand(anvio_dir + "{bin_sample}/{bin_sample}.db.anvi_add_maxbin.done",
               bin_sample=config['binning_samples'])