#!/usr/bin/python
import click
import os
from commands import cmd_rename

class Config(object):

    def __init__(this, editor):
        this.editor = editor

@click.group()
@click.option('--editor', default='vim', type=click.Choice(['vi', 'vim'])) 
@click.pass_context
def cli(ctx, editor):
    ctx.obj = Config(editor)

@cli.command()
@click.argument('find')
@click.argument('replace')
@click.argument('directory', default='.', type=click.Path(exists=True, resolve_path=True))
@click.pass_obj
def rename(config, find, replace, directory):
    """Rename all instances of FIND with REPLACE."""
    click.echo("Finding relevant files...")
    format_string = cmd_rename.find_replace_string(find, replace)
    valid_files = cmd_rename.find_relevant_files(find, directory)
    cmd_rename.edit_relevant_files(config, format_string, valid_files)

if __name__ == '__main__':
    cli()

