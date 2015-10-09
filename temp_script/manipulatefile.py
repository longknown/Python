#!/usr/bin/python
import sys

__author__ = 'Thomas'

file1 = sys.argv[1]
file2 = sys.argv[2]
fout = open('mir_exp', 'w')

id_mir = {}
with open(file1, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        _id = elements[0]
        mirna = elements[1]
        id_mir[_id] = mirna

with open(file2, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        _id = elements[0]
        if _id in id_mir:
            elements[0] = id_mir[_id]
            outputline = '\t'.join(elements)
            fout.write(outputline+'\n')

fout.close()
