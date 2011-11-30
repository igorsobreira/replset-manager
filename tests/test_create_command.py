import os

from lib import state

from helpers import remove_state_file, run

def setup_function(func):
    remove_state_file()


def test_should_save_state():
    assert not os.path.isfile(state.filename)

    run('create')

    assert os.path.isfile(state.filename)
