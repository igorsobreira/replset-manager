import json
import os

import pytest

from replmgr import state
from replmgr.state import State

from helpers import remove_state_file

def setup_function(func):
    remove_state_file()

def test_state_should_behave_like_dict():
    state = State()
    state.pids = [1,2]

    assert [1,2] == state['pids']

def test_dump_should_persist_state_in_file():
    s = State()
    s.database = 'mongodb'
    s.pids = [123, 312]
    
    state.dump(s)

    try:
        with open(state.filename) as fileobj:
            data = json.load(fileobj)
    except TypeError:
        pytest.fail("%r should not be empty" % state.filename)
    except ValueError:
        pytest.fail("%r should be JSON" % state.filename)
    
    assert {'database': 'mongodb', 'pids': [123, 312]} == data

def test_stateloader_should_load_existing_state(tmpdir):
    state.dump({'pids': [1,2]})

    s = state.load()
    
    assert isinstance(s, State)
    assert [1,2] == s.pids

def test_clear_should_remove_state_file():
    state.dump({'foo': 'bar'})

    assert os.path.isfile(state.filename)
    state.clear()
    assert not os.path.isfile(state.filename)
