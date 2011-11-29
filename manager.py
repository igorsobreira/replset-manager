#!/usr/bin/env python

import argparse

def do_create(args):
    print 'create ', args

def do_list_nodes(args):
    print 'list nodes', args

def do_kill_nodes(args):
    print 'kill nodes', args

def main():
    parser = argparse.ArgumentParser(description='MongoDB ReplicaSet Manager')
    subparsers = parser.add_subparsers()

    # available commands

    parser_create = subparsers.add_parser('create',
                                          help='Create new replica set')
    parser_listnodes = subparsers.add_parser('listnodes',
                                             help='List all available nodes')
    parser_killnodes = subparsers.add_parser('killnodes',
                                             help='Kill replica set nodes')

    parser_create.set_defaults(func=do_create)
    parser_listnodes.set_defaults(func=do_list_nodes)
    parser_killnodes.set_defaults(func=do_kill_nodes)
    
    # 'create' command options
    
    parser_create.add_argument('--name', action='store', nargs='?', required=True,
                               help='The replica set name')
    parser_create.add_argument('--members', action='store', nargs='?', default=3,
                               help='How many members this replica set should have. 3 by default')
    parser_create.add_argument('--dbpath', action='store', nargs='?', default='/data',
                               help='Directory for datafiles. "/data" by default')
    
    # 'listnodes' command options
    
    parser_listnodes.add_argument('--verbose', action='store_true',
                                  help='Show more information')
    
    # 'killnode' command options
    
    parser_killnodes.add_argument('nodes', action='store', nargs='+', type=int,
                                  help='Kill these nodes')
    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
