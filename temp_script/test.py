__author__ = 'Thomas'

#!/usr/bin/python
import sys

fn = sys.argv[1]
li = {}  # dict, key: line head; value: list
with open(fn, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        number_li = [float(i) for i in elements[1:]]
        li[elements[0]] = number_li

print li
