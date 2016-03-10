#!/usr/bin/python
import sys

fn = sys.argv[1]
f1 = file(fn)

while True:
    line = f1.readline()
    if len(line) == 0:
        break
    line = line.rstrip('\n')

    if line[0:3] == 'osa':
        flag = line
    else:
        p_out = flag + '\t' + line
        print p_out
