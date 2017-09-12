rule mash_sketch:
    """
    Sketches a trimmed and host-filtered fastq file. 
    
    There is almost no documentation for this tool, so it's problematic.

    Relevant parameters might be:
    -b : use bloom filtering on kmers to reduce impact of low-freq erros.
    -m N: use explicit depth filtering on kmers (bigger memory impact than bloom)
    """
    input:
        forward = qc_dir + "{sample}/filtered/{sample}.R1.trimmed.filtered.fastq.gz",
        reverse = qc_dir + "{sample}/filtered/{sample}.R2.trimmed.filtered.fastq.gz"
    output:
        sketch = mash_dir + '{sample}/mash/{sample}.msh'
    params:
        mash = config['software']['mash'],
        seqtk = config['software']['seqtk'],
        mash_params = config['params']['mash']['other'],
        depth = config['params']['mash']['depth']
    threads:
        1
    log:
        mash_dir + "logs/mash_sketch.sample=[{sample}].log"
    benchmark:
        "benchmarks/mash/mash_sketch.sample=[{sample}].json"
    run:
        output_base = os.path.splitext(output['sketch'])[0]
        
        with tempfile.TemporaryDirectory(dir=TMP_DIR_ROOT) as temp_dir:
            shell("""
                  cat {input.forward} {input.reverse} > {temp_dir}/{wildcards.sample}

                  if [ -n "{params.depth}" ]; then
                    seqtk sample {temp_dir}/{wildcards.sample} {params.depth} > {temp_dir}/subsampled.fastq
                    mv {temp_dir}/subsampled.fastq {temp_dir}/{wildcards.sample}
                  fi
                  
                  {params.mash} sketch {params.mash_params} -o {output_base} {temp_dir}/{wildcards.sample}
                  """)


rule mash_refseq:
    """
    Compares a mash sketch against refseq sketch. 

    Requires that the sketches have same -k values -- for RefSeqDefault, 
    -k should equal 21. 
    """
    input:
        sketch = mash_dir + '{sample}/mash/{sample}.msh'
    output:
        refseq = mash_dir + '{sample}/mash/{sample}.refseq.txt'
    params:
        mash = config['software']['mash'],
        db = config['params']['mash']['refseq_db']
    threads:
        1
    log:
        mash_dir + "logs/mash_refseq.sample=[{sample}].log"
    benchmark:
        "benchmarks/mash/mash_refseq.sample=[{sample}].json"
    run:
        shell("""
              {params.mash} dist {params.db} {input.sketch} | sort -gk3 > {output.refseq}
              """)

rule mash_dm:
    """
    Makes mash distance output file
    """
    input:
        expand(mash_dir + '{sample}/mash/{sample}.msh',
            sample = samples)
    output:
        dm = mash_dir + 'combined_analysis/mash.dist.txt'
    params:
        mash = config['software']['mash']
    threads:
        1
    log:
        mash_dir + "logs/mash_dm.log"
    benchmark:
        "benchmarks/mash/mash_dm.json"
    run:
        for i in range(len(input)):
            for j in range(i,len(input)):
                thing1 = input[i]
                thing2 = input[j]
                shell("""
                      {params.mash} dist {thing1} {thing2} >> {output.dm}
                      """)

rule mash_dm_write:
    """
    Writes square distance matrices from p values and distances that Mash makes
    """
    input:
        dm = mash_dir + 'combined_analysis/mash.dist.txt'
    output:
        dist_matrix = mash_dir + 'combined_analysis/mash.dist.dm',
        p_matrix = mash_dir + 'combined_analysis/mash.dist.p'
    threads:
        1
    log:
        mash_dir + "logs/mash_dm_write.log"
    benchmark:
        "benchmarks/mash/mash_dm_write.json"
    run:
        from skbio.stats.distance import DissimilarityMatrix
        import pandas as pd
        import numpy as np

        mash_vec = pd.read_csv(input[0], sep = '\t', header=None)

        # get sorted list of samples
        samples = sorted(set(mash_vec[0]) | set(mash_vec[1]))

        dm = np.zeros([len(samples),len(samples)])
        pm = np.zeros([len(samples),len(samples)])

        # fill matrices with values
        for s1, s2, d, p in zip(mash_vec[0],mash_vec[1],mash_vec[2],mash_vec[3]):
            i1 = samples.index(s1)
            i2 = samples.index(s2)
            print('s1: %s, s2: %s, i1: %s, i2: %s, d: %s, p: %s' % (s1, s2, i1, i2, d, p))
            dm[i1,i2] = d
            dm[i2,i1] = d
            pm[i1,i2] = p
            pm[i2,i1] = p

        ids = [os.path.basename(x) for x in samples]
        sk_dm = DissimilarityMatrix(dm, ids=ids)
        sk_pm = DissimilarityMatrix(pm, ids=ids)

        sk_dm.write(output['dist_matrix'])
        sk_pm.write(output['p_matrix'])

#### Mash rules
rule mash:
    input:
        expand(mash_dir + '{sample}/mash/{sample}.msh',
               sample=samples),
        expand(mash_dir + '{sample}/mash/{sample}.refseq.txt',
               sample=samples),
        mash_dir + 'combined_analysis/mash.dist.dm',
        mash_dir + 'combined_analysis/mash.dist.p'

