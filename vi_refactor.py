import argparse
import configparser
import os
import re
import sys
import tempfile
import subprocess

SETTINGS = configparser.ConfigParser()
SETTINGS.read(".vi_refactor")

EDITOR = os.environ.get('EDITOR', SETTINGS.get('Editor', 'Name'))
FIND_REPLACE_STR = ':%s/{0}/{1}/{2}'

def find_replace_string(find, replace, args):
    return FIND_REPLACE_STR.format(find, replace, args)

def edit_file(file_name, format_string):
    with open(file_name) as f:
        subprocess.call([EDITOR, '-c', format_string, '+set backupcopy=yes', f.name])
        f.seek(0)
        edited_message = f.read()
        print edited_message

def is_ignored_file(name):
    return bool(re.match("\..+", name))

def find_relevant_files(dir):
    flatten       = lambda l: [item for sublist in l for item in sublist]
    is_valid_file = lambda p, f: os.path.isfile(os.path.join(p, f)) and not is_ignored_file(f)
    is_valid_dir  = lambda p, d: os.path.isdir(os.path.join(p, d)) and not is_ignored_file(d)
    items = os.listdir(dir)
    files = [os.path.join(dir, f) for f in items if is_valid_file(dir, f)]
    dirs  = [os.path.join(dir, d) for d in items if is_valid_dir(dir, d)]
    files.extend(flatten(map(find_relevant_files, dirs)))
    return files

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Refactor your codebase with vi/m.')
    parser.add_argument('find', metavar='find', type=str,
                        help='value to refactor')
    parser.add_argument('replace', metavar='replace', type=str,
                        help='substitution value')
    parser.add_argument('directory', metavar='directory', type=str, 
                        nargs='*',  default='.', 
                        help='directory(s) to refactor files in (default: ./)')
    args = parser.parse_args()
    arg_dict = vars(args)
    format_string = find_replace_string(arg_dict['find'],
                                        arg_dict['replace'],
                                        'gc')
    valid_files = find_relevant_files(arg_dict['directory'])
    map(lambda fname: edit_file(fname, format_string), valid_files)
