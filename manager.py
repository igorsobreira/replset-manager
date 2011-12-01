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
    try:
        nodes = state.load()
    except IOError as ex:
        if ex.errno == errno.ENOENT: # No such file or directory
            print 'No mongod running'
            return

    for node in nodes:
        print ' => Node {0}'.format(node)
        print '  \_ pid: {0}'.format(nodes[node]['pid'])

def do_kill_nodes(args):
    nodes = state.load()

    if 'all' in args.nodes:
        for node, info in nodes.iteritems():
            print 'Killing node {0} with pid {1}'.format(node, info['pid'])
            os.kill(info['pid'], 15)
        state.clear()
    else:
        for node in args.nodes:
            info = nodes.pop(node)
            print 'Killing node {0} with pid {1}'.format(node, info['pid'])
            os.kill(info['pid'], 15)
        state.dump(nodes)

def main():
    parser = argparse.ArgumentParser(description='MongoDB ReplicaSet Manager')
    subparsers = parser.add_subparsers()

    # available commands

    parser_create = subparsers.add_parser('create', help=commands.Create.desc)
    parser_listnodes = subparsers.add_parser('listnodes',
                                             help='List all available nodes')
    parser_killnodes = subparsers.add_parser('killnodes',
                                             help='Kill replica set nodes')

    parser_create.set_defaults(func=do_create)
    parser_listnodes.set_defaults(func=do_list_nodes)
    parser_killnodes.set_defaults(func=do_kill_nodes)    
    
    commands.Create.configure_parser(parser_create)

    # 'listnodes' command options
    
    parser_listnodes.add_argument('--verbose', action='store_true',
                                  help='Show more information')
    
    # 'killnode' command options
    
    parser_killnodes.add_argument('nodes', action='store', nargs='+',
                                  help='Kill these nodes', default='all')
    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
