#!/usr/bin/python

import sys

maturefile = sys.argv[1]
snpfile = sys.argv[2]

f1 = file(maturefile, 'r')
f2 = file(snpfile, 'r')

mature_coord = {}
while True:
    line = f1.readline()
    if len(line) == 0:
        break
    elements1 = line.rstrip('\n').split()
    if not mature_coord.has_key(elements1[0]):
        mature_coord[elements1[0]] = [[elements1[1], int(elements1[4]), int(elements1[5])]]
    else:
        mature_coord[elements1[0]].append([elements1[1], int(elements1[4]), int(elements1[5])])
f1.close()
while True:
    line2 = f2.readline()
    if len(line2) == 0:
        break
    elements2 = line2.rstrip('\n').split()
    position = int(elements2[3])
    miRNA = elements2[0]
    for i in mature_coord[miRNA]:
        if position >= i[1] and position <= i[2]:
            print line2.rstrip('\n')+'\tYES'
            print i
            break
f2.close()