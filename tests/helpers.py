import os
import subprocess
from os.path import dirname, abspath, join

from lib import state


def remove_state_file():
    if os.path.isfile(state.filename):
        os.remove(state.filename)

def run(command):
    manager = abspath(join(dirname(__file__), '..', 'manager.py'))
    cmd = 'python {0} {1} --name testrepl'.format(manager, command)

    subprocess.call(cmd, shell=True, stdout=None)
