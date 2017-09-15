import click

@click.group()
def run():
    pass


def _arg_split(ctx, param, value):
    # split columns by ',' and remove whitespace
    _files = [c.strip() for c in value.split(',')]
    return _files

@run.command()
@click.option('--input-dir', required=True, type=click.STRING,
              callback=_arg_split,
              help='Input directories of all of the samples.')
@click.option('--sample-sheet', required=True, type=click.STRING,
              callback=_arg_split,
              help='Sample sheets used to demultiplex the illumina run.')
@click.option('--params', type=click.PATH, required=True,
              help='Specify parameters for the tools.')
@click.option('--local-scratch', type=click.PATH, required=False,
              help='Temporary directory for storing intermediate files.')
@click.option('--log-dir', type=click.PATH, required=False,
              help='Directory containing log files.')
@click.option('--restart', is_flag=True, default=False,
              help='Restarts the run and overwrites previous input.')
@click.option('--output-dir',
              help='Input directory of all of the samples.')
# TODO: extra snakemake parameters with defaults

# TODO: everything past here will be passed directly into snakemake
def local_workflow():
    """

    If a manifest is not specified, the files containing forward and reverse reads
    will be automatically identified using regex.

    """

    # --no-lock?

    # parameters, samples and environmental variables will all have to be concatenated
    # together to feed into snakemake.
    pass

@run.command()
@click.option('--input-dir',
              help='Input directory of all of the samples.')
@click.option('--manifest',
              help='Manifest file containing all of the paths (csv file).')
@click.option('--params',
              help='Specify parameters for the tools.')
@click.option('--cluster-file',
              help='Input biom table of abundances.')
@click.option('--local-scratch',
              help='Temporary directory for storing intermediate files.')
@click.option('--qsub/--slurm', is_flag=True,
              help='Temporary directory for storing intermediate files.')
@click.option('--log-dir',
              help='Directory containing log files.')
@click.option('--output-dir',
              help='Input directory of all of the samples.')
def cluster_workflow():
    """

    If a manifest is not specified, the files containing forward and reverse reads
    will be automatically identified using regex.

    """

    # below are some examples of cluster inputs
    # -j 16 --local-cores 4 -w 90 --cluster-config cluster.json
    # --cluster "qsub -e {cluster.error} -o {cluster.output} -m n -l nodes=1:ppn={cluster.n} -l mem={cluster.mem}gb -l walltime={cluster.time}"

    pass

@run.command()
@click.option('--config-file',
              help='Input biom table of abundances (optional)')
def install():
    """ This replaces the install.sh

    This will spit out a config file with environment parameters.
    This configuration file will be implicitly passed to the other
    commands.
    """
    pass


if __name__ == "__main__":
    run()
