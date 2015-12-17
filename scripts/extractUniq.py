#!/usr/bin/python
import sys

__author__ = 'Thomas'


class Target:
    def __init__(self, genename, start, end, chrid, ori):
        self.name = genename
        self.start = start
        self.end = end
        self.chr = chrid
        self.ori = ori


listfile = sys.argv[1]
blastfile = sys.argv[2]

targetlist = []
with open(listfile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        genename = elements[0]
        start = int(elements[1])
        end = int(elements[2])
        chrid = elements[3]
        ori = elements[4]
        temp = Target(genename, start, end, chrid, ori)
        targetlist.append(temp)

with open(blastfile, 'r') as f2:
    index = 0
    temp_target = targetlist[index]
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        name = elements[0]
        chrid = elements[1]
        start = int(elements[8])
        end = int(elements[9])
        if name != temp_target.name:  # if not consistent with previous target name, then move to next target
            index += 1
            temp_target = targetlist[index]
        if chrid != temp_target.chr:
            continue
        if start >= temp_target.start and end <= temp_target.end:
            print line
        else:
            continue
