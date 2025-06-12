#!/bin/env python

import os
from sys import argv
from subprocess import check_call
from nnodes import root

root.init()

for _i, node in enumerate(root[0]):
    if node.name in argv:
        print(f"Found {node.name}")
        stationdir = os.path.join(node.db, node.network, node.station)
        print("  resetting...")
        node.reset()
        print(f"  removing {stationdir}")
        check_call(f'rm -rf {stationdir}', shell=True)

        
root.save()                     
