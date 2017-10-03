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
    parser.add_argument('find_pattern', metavar='find_pattern', type=str,
                        help='value to refactor')
    parser.add_argument('replace_pattern', metavar='replace_pattern', type=str,
                        help='substitution value')
    parser.add_argument('directory', metavar='directory(s)', type=str, 
                        nargs='*',  default='.', 
                        help='directory(s) to refactor files in (default: ./)')
    args = parser.parse_args()
    arg_dict = vars(args)
    format_string = find_replace_string(arg_dict['find_pattern'],
                                        arg_dict['replace_pattern'],
                                        'gc')
    edit_file('test_files/test.txt', format_string)

