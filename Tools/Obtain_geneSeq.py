#!/usr/bin/python
import sys
from Bio import SeqIO

allseqfile = sys.argv[1]
geneloc_file = sys.argv[2]
geneloc_list = []

with open(geneloc_file, 'r') as genef1:
    for line in genef1:
        geneloc = line.rstrip('\n')
        geneloc_list.append(geneloc)

for seq_record in SeqIO.parse(allseqfile, "fasta"):
    parent_name = seq_record.id.split('.')[0]
    if parent_name in geneloc_list:
        print('>'+seq_record.id)
        print(seq_record.seq)
