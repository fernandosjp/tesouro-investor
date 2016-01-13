import click
from alerter import Alerter

@click.group()
def cli():
    pass

@cli.command()
@click.argument('config', default="config.yml",type=click.Path(exists=True))
@click.argument('alerts', default="alerts.json", type=click.Path(exists=True))
def alert(**kwargs):
	alert = Alerter(kwargs['alerts'],kwargs['config'])
	alert.alert()

if __name__ == '__main__':
    cli()


