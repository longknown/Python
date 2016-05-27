#!/usr/bin/python
import sys

from scripts.Fuse_intervals import Interval, IntervalSet

FIX_WIDTH = 5000

__author__ = 'Thomas'
coord_file = sys.argv[1]

chr_coord = {}  # key: chr_id; value: IntervalSet.
with open(coord_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split('\t')
        chr_id = elements[0]
        length = len(elements)
        if chr_id not in chr_coord:
            chr_coord[chr_id] = IntervalSet()
        for i in xrange(1, length, 2):
            start = int(elements[i])
            end = int(elements[i+1])
            fix_start = (start / FIX_WIDTH) * FIX_WIDTH + 1
            fix_end = (end / FIX_WIDTH + 1) * FIX_WIDTH
            fix_interval = Interval(fix_start, fix_end)
            chr_coord[chr_id].insert(fix_interval)

for i in chr_coord:
    print i
    chr_coord[i].print_intervalset()
    print '\n'
