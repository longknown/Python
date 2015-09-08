#!/usr/bin/python
__author__ = 'Thomas'

REF_GENOME_PATH = '/Users/Thomas/Academy/RiceGenome/msu7.0/BLAST_local_genome/all.chr.con'
from Bio import SeqIO
import sys

def obtain_N(seqrecords, chr_id, pos):
    return seqrecords[chr_id][pos-1]
records = {}
for record in SeqIO.parse(REF_GENOME_PATH, 'fasta'):
    records[record.id] = record.seq

query_f = sys.argv[1]
with open(query_f, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        job = elements[0]
        chr_id = elements[1]
        pos = int(elements[2])
        allele = obtain_N(records, chr_id, pos)
        print allele
