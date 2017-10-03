import sys, tempfile, os
from subprocess import call
from curses.ascii import ctrl

ESC = ctrl(']')
EDITOR = os.environ.get('EDITOR', 'vim')

initial_message = "hello world"

with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    tf.write('hello world')
    tf.flush()
    call([EDITOR, '-c' ':%s/hello/bye/gc', '+set backupcopy=yes', tf.name])
    tf.seek(0)
    edited_message = tf.read()
    print edited_message

