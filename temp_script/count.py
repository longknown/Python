#!/usr/bin/python
import sys

fn = sys.argv[1]
f1 = file(fn)
name = {}
while True:
    line = f1.readline()
    if len(line) == 0:
        break
    line = line.rstrip('\n')
    both = line.split()
    if both[1] in name:
        name[both[1]].append(both[0])
    else:
        name[both[1]] = [both[0]]

f1.close()
for i in name:
    print i + '\t' + str(len(name[i]))
    print name[i]
