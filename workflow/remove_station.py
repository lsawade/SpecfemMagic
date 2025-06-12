#!/bin/env python

import os
from sys import argv
from subprocess import checkcall
from nnodes import root

root.init()

for _i, node in enumerate(root):
    if node.name in argv:
        print(f"Found {node.name}")
        stationdir = os.path.join(node.db, node.network, node.station)
        print("  resetting...")
        node.reset()
        print(f"  removing {stationdir}")
        checkcall(f'rm -rf {stationdir}', shell=True)

        
root.save()                     
