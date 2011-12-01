import json
import os.path

filename = '/tmp/replicaset-manager.data'

def dump(state):
    with open(filename, 'w') as fileobj:
        fileobj.write(json.dumps(state))

def load():
    with open(filename, 'r') as fileobj:
        return State(json.loads(fileobj.read()))

def clear():
    if os.path.isfile(filename):
        os.remove(filename)

class State(dict):
    
    def __setattr__(self, attr, value):
        self[attr] = value

    def __getattr__(self, attr):
        return self[attr]
