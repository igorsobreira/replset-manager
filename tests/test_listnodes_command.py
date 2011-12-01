import pytest

from helpers import (remove_state_file, run, assert_mongods_running,
                     kill_running_mongods)

def setup_function(func):
    remove_state_file()
    kill_running_mongods()


def test_should_list_all_running_nodes():
    run('create')
    nodes_info = run('listnodes')

    assert_mongods_running(3)
    assert 3 == nodes_info.count('Node')


@pytest.mark.xfail
def test_should_not_fail_if_no_state_file():
    assert 0
