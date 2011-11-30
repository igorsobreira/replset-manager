import os
import subprocess
import time
from os.path import dirname, abspath, join

from lib import state


def remove_state_file():
    if os.path.isfile(state.filename):
        os.remove(state.filename)

def run(command):
    manager = abspath(join(dirname(__file__), '..', 'manager.py'))
    cmd = 'python {0} {1} --name testrepl'.format(manager, command)

    subprocess.call(cmd, shell=True, stdout=None)

def assert_mongods_running(count):
    try:
        procs = subprocess.check_output('ps ax | grep mongod | grep -v grep',
                                        shell=True)
    except subprocess.CalledProcessError as ex:
        if count == 0:
            return
        raise ex

    actual_count = len(procs.strip().split('\n'))
    assert count == actual_count, "Should have %s mongos running, but %s found" % (count, actual_count)

def kill_running_mongods():
    subprocess.call("ps ax | grep mongod | grep -v grep | awk '{print $1}' | xargs kill",
                    shell=True)
    time.sleep(0.2)
