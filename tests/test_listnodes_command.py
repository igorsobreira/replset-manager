import pytest

from helpers import (run, assert_mongods_running, assert_no_state_file,
                     clear_environ)

def setup_function(func):
    clear_environ()

def test_should_list_all_running_nodes():
    run('create')
    output = run('listnodes')

    assert_mongods_running(3)
    assert 3 == output.stdout.count('Node')

def test_should_not_fail_if_no_state_file():
    assert_mongods_running(0)
    assert_no_state_file()

    output = run('listnodes')
