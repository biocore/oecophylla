import click
import json
import os

"""
This is the main Oecophylla script which handles launching of the entire
pipeline.


"""


@click.group()
def run():
    pass


def _arg_split(ctx, param, value):
    # split columns by ',' and remove whitespace
    _files = [c.strip() for c in value.split(',')]
    return _files

@run.command()
@click.option('--input-dir', '-i', required=True, type=click.STRING,
              callback=_arg_split,
              help='Input directory with all of the samples.')
@click.option('--sample-sheet', '-s', required=True, type=click.STRING,
              callback=_arg_split,
              help='Sample sheets used to demultiplex the Illumina run.')
@click.option('--params', '-p', type=click.PATH, required=True,
              help='Specify parameters for the tools.')
@click.option('--cluster-params', type=click.PATH, required=False,
              help='File with parameters for a cluster job.')
@click.option('--local-scratch', type=click.PATH, default='/tmp'
              help='Temporary directory for storing intermediate files.')
@click.option('--run-location',
              type=click.Choice(['torque', 'slurm', 'local']),
              default='local',
              help='Temporary directory for storing intermediate files.')
@click.option('--log-dir', type=click.PATH, required=False,
              default='/dev/null',
              help='Directory containing log files.')
@click.option('--output-dir', '-o', type=click.PATH, required=True,
              help='Input directory of all of the samples.')
@click.option('--restart', is_flag=True, default=False,
              help='Restarts the run and overwrites previous input.')
# TODO: extra snakemake parameters with defaults
# TODO: everything past here will be passed directly into snakemake
def workflow():
    import snakemake
    from skbio.io.registry import Format

    # INPUT DIR
    # sniff with scikit bio

    # SAMPLE MANIFEST
    # If a manifest is not specified, the files containing forward and reverse reads
    # will be automatically identified using regex.


    # OUTPUT


    # LOGS
    if log_dir:
        if not os.path.exists(directory):
            os.makedirs(directory)
    else:
        os.makedirs('%s/%s' % (output_dir, 'cluster_logs'))


    snakefile = "%s/../Snakefile" % __file__
    with open(cluster_params) as _file:
        cluster = json.load(_file)
    # TODO cluster queue logic

    snakemake.snakemake(snakefile, listrules=False, list_target_rules=False,
                        cores=cluster['cores'],
                        nodes=cluster['nodes'],
                        local_cores=cluster['local_cores'],
                        resources={},
                        config={}, configfile=None, config_args=None,
                        workdir=None, targets=None, dryrun=False, touch=False,
                        forcetargets=False, forceall=False, forcerun=[],
                        until=[], omit_from=[], prioritytargets=[], stats=None,
                        printreason=False, printshellcmds=False,
                        debug_dag=False)
    # --no-lock?

    # parameters, samples and environmental variables will all have to be concatenated
    # together to feed into snakemake.


    # below are some examples of cluster inputs
    # -j 16 --local-cores 4 -w 90 --cluster-config cluster.json
    # --cluster "qsub -e {cluster.error} -o {cluster.output} -m n -l nodes=1:ppn={cluster.n} -l mem={cluster.mem}gb -l walltime={cluster.time}"


@run.command()
@click.option('--config-file',
              help='Input biom table of abundances (optional)')
def install():
    """ This replaces the install.sh

    This will spit out a config file with environment parameters.
    This configuration file will be implicitly passed to the other
    commands.
    """

if __name__ == "__main__":
    run()
