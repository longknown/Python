#!/usr/bin/python
''' Usage: This script is written to read in miRNA name list and .gff3 file, to grasp the coordination of
    each miRNAs;
'''
import sys

name_file = sys.argv[1]  # name_file stores the list of query miRNA names
gff_file = sys.argv[2]  # gff_file stores the information of coordinations of precursor or mature miRNAs

# Making a dict for gff_file
f2 = file(gff_file)
gff_dict = {}  # to store coordination info as dict
while True:
    line = f2.readline()
    if len(line) == 0:
        break
    line.rstrip('\n')
    columns = line.split()
    name_column = columns[8].split(';')
    key_name = name_column[2].split('=')
    keyname = key_name[1]
    gff_dict[keyname] = [columns[0], columns[3:5], columns[6]]  # Values are Chr#, interval(start & end), (+/-)
f2.close()

# Searching coordination and print out
f1 = file(name_file)
while True:
    line = f1.readline()
    if len(line) == 0:
        break
    miRNA_name = line.rstrip('\n')
    if miRNA_name in gff_dict:
        coord = gff_dict[miRNA_name]
        print miRNA_name + '\t' + coord[2] + '\t' + coord[0] + '\t' + coord[1][0] + '\t' + coord[1][1]
    else:
        print 'Sorry, but %s is not found!!!' % miRNA_name
f1.close()
