import json

filename = '/tmp/replicaset-manager.data'

def dump(state):
    with open(filename, 'w') as fileobj:
        fileobj.write(json.dumps(state))

def load():
    with open(filename, 'r') as fileobj:
        return State(json.loads(fileobj.read()))

class State(dict):
    
    def __setattr__(self, attr, value):
        self[attr] = value

    def __getattribute__(self, attr):
        return self[attr]
