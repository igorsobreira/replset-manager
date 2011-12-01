
from helpers import run, assert_mongods_running, clear_environ, assert_no_state_file

def setup_function(func):
    clear_environ()

def test_kill_all_should_kill_all_nodes_and_remove_state_file():
    run('create')
    assert_mongods_running(3)

    run('killnodes all')
    assert_mongods_running(0)
    assert_no_state_file()
