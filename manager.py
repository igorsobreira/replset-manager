#!/usr/bin/env python

import os
import argparse
import errno

from lib import commands
from lib import state

def main():
    parser = argparse.ArgumentParser(description='MongoDB ReplicaSet Manager')
    subparsers = parser.add_subparsers()

    for command_class_name in commands.__all__:
        command_class = getattr(commands, command_class_name)
        command_parser = subparsers.add_parser(command_class.name,
                                               help=command_class.desc)
        command_parser.set_defaults(func=command_class.call)
        command_class.configure_parser(command_parser)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
