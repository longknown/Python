#!/usr/bin/python
import sys
__author__ = 'thomas'
'''Usage
        Description： This is the 1st step of the haplotype analysis, currently you've got basic info of SNPs at hand;
        :param a file containing miRNA and its SNPs (even NULL values are accepted, although will be eliminated later)
        :returns -m for miRNA haplotype; -h for haplotype pattern
'''

infile = sys.argv[1]

