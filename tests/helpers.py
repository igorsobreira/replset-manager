import os
import subprocess
import time
from os.path import dirname, abspath, join

from lib import state


def remove_state_file():
    state.clear()

def kill_running_mongods():
    subprocess.call("ps ax | grep mongod | grep -v grep | awk '{print $1}' | xargs kill",
                    shell=True)
    time.sleep(0.2)

def clear_environ():
    remove_state_file()
    kill_running_mongods()

def run(command):
    manager = abspath(join(dirname(__file__), '..', 'manager.py'))

    if command == 'create':
        command += ' --name testrepl'

    cmd = 'python {0} {1}'.format(manager, command)

    ret = subprocess.check_output(cmd, shell=True)

    if 'killnodes' in command:
        time.sleep(0.2)

    return ret

def assert_mongods_running(count):
    popen = subprocess.Popen('ps ax | grep mongod | grep -v grep',
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    output, err = popen.communicate()
    proc_list = output.strip().split('\n')
    actual_count = len(filter(bool, proc_list))

    assert count == actual_count, \
        "Should have %s mongos running, but %s found" % (count, actual_count)

def assert_no_state_file():
    assert not os.path.isfile(state.filename)
