import click
import json
import os
import glob

"""
This is the main Oecophylla script which handles launching of the entire
pipeline and installation of all necessary modules/environments.
Using a set of FASTA/FASTQ input files,
sample sheet (Illumina-specific) and tool parameters file,
it launches the Snakemake pipeline, either locally or on a supported
cluster system (Torque, Slurm).

Example usage:
==============

Installation:
-------------
oecophylla install

Execute Workflow:
-----------------
oecophylla workflow --input-dir ./inputs --sample-sheet sample.txt --params params.json --output-dir ./outputs

"""


@click.group()
def run():
    pass


def _arg_split(ctx, param, value):
    # split columns by ',' and remove whitespace
    _files = [c.strip() for c in value.split(',')]
    return _files


def _create_dir(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

@run.command()
@click.option('--input-dir', '-i', required=True, type=click.STRING,
              callback=_arg_split,
              help='Input directory with all of the samples.')
@click.option('--sample-sheet', '-s', required=True, type=click.STRING,
              callback=_arg_split,
              help='Sample sheets used to demultiplex the Illumina run.')
@click.option('--params', '-p', type=click.PATH, required=True,
              help='Specify parameters for the tools in a JSON file.')
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
    from skbio.io.registry import sniff

    # INPUT DIR
    for inp_file in glob.glob('%s/*' % input_dir):
        file_format = sniff(inp_file)[0]
        if (file_format != 'fasta') or (file_format != 'fastq'):
            raise TypeError('Input files need to be in FASTA or FASTQ format.')

    # SAMPLE SHEET
    # If a manifest is not specified, the files containing forward and reverse reads
    # will be automatically identified using regex.


    # OUTPUT
    # create output directory, if does not exist
    _create_dir(output_dir)

    # PARAMS


    # LOGS
    if log_dir:
        _create_dir(log_dir)
    else:
        os.makedirs('%s/%s' % (output_dir, 'cluster_logs'))

    # CLUSTER SETUP


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
@click.option('--config-file', default=None,
              help='Configuration file defining specific installations of all'
                   ' modules.')
def install():
    """ This replaces the install.sh

    This will spit out a config file with environment parameters.
    This configuration file will be implicitly passed to the other
    commands.
    """
    if not config_file:
        import install

if __name__ == "__main__":
    run()
