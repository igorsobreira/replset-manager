from distutils.core import setup
from os.path import dirname, join, abspath

README = abspath(join(dirname(__file__), 'README.md'))
with open(README) as fileobj:
    long_description = fileobj.read()

setup(name='replset-manager',
      version='0.1',
      description='MongoDB ReplicaSet Manager',
      long_description=long_description,
      author='Igor Sobreira',
      author_email='igor@igorsobreira.com',
      url='https://github.com/igorsobreira/replset-manager',
      packages=['replmgr'],
      scripts=['scripts/replmgr'],
      requires=['pymongo']
      )
