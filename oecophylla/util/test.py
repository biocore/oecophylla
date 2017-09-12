rule test_temp_expand:
    input:
        "test.fa"
    output:
        temp(
            expand("out_{sample}.temp",
                   sample=config['binning_samples'])
            )
    run:
        for f in output:
            print("wildcards")
            print(  wildcards)
            shell("echo '{f}' > {f}")

rule test_merge:
    input:
        expand("out_{sample}.temp",
                   sample=config['binning_samples'])
    output:
        "testout.fa"
    run:
        print(wildcards)
        f_list = ' '.join(input)
        shell("cat {f_list} > {output}")