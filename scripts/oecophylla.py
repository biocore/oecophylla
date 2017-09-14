import click

@click.group()
def run():
    pass

@run.command()
@click.option('--config-file',
              help='Input biom table of abundances')
def workflow():
    pass

if __name__ == "__main__":
    run()
