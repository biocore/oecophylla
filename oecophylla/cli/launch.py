import click
import yaml
import os
import glob
from oecophylla.util.parse import (illumina_filenames_to_df,
                                   extract_sample_reads,
                                   add_filter_db,
                                   extract_sample_paths,
                                   read_sample_sheet,
                                   extract_samples_from_sample_sheet)
import subprocess

"""
This is the main Oecophylla script which handles launching of the entire
pipeline and installation of all necessary modules/environments.
Using a set of FASTA/FASTQ input files,
sample sheet (Illumina-specific) and tool parameters file,
it launches the Snakemake pipeline, either locally or on a supported
cluster system (Torque, Slurm).

Example usage:
==============

*NOT FUNCTIONAL AS OF NOW*
Installation:
-------------
oecophylla install

Execute Workflow:
-----------------
oecophylla workflow --input-dir ./inputs --sample-sheet sample.txt --params params.yaml --output-dir ./outputs

"""


@click.group()
def run():
    pass


#TODO will be used, once we add multiple directory support
def _arg_split(ctx, param, value):
    # split columns by ',' and remove whitespace
    _files = [c.strip() for c in value.split(',')]
    return _files


def _create_dir(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)


@run.command()
@click.argument('targets', nargs=-1)
#TODO add an option to process multiple directories
@click.option('--input-dir', '-i', required=True, type=click.STRING,
              help='Input directory with all of the samples.')
#TODO add an option to process multiple directories
@click.option('--sample-sheet', '-s', required=False, type=click.STRING,
              default=None,
              help='Sample sheets used to demultiplex the Illumina run.')
@click.option('--params', '-p', type=click.Path(exists=True), required=True,
              help='Specify parameters for the tools in a YAML file.')
@click.option('--envs', '-e', type=click.Path(exists=True), required=True,
              help='Specify environments for the tools in a YAML file.')
@click.option('--cluster-config', type=click.Path(), required=False,
              help='File with parameters for a cluster job.')
@click.option('--local-scratch', type=click.Path(resolve_path=True,
              writable=True),
              default='/tmp',
              help='Temporary directory for storing intermediate files.')
@click.option('--workflow-type',
              type=click.Choice(['torque', 'slurm', 'local']),
              default='local',
              help='Select where to run the pipeline (cluster or locally).')
@click.option('--output-dir', '-o', type=click.Path(),
              help='Input directory of all of the samples.')
@click.option('--snakemake-args', type=click.STRING, default='',
              help=('arguments to pass into snakemake '
                    '(needs to be passed in by quotes)'))
@click.option('--local-cores', '-j', required=False, type=click.INT, default=2,
              help='Number of local cores to run for snakemake scheduler.')
@click.option('--jobs', '-j', required=False, type=click.INT, default=None,
              help='Number of processes to run.  When running on the cluster, '
              'this corresponds to the number of jobs to launch.')
@click.option('--force', is_flag=True, default=False,
              help='Restarts the run and overwrites previous input.')
@click.option('--just-config', is_flag=True, flag_value=False,
              help='Only generate the configuration file.')
def workflow(targets, input_dir, sample_sheet, params, envs,
             cluster_config, local_scratch, workflow_type, output_dir,
             snakemake_args, local_cores, jobs,
             force, just_config):
    import snakemake
    from skbio.io.registry import sniff

    # SNAKEMAKE
    snakefile = "%s/../../Snakefile" % os.path.abspath(os.path.dirname(__file__))

    # INPUT DIR
    for inp_file in glob.glob('%s/*' % input_dir):

        file_format = sniff(inp_file)[0]

        if (file_format != 'fasta') and (file_format != 'fastq'):
            raise TypeError('Input files need to be in FASTA or FASTQ format.')

    # OUTPUT
    # create output directory, if does not exist
    _create_dir(output_dir)

    # SAMPLE SHEET
    # If a manifest is not specified, the files containing forward and reverse reads
    # will be automatically identified using regex.
    if sample_sheet:
        _sheet = read_sample_sheet(sample_sheet)
        sample_dict = extract_samples_from_sample_sheet(_sheet, input_dir)
    else:
        sample_dict = extract_sample_paths(input_dir)

    # PARAMS
    with open(params, 'r') as f:
        params_dict = yaml.load(f)

    # ENVS
    with open(envs, 'r') as f:
        envs_dict = yaml.load(f)

    # CONFIG
    # merge PARAMS, SAMPLE_DICT, ENVS
    config_dict = {}
    config_dict['samples'] = sample_dict
    config_dict['params'] = params_dict
    config_dict['envs'] = envs_dict
    config_dict['tmp_dir_root'] = local_scratch

    config_yaml = yaml.dump(config_dict, default_flow_style=False)



    config_fp = '%s/%s' % (output_dir, 'config.yaml')
    with open(config_fp, 'w') as f:
        f.write(config_yaml)

    # TODO: LOGS
    # if log_dir:
    #     _create_dir(log_dir)
    # else:
    #     os.makedirs('%s/%s' % (output_dir, 'cluster_logs'))
    if workflow_type == 'torque':
        cluster_setup = "\"qsub -e {cluster.error} -o {cluster.output} \
                         -m {cluster.email} \
                         -l nodes=1:ppn={cluster.nodes} \
                         -l mem={cluster.memory} \
                         -l walltime={cluster.time}\" "

        if jobs == None:
            jobs = 16

        cmd = ' '.join(["snakemake ",
                        "--snakefile %s " % snakefile,
                        "--local-cores %s " % local_cores,
                        "--jobs %s " % jobs,
                        "--cluster-config %s " % cluster_config,
                        "--cluster %s "  % cluster_setup,
                        "--configfile %s " % config_fp,
                        "--directory %s " % output_dir,
                        snakemake_args,
                        ' '.join(targets)])
    elif workflow_type == 'slurm':
        cluster_setup = "srun -e {cluster.error} -o {cluster.output} \
                         -mail-user={cluster.email} \
                         -n {cluster.nodes} \
                         --mem={cluster.memory} \
                         --time={cluster.time}"
        if jobs == None:
            jobs = 16

        cmd = ' '.join(["snakemake ",
                        "--snakefile %s " % snakefile,
                        "--local-cores %s " % local_cores,
                        "--jobs %s " % jobs,
                        "--cluster-config %s " % cluster_config,
                        "--cluster %s " % cluster_setup,
                        "--configfile % s " % config_fp,
                        "--directory %s " % output_dir,
                        snakemake_args,
                        ' '.join(targets)])

    elif workflow_type == 'local':

        if jobs == None:
            jobs = 2

        cluster_setup = None
        cmd = ' '.join(["snakemake ",
                        "--snakefile %s " % snakefile,
                        "--local-cores %s " % local_cores,
                        "--jobs %s " % jobs,
                        "--directory %s " % output_dir,
                        "--configfile %s " % config_fp,
                        snakemake_args,
                        ' '.join(targets)])
    else:
        raise ValueError('Incorrect workflow-type specified in launch script.')

    if not just_config:
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()


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

