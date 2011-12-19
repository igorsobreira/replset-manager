import os
import subprocess
import time
import shutil
from os.path import dirname, abspath, join

from lib import state

test_logfile = abspath(join(dirname(__file__), 'test-output.log'))
test_dbpath = '/tmp/test-data'

def remove_state_file():
    state.clear()

def remove_tmp_dirs():
    shutil.rmtree(test_dbpath, ignore_errors=True)

def kill_running_mongods():
    subprocess.call("ps ax | grep mongod | grep -v grep | awk '{print $1}' | xargs kill",
                    shell=True)
    time.sleep(0.2)

def clear_environ():
    remove_state_file()
    remove_tmp_dirs()
    kill_running_mongods()

def run(command):
    manager = abspath(join(dirname(__file__), '..', 'manager.py'))

    if command == 'create':
        command += ' --name testrepl'
        command += ' --dbpath ' + test_dbpath

    cmd = 'python {0} {1}'.format(manager, command)

    popen = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    out, err = popen.communicate()

    if 'killnodes' in command:
        time.sleep(0.2)

    write_test_log(' ==> Output for command %r' % cmd)
    write_test_log(out)
    write_test_log(err)

    output = type('Output', (object,), 
                  {'stdout': out,
                   'stderr': err,
                   'exitcode': popen.returncode})

    return output()

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

def write_test_log(string):
    with open(test_logfile, 'a') as fileobj:
        fileobj.write(string)
        fileobj.write('=' * 100)
        fileobj.write('\n')
