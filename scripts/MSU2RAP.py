#!/usr/bin/python
import sys

__author__ = 'Thomas'
'''Function: mutual switch from MSU to RAP and vice versa.
:param RAP-MSU.txt, loci file
:return a corresponding mapping file, maps to the original file line by line
'''

mapping_file = sys.argv[1]
loci_file = sys.argv[2]

write2file = open('switch_genename', 'w')
miss2file = open('miss.txt', 'w')

rap2msu = {}
msu2rap = {}
with open(mapping_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split('\t')
        rap_name = elements[0]
        msu_names = elements[1].split(', ')
        if rap_name not in rap2msu:
            rap2msu[rap_name] = msu_names
        for name in msu_names:
            if name not in msu2rap:
                msu2rap[name] = rap_name

with open(loci_file, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        if line[:3] == 'LOC':
            if line not in msu2rap:
                print 'Gene: %s does not exist in the mapping list!!!' % line
                write2file.write('\n')
                miss2file.write(line+'\n')
                continue
            map_name = msu2rap[line]
            write2file.write(map_name+'\n')
        else:
            if line not in rap2msu:
                print 'Gene: %s does not exist in the mapping list!!!' % line
                write2file.write('\n')
                miss2file.write(line+'\n')
                continue
            map_name = rap2msu[line]
            output_line = ', '.join(map_name)
            write2file.write(output_line+'\n')

write2file.close()
miss2file.close()
