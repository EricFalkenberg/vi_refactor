import argparse
import os
import sys
import tempfile
import subprocess

EDITOR = os.environ.get('EDITOR', 'vim')
FIND_REPLACE_STR = ':%s/{0}/{1}/{2}'

def find_replace_string(find, replace, args):
    return FIND_REPLACE_STR.format(find, replace, args)

def edit_file(file_name, format_string):
    with open(file_name) as f:
        subprocess.call([EDITOR, '-c', format_string, '+set backupcopy=yes', f.name])
        f.seek(0)
        edited_message = f.read()
        print edited_message

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Refactor your codebase with vi/m.')
    args = parser.parse_args()
    edit_file('test.txt', find_replace_string("hello", "goodbye", "gc"))

