#!/usr/bin/python
import click
import click_cmd.rename
import click_cmd.analyze
import os
import subprocess

class Config(object):

    def __init__(this, editor):
        this.editor = editor

@click.group()
@click.option('--editor', default='vim', type=click.Choice(['vi', 'vim'])) 
@click.pass_context
def cli(ctx, editor):
    ctx.obj = Config(editor)

@cli.command()
def version():
    prog_name = __name__.split(".")[-1]
    subprocess.call(["brew", "info", prog_name])

@cli.command()
@click.argument('find')
@click.argument('replace')
@click.argument('directory', default='.', type=click.Path(exists=True, resolve_path=True))
@click.pass_obj
def rename(config, find, replace, directory):
    """Rename all instances of FIND with REPLACE."""
    click.echo("Finding relevant files...")
    format_string = click_cmd.rename.find_replace_string(find, replace)
    valid_files   = click_cmd.rename.find_relevant_files(find, directory)
    click_cmd.rename.edit_relevant_files(config, format_string, valid_files)

@cli.command()
@click.option('--lang', default='java', type=click.Choice(['java']))
@click.argument('directory', default='.', type=click.Path(exists=True, resolve_path=True))
def analyze(lang, directory):
    raise NotImplementedError()

if __name__ == '__main__':
    cli()

