#!/usr/bin/python
import sys
from Bio import SeqIO

__author__ = 'Thomas'

allchrfile = sys.argv[1]
tablefile = sys.argv[2]

wastson_mapping = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

genome_seq = {}
for record in SeqIO.parse(allchrfile, 'fasta'):
    genome_seq[record.id] = str(record.seq)

with open(tablefile, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        chrid = elements[0]
        ori = elements[1]
        frag_seq = elements[2]
        if ori == '-':
            temp_seq = ''
            for i in frag_seq[::-1]:
                temp_seq += wastson_mapping[i]
        else:
            temp_seq = frag_seq

        pos = genome_seq[chrid].find(temp_seq)
        count = genome_seq[chrid].count(temp_seq)
        print pos, count
