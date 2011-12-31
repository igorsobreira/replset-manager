MongoDB ReplicaSet Manager
==========================

Command line utility to start and manage a ReplicaSet cluster in MongoDB

Under development
-----------------

It's not done yet. The existing commands _almost_ work... (see issues)

Why?
----

When developing a project using MongoDB I just realized we had this bug
on production, when a primary node crashed and a new node was elected.
But the application didn't survive because we didn't tested with replica
sets (shame on me)!

Since then I've been trying to work with a local replica set. But it's 
boring! You need to start all nodes on different ports (locally)
using different data dirs, call rs.initiate(), and so on...

The initial fase for this project is to help you, developer, to work with a
local replica set on your machine. But it's quite easy to make it work
on any environment if people find it useful.

Hope you enjoy, and contribute!

Usage
-----

    $ ./manager.py -h
    usage: manager.py [-h] {create,killnodes,listnodes} ...

    MongoDB ReplicaSet Manager

    positional arguments:
      {create,killnodes,listnodes}
        create              Create new replica set
        listnodes           List all available nodes
        killnodes           Kill replica set nodes

    optional arguments:
      -h, --help            show this help message and exit

How to contribute
-----------------

#### Create a fork on github (https://github.com/igorsobreira/replset-manager)

#### Install for development:
   
        $ cd replset-manager
        $ pip install -e .

#### Run tests:

        $ ./runtests
        $ ./runtests help

#### Commit(s), push, pull request

#### There a couple scripts on dev-scripts/ you may found useful
