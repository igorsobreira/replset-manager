import os

import pytest

from replmgr import state, exitcodes
from helpers import run, assert_mongods_running, clear_environ

def setup_function(func):
    clear_environ()

def test_should_start_mongods_and_save_state():
    assert not os.path.isfile(state.filename)
    assert_mongods_running(0)

    run('create')

    assert os.path.isfile(state.filename)
    assert_mongods_running(3)

def test_should_not_allow_create_if_state_file_exists():
    run('create')

    assert os.path.isfile(state.filename)
    assert_mongods_running(3)

    output = run('create')
    assert exitcodes.MONGOD_ALREADY_STARTED == output.exitcode
    assert 'Mongods already started' in output.stderr
    assert 'state file found' in output.stderr

@pytest.mark.xfail
def test_should_do_nothing_on_already_initiated_error():
    # pymongo.errors.OperationFailure: command SON([('replSetInitiate', 1)]) failed: already initialized
    assert 0

@pytest.mark.xfail
def test_should_prompt_if_data_from_previous_databases_already_exists():
    # this causes the error above
    assert 0
