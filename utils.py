import click
from settings import Config, EDGEPORTS

from EdgeTextGenerator import edge_main
from FogNode import fog_main
from CloudNode import cloud_main

fog_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@fog_config
def interface(config, verbose):
    config.verbose = verbose


@interface.command()
@click.argument('text', required=False)
@click.option('--n', default=1, help="Number of lines")
@fog_config
def text_generator(config, text, n):
    edge_main(text, n)


@interface.command()
@fog_config
def fog_node(config):
    fog_main()


@interface.command()
@fog_config
def cloud_node(config):
    cloud_main()
#    central_main()


def main():
    interface()


