#!/usr/bin/python
__author__ = 'Thomas'

import sys

from Tools.search_interval.Fuse_intervals import Interval, IntervalSet

chr_interval = {}  # key: chromosome id; value: intervals of genome coordination
ifile = sys.argv[1]
with open(ifile, 'r') as f:  # ifile format: chr_id start end
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        chr_id = elements[0]
        start = int(elements[1])
        end = int(elements[2])
        interval = Interval(start, end)
        if chr_id not in chr_interval:
            iset = IntervalSet()
            iset.insert(interval)
            chr_interval[chr_id] = iset
        else:
            chr_interval[chr_id].insert(interval)

for chr_id in chr_interval:
    print chr_id, chr_interval[chr_id].number
    chr_interval[chr_id].print_intervalset()
cover_dict = {}
for chr_id in chr_interval:
    cover_dict[chr_id] = IntervalSet(chr_interval[chr_id])
    pos = 0
    while True:
        if pos == cover_dict[chr_id].number:
            break
        ins_start = cover_dict[chr_id][pos].start / 50000
        ins_item = Interval(ins_start*50000+1, (ins_start+1)*50000)
        cover_dict[chr_id].insert(ins_item)
        pos += 1


print()
for chr_id in cover_dict:
    print chr_id, cover_dict[chr_id].number
    cover_dict[chr_id].print_intervalset()
