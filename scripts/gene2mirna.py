#!/usr/bin/python
import sys

__author__ = 'Thomas'

target_dict = {}

for i in xrange(1, len(sys.argv)):
    filename = sys.argv[i]
    with open(filename, 'r') as f:
        header = f.readline().rstrip('\n')
        for gene in f:
            gene = gene.rstrip('\n')
            if gene not in target_dict:
                target_dict[gene] = []
            target_dict[gene].append(header)

for gene in sorted(target_dict.keys()):
    print '*' * 40
    print gene + ':'
    for mirna in sorted(target_dict[gene]):
        print mirna
print '*' * 40
