#!/usr/bin/python
import sys

__author__ = 'Thomas'

file1 = sys.argv[1]
file2 = sys.argv[2]

chosen_set = []
with open(file1, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        mir = elements[0]
        gene = elements[1]
        chosen_set.append([mir, gene])


with open(file2, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        mirname = elements[0]
        genename = elements[1]
        for pair in chosen_set:
            if pair[0] in mirname and pair[1] in genename:
                print line
