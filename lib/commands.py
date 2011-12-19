import os
import errno
import pprint
import time
import subprocess
import sys

import pymongo

from lib import state, exitcodes
from lib.colors import red

__all__ = 'Create', 'ListNodes', 'KillNodes'

class Command(object):
    '''
    Abstract class to all command
    '''

    def __init__(self, args):
        self.args = args

    @classmethod
    def configure_parser(cls, parser):
        raise NotImplementedError

    def handle(self):
        raise NotImplementedError

    @classmethod
    def call(cls, args):
        cls(args).handle()

    def load_state(self):
        try:
            return state.load()
        except IOError as ex:
            if ex.errno == errno.ENOENT: # No such file or directory
                print 'No mongod running'
                exit(0)

    def info(self, msg, format=False):
        if format:
            pprint.pprint(msg)
        else:
            print(msg)
    
    def error(self, msg):
        sys.stderr.write(red(msg + "\n"))

class Create(Command):

    name = 'create'
    desc = 'Create new replica set'
    first_port = 27001

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--name', action='store', nargs='?', required=True,
                            help='The replica set name')
        parser.add_argument('--members', action='store', nargs='?', default=3,
                            help='How many members this replica set should have. '
                            '3 by default')
        parser.add_argument('--dbpath', action='store', nargs='?', default='/tmp/data',
                            help='Directory for datafiles. "/tmp/data" by default')
        parser.add_argument('--mongod', action='store', nargs='?', default='mongod',
                            help='`mongod` executable')
        parser.add_argument('--logsdir', action='store', nargs='?', default='/tmp/logs',
                            help='Directory to store nodes logs')

    def handle(self):
        self.exit_if_existing_state_file()

        command = ('{mongod} --dbpath={dbpath} --rest --replSet '
                   '{name} --port={port} --logpath {log}')
        nodes = {}

        for node in range(self.args.members):
            dbpath = os.path.join(self.args.dbpath, str(node+1))
            logfile = os.path.join(self.args.logsdir, '{0}.log'.format(node+1))

            self.ensure_directory_exists(dbpath)
            self.ensure_directory_exists(self.args.logsdir)
            port = self.first_port+node

            cmd = command.format(mongod=self.args.mongod,
                                 port=port,
                                 name=self.args.name,
                                 dbpath=dbpath,
                                 log=logfile)
            self.info("Starting node {0} ({1})".format(node+1, cmd))
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            nodes[node+1] = {'pid': p.pid, 'port': port, 'host': 'igormac'}

        self.initiate(nodes)
        state.dump(nodes)
        self.info("Use `listnodes` command for more information about each node")

    def exit_if_existing_state_file(self):
        if state.exists():
            self.error("Mongods already started")
            self.error("(state file found on '{0}')".format(state.filename))
            exit(exitcodes.MONGOD_ALREADY_STARTED)
        
    def ensure_directory_exists(self, directory):
        try:
            os.makedirs(directory)
        except OSError, ex:
            if ex.errno != errno.EEXIST:
                raise ex

    def initiate(self, nodes):
        self.info('Initiating replica set')
        primary = nodes[1]
        admin = None
        limit = 5
        while not admin:
            if limit == 0:
                self.error('Primary not found. Give up!')
                self.error('Fail.')
                return
            limit -= 1

            try:
                admin = pymongo.Connection(primary['host'],
                                           primary['port'],
                                           slave_okay=True).admin
            except pymongo.errors.AutoReconnect:
                time.sleep(0.5)
                self.info('Primary not found yet... retrying')

        result = admin.command('replSetInitiate')
        self.info(result, format=True)
        self.info('ok')

class ListNodes(Command):

    name = 'listnodes'
    desc = 'List all available nodes'
    
    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--verbose', action='store_true',
                            help='Show more information')
    

    def handle(self):
        nodes = self.load_state()

        for node in nodes:
            print ' => Node {0}'.format(node)
            print '  \_ pid: {0}'.format(nodes[node]['pid'])


class KillNodes(Command):

    name = 'killnodes'
    desc = 'Kill replica set nodes'

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('nodes', action='store', nargs='+',
                            help="Kill specific nodes by id or 'all'", 
                            default='all')
    
    def handle(self):
        nodes = self.load_state()

        if 'all' in self.args.nodes:
            for node, info in nodes.iteritems():
                print 'Killing node {0} with pid {1}'.format(node, info['pid'])
                os.kill(info['pid'], 15)
            state.clear()
        else:
            for node in self.args.nodes:
                info = nodes.pop(node)
                print 'Killing node {0} with pid {1}'.format(node, info['pid'])
                os.kill(info['pid'], 15)
            state.dump(nodes)
