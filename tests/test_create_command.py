import os

from lib import state

from helpers import (remove_state_file, run, assert_mongods_running,
                     kill_running_mongods)

def setup_function(func):
    remove_state_file()
    kill_running_mongods()


def test_should_start_mongods_and_save_state():
    assert not os.path.isfile(state.filename)
    assert_mongods_running(0)

    run('create')

    assert os.path.isfile(state.filename)
    assert_mongods_running(3)
