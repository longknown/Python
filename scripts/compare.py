#!/usr/bin/python
import sys

__author__ = 'Thomas'

mir_target = {}  # key: miRNA name; value: target list;

literal_file = sys.argv[1]
predict_file = sys.argv[2]

with open(predict_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        mir = elements[0]
        target = elements[1]
        if mir not in mir_target:
            mir_target[mir] = []
        mir_target[mir].append(target)

with open(literal_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        mir = elements[0]
        target = elements[1]
        if target not in mir_target[mir]:
            print line
