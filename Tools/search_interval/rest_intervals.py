#!/usr/bin/python
__author__ = 'Thomas'

import sys

from Python.Tools.plink_parser.Fuse_intervals import Interval

fl = sys.argv[1]
chr_itv = {}
for i in xrange(1, 13):
    chr_id = 'chr{0:02}'.format(i)
    chr_itv[chr_id] = []
    for j in xrange(0, 870):
        temp = Interval(50000*j+1, 50000*(j+1))
        chr_itv[chr_id].append(temp)

with open(fl, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split('-')
        temp_chrid = elements[1][3:]
        temp_start = int(elements[2])
        temp_end = int(elements[3])
        temp_itv = Interval(temp_start, temp_end)
        if temp_itv in chr_itv[temp_chrid]:
            chr_itv[temp_chrid].remove(temp_itv)

for chr_id in chr_itv:
    print chr_id
    for itv in chr_itv[chr_id]:
        itv.print_interval()
