#!/bin/env python

from sys import argv
from nnodes import root

root.init()

for _i, node in enumerate(root):
    if node.name in argv[1]:
        print(f"Found {node.name}")

        for _j, sim in enumerate(node[1]):
            if sim.name[-1] == argv[2]:
                print(f'  Found {sim.name[-1]}')
                sim.reset()

root.save()
