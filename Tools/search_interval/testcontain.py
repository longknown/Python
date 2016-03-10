#!/usr/bin/python
__author__ = 'Thomas'

import sys
import os

from Python.Tools.plink_parser.Fuse_intervals import Interval, IntervalSet




# To obtain all genome coords according to filename
path = sys.argv[1]
coord_f = sys.argv[2]
chr_iv = {}  # store dict, key: chr id / value: IntervalSet

for i in os.listdir(path):
    if i[-3:] != 'zip':
        continue
    part = i.split('-')
    chr_id = part[1][3:]
    start = int(part[2])
    end = int(part[3])
    iv1 = Interval(start, end)
    if chr_id not in chr_iv:
        chr_iv[chr_id] = IntervalSet(iv1)
    else:
        chr_iv[chr_id].insert(iv1)

with open(coord_f, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        chr_id = elements[0]
        start = int(elements[1])
        end = int(elements[2])
        iv_test = Interval(start, end)
        if iv_test not in chr_iv[chr_id]:
            print chr_id
            iv_test.print_interval()


print('')
for i in chr_iv:
    print i
    chr_iv[i].print_intervalset()
