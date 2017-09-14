import click
try:
    import snakemake
except ImportError:
    import subprocess
    subprocess.call(["source activate", 'oecophylla'])
    import snakemake
"""
notes
-----

we need to activate the environment first 

expected functionality:
  * torque submission
  * slurm submission (flag --cluster-queue)
  * local run (flag --cluster-queue local)

  * option to generate only config files (flag)
"""

@click.group()
def run():
    pass

@run.command()
@click.option('--config-file',
              help='Paths to databases')
@click.option('--params-file',
	      help='Tool parameters')
@click.option('--manifest',
              help='Paths to input files; preparation information.')
def workflow():
    pass

if __name__ == "__main__":
    run()
