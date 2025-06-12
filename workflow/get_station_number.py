#!/bin/env python

import os
from sys import argv
from subprocess import check_call
from nnodes import root

root.init()

for _i, node in enumerate(root):
    if node.name in argv:
        print(f"{argv[1]} is number {_i} in the workflow.")
