import os
import errno

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
        parser.add_argument('--dbpath', action='store', nargs='?', default='/data',
                            help='Directory for datafiles. "/data" by default')
        parser.add_argument('--mongod', action='store', nargs='?', default='mongod',
                            help='`mongod` executable')

    def handle(self):
        command = '{mongod} --dbpath={dbpath} --rest --replSet {name} --port={port} &'

        for node in range(self.args.members):
            dbpath = os.path.join(self.args.dbpath, str(node+1))
            self.ensure_directory_exists(dbpath)
            
            cmd = command.format(mongod=self.args.mongod,
                                 port=self.first_port+node,
                                 dbpath=dbpath,
                                 name=self.args.name)
            print(cmd)
        
        
    def ensure_directory_exists(self, directory):
        try:
            os.makedirs(directory)
        except OSError, ex:
            if ex.errno != errno.EEXIST:
                raise ex