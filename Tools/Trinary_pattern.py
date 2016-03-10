#!/usr/bin/python
''' Usage: This script aims to obtain the "Trinary pattern" of a haplotype;
    Trinary pattern: for each marker(SNP), if it's the same as the Ref allele, then it will be assigned as 0, Non-ref as 1,
        N as 2, such as Ref_pattern = 'ATCG', haplotype = 'GCCN', trinary pattern = '1102';
    Input file format: First column is reference pattern, second column is haplotype;
    Print out: the trinary pattern in order.
'''
import sys

fn = sys.argv[1]
f1 = file(fn)

while True:
    line = f1.readline()
    if len(line) == 0:
        break

    line = line.rstrip('\n')
    columns = line.split()
    trinary = ''
    for i in range(0, len(columns[0])):
        if columns[1][i] == 'N':
            trinary += '2'
        elif columns[1][i] == columns[0][i]:
            trinary += '0'
        else:
            trinary += '1'
    print trinary
f1.close()
