#!/usr/bin/python
import click
import configparser
import os
import re
import sys
import tempfile
import subprocess

DEVNULL  = open(os.devnull, 'w')
FIND_REPLACE_STR = ':%s/{0}/{1}/{2}'

def find_replace_string(find, replace, args):
    return FIND_REPLACE_STR.format(find, replace, args)

def edit_file(config, file_name, format_string):
    EDITOR = os.environ.get('EDITOR', config.editor)
    with open(file_name) as f:
        subprocess.call([EDITOR, '-c', format_string, '+set backupcopy=yes', f.name])
        f.seek(0)
        edited_message = f.read()

def is_ignored_file(name):
    return bool(re.match("\..+", name))

def is_valid_file(path, fname):
    return os.path.isfile(os.path.join(path, fname)) and not is_ignored_file(fname)

def is_valid_dir(path, dirname):
    return os.path.isdir(os.path.join(path, dirname)) and not is_ignored_file(dirname)

def flatten(l):
    return [item for sublist in l for item in sublist]

def find_relevant_files(dir):
    items = os.listdir(dir)
    files = [os.path.join(dir, f) for f in items if is_valid_file(dir, f)]
    dirs  = [os.path.join(dir, d) for d in items if is_valid_dir(dir, d)]
    files.extend(flatten(map(find_relevant_files, dirs)))
    return files

def file_contains_search_string(fname, search_string):
    return subprocess.call(['grep', search_string, fname], stdout=DEVNULL) == 0


class Config(object):

    def __init__(this, editor):
        this.editor = editor

@click.group()
@click.option('--editor', default='vim') 
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
    click.echo('{0} {1} {2} {3}'.format(config.editor, find, replace, directory))
    format_string = find_replace_string(find, replace, 'gc')
    valid_files = find_relevant_files(directory)
    valid_files = filter(lambda f: file_contains_search_string(f, find), valid_files)
    map(lambda fname: edit_file(config, fname, format_string), valid_files)
    

if __name__ == '__main__':
    cli()

