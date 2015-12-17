#!/usr/bin/python
import sys

__author__ = 'Thomas'

mirmap_file = sys.argv[1]
exp_file = sys.argv[2]

fout = open('output', 'w')

exp = {}
with open(exp_file) as f1:
    header = f1.readline()
    fout.write(header)
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        ID = elements[0]
        exp[ID] = elements[1:]
with open(mirmap_file) as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        ID = elements[0]
        uuid = elements[1]
        line_list = [uuid] + exp[ID]
        output_line = '\t'.join(line_list)
        fout.write(output_line+'\n')

fout.close()
