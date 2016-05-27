#!/usr/bin/python
import sys

__author__ = 'Thomas'

file1 = sys.argv[1]
file2 = sys.argv[2]

identifiers = []
with open(file1, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        identifiers.append([elements])

print identifiers

with open(file2, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        miRID = elements[0].split('-')[1][:-1]
        geneID = elements[1][:14]
        ID_pair = [miRID, geneID]
        print ID_pair
        if ID_pair in identifiers:
            print line
