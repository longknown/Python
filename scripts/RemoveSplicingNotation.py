#!/usr/bin/python
import sys
__author__ = 'Thomas'

inputFile = sys.argv[1]

with open(inputFile, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split('\t')
        mirna = elements[0]
        target = elements[1]
        pattern = elements[3]
        cultivars = elements[-1]

        print '\t'.join([mirna, target.split('.')[0], pattern, cultivars])
