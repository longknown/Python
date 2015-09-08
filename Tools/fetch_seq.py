#!/usr/bin/python
import sys
from Bio import SeqIO

fastafile = sys.argv[1]
coorfile = sys.argv[2]

def fetch_seq(fastafile, seqname, start, end):
    for seq_record in SeqIO.parse(fastafile, 'fasta'):
        if seq_record.id == seqname:
            seq_fetch = seq_record.seq[start:end]
            print(seqname+'\t'+seq_fetch)
            break

f1 = file(coorfile)
while True:
    line = f1.readline()
    if len(line) == 0:
        break
    line = line.rstrip('\n')
    elements = line.split()
    seqname = elements[0]
    start = int(elements[1])-1
    end = int(elements[2])
    fetch_seq(fastafile, seqname, start, end)

f1.close()
