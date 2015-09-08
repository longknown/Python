#!/usr/bin/python

import sys
import os
filename = sys.argv[1]

f = file(filename)
while True:
    line = f.readline()
    if len(line) == 0:
        break

    line = line.rstrip('\n')
    elements = line.split()
    sign = elements[0]
    seq = elements[1]

    if sign == '+':
        dna_seq = os.popen("echo "+seq+" | tr 'T' 'U'").read().rstrip('\n')
    elif sign == '-':
        dna_seq = os.popen("echo "+seq+" | tr 'ATGC' 'UACG' | rev").read().rstrip('\n')

    print sign + '\t' + dna_seq;
