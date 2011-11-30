import os
import errno
from subprocess import Popen

class Command(object):
    def __init__(self, args):
        self.args = args

    @classmethod
    def configure_parser(cls, parser):
        raise NotImplementedError

    def handle(self):
        raise NotImplementedError


class Create(Command):

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
        command = ('{mongod} --dbpath={dbpath} --rest --replSet '
                   '{name} --port={port} --logpath {log} &')

        pids = []

        for node in range(self.args.members):
            dbpath = os.path.join(self.args.dbpath, str(node+1))
            logfile = os.path.join(self.args.logsdir, '{0}.log'.format(node+1))

            self.ensure_directory_exists(dbpath)
            self.ensure_directory_exists(self.args.logsdir)
            
            cmd = command.format(mongod=self.args.mongod,
                                 port=self.first_port+node,
                                 name=self.args.name,
                                 dbpath=dbpath,
                                 log=logfile)
            p = Popen(cmd, shell=True)
            pids.append(p.pid)

        print pids
        
    def ensure_directory_exists(self, directory):
        try:
            os.makedirs(directory)
        except OSError, ex:
            if ex.errno != errno.EEXIST:
                raise ex
