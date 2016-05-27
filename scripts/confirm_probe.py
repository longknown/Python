#!/usr/bin/python
import sys

__author__ = 'Thomas'

probeFILE = sys.argv[1]
matureFILE = sys.argv[2]

mature_seq = {}
with open(matureFILE, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        mirna = elements[0]
        seq = elements[1]
        if mirna[-2:] == '5p':
            temp_mir = mirna[:-3]
            mature_seq[temp_mir] = seq
        elif mirna[-2:] == '3p':
            continue
        else:
            mature_seq[mirna] = seq

with open(probeFILE, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        mirna = elements[1]
        seq = elements[3]
        if mirna not in mature_seq:
            print '%s: does not appear in current list!' % mirna
            continue
        else:
            mature = mature_seq[mirna].replace('U', 'T')
            count = seq.count(mature)
            rest = seq.replace(mature, '')
            print '%s: Mature Occurrence %s, mature sequence: %s; rest fragment: %s, rest in mature: %s' % (mirna, count, mature, rest, rest in mature)
