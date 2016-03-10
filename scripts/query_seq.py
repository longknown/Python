#!/usr/bin/python
import sys
from Bio import SeqIO

__author__ = 'Thomas'

cdnafile = sys.argv[1]
listfile = sys.argv[2]

records = {}
for record in SeqIO.parse(cdnafile, 'fasta'):
    records[record.id] = str(record.seq)

with open(listfile, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        name = elements[0]
        start = int(elements[1])
        end = int(elements[2])
        if name in records:
            print records[name][start-1:end].replace('U', 'T')
