#!/usr/bin/python

import sys
import re

fname = sys.argv[1]
fa_len = int(sys.argv[2])

f = file(fname)

# to modify the length of each line of .fasta file to specified length.
while True:
    line = str(f.readlines())
    if len(line) == 0:
        break
    line_strip = line.strip('\n')

