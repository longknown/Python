#!/usr/bin/python
import sys

fn = sys.argv[1]
with open(fn, 'r') as f1:
    for line in f1:
        columns = line.split()
        geneid = columns[8]
        geneid = geneid[3:16]
        print(geneid+'\t'+columns[6]+'\t'+columns[0]+'\t'+columns[3]+'\t'+columns[4])
