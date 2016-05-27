#!/usr/bin/python
import sys
'''
    This script helps to extract the cultivars and counting the cultivar numbers;
    Cultivars would be stored in a file; Cultivar numbers would be shown directly;
'''
__author__ = 'Thomas'

cultivarFile = sys.argv[1]
patternFile = sys.argv[2]
_mirna = sys.argv[3]
_target = sys.argv[4]

outfile = open('cultivars.txt', 'w')

refdict = {}
with open(cultivarFile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        mirna = elements[0]
        target = elements[1]
        pattern = elements[2]
        cultivars = elements[3]
        if cultivars == '':
            print 'Alert, no cultivars: %s' % line
        temp_key = mirna + ':' + target + ':' + pattern
        refdict[temp_key] = cultivars

count = 0
with open(patternFile, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')

        temp_key = _mirna + ':' + _target + ':' + line
        if temp_key not in refdict:
            print 'Alert, this pattern is not found: %s' % line
            continue
        cultivars = refdict[temp_key]
        count += cultivars.count(',') + 1
        outfile.write(line+'\t'+cultivars+'\n')

print count
