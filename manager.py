#!/usr/bin/env python

import os
import argparse
import errno

from lib import commands
from lib import state


def do_create(args):    
    create = commands.Create(args)
    create.handle()

def do_list_nodes(args): 
    list_nodes = commands.ListNodes(args)
    list_nodes.handle()

def do_kill_nodes(args):
    kill_nodes = commands.KillNodes(args)
    kill_nodes.handle()

def main():
    parser = argparse.ArgumentParser(description='MongoDB ReplicaSet Manager')
    subparsers = parser.add_subparsers()

    # available commands

    parser_create = subparsers.add_parser('create', help=commands.Create.desc)
    parser_listnodes = subparsers.add_parser('listnodes', help=commands.ListNodes.desc)
    parser_killnodes = subparsers.add_parser('killnodes', help=commands.KillNodes.desc)

    parser_create.set_defaults(func=do_create)
    parser_listnodes.set_defaults(func=do_list_nodes)
    parser_killnodes.set_defaults(func=do_kill_nodes)    
    
    commands.Create.configure_parser(parser_create)
    commands.ListNodes.configure_parser(parser_listnodes)
    commands.KillNodes.configure_parser(parser_killnodes)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
