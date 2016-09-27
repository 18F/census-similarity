#!/usr/bin/env python3
import logging

import click

from census_similarity import commands


@click.group()
def cli():
    """CSV similarity tools for the census"""
    logging.basicConfig(level=logging.DEBUG)


cli.add_command(commands.cluster_by_field)
cli.add_command(commands.group_by)
cli.add_command(commands.lookup)


if __name__ == '__main__':
    cli()
