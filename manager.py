#!/usr/bin/env python


import argparse

import commands

def do_create(args):    
    create = commands.Create(args)
    create.handle()

def do_list_nodes(args):
    print 'list nodes', args

def do_kill_nodes(args):
    print 'kill nodes', args


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
    
    parser_killnodes.add_argument('nodes', action='store', nargs='+', type=int,
                                  help='Kill these nodes')
    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
