#!/usr/bin/python
import sys
from Bio import SeqIO

__author__ = 'Thomas'

loci_file = sys.argv[1]
seq_file = sys.argv[2]

loci_list = []
with open(loci_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        loci_list.append(line)


for record in SeqIO.parse(seq_file, 'fasta'):
    if record.id in loci_list:
        print '> %s' % record.id
        print record.seq
