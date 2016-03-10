#!/usr/bin/python
import sys

from Fuse_intervals import Interval, IntervalSet

__author__ = 'Thomas'
downloaded = sys.argv[1]
all = sys.argv[2]

download_dict = {}  # stores the intervals of the downloaded files
with open(downloaded, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('-')
        chrid = elements[0]
        start = int(elements[1])
        end = int(elements[2])
        temp = Interval(start, end)
        if chrid not in download_dict:
            download_dict[chrid] = IntervalSet()
        download_dict[chrid].insert(temp)

with open(all, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        chrid = elements[0]
        for i in xrange(1, len(elements), 2):
            start = int(elements[i])
            end = int(elements[i+1])
            test_interval = Interval(start, end)
            if test_interval not in download_dict[chrid]:
                print_start = (test_interval.start / 5000) * 5000 + 1
                print_end = (test_interval.end / 5000 + 1) * 5000
                print chrid, print_start, print_end
