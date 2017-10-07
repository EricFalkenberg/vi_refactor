import os
import re
import subprocess

DEVNULL  = open(os.devnull, 'w')
FIND_REPLACE_STR = ':%s/{0}/{1}/{2}'

def find_replace_string(find, replace):
    return FIND_REPLACE_STR.format(find, replace, 'gc')

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

def find_all_files(dir):
    items = os.listdir(dir)
    files = [os.path.join(dir, f) for f in items if is_valid_file(dir, f)]
    dirs  = [os.path.join(dir, d) for d in items if is_valid_dir(dir, d)]
    files.extend(flatten(map(find_all_files, dirs)))
    return files

def file_contains_search_string(fname, search_string):
    return subprocess.call(['grep', search_string, fname], stdout=DEVNULL) == 0

def find_relevant_files(search_string, directory):
    valid_files   = find_all_files(directory)
    return filter(lambda f: file_contains_search_string(f, search_string), valid_files)

def edit_relevant_files(config, format_string, valid_files):
    map(lambda fname: edit_file(config, fname, format_string), valid_files)
