import os

from lib import state

from helpers import run, assert_mongods_running, clear_environ

def setup_function(func):
    clear_environ()

def test_should_start_mongods_and_save_state():
    assert not os.path.isfile(state.filename)
    assert_mongods_running(0)

    run('create')

    assert os.path.isfile(state.filename)
    assert_mongods_running(3)
