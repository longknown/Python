#!/usr/bin/python
import sys

__author__ = 'Thomas'
'''
:param gene lists, RAP-MSU.txt, annotation.csv, expression file;
:return an extracted expression file of the input genes;
'''

gene_list_file = sys.argv[1]
mapping_file = sys.argv[2]
annotation_file = sys.argv[3]
exp_file = sys.argv[4]

extract_f = open('extracted_exp.txt', 'w')
miss_f = open('missGene.txt', 'w')

msu2rap = {}
with open(mapping_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split('\t')
        rap_name = elements[0]
        msu_names = elements[1].split(', ')
        for name in msu_names:
            if name not in msu2rap:
                msu2rap[name] = rap_name

map2id = {}
with open(annotation_file, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        if len(elements) <= 3:
            continue
        _id = elements[0]
        orf = elements[2]
        gene_name = orf.split('|')[0]
        if gene_name not in map2id:
            map2id[gene_name] = _id

gene_list = {}
with open(gene_list_file, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        if line in gene_list:
            continue
        if line not in msu2rap:
            print 'Gene: %s map to RAP failed!' % line
            miss_f.write(line+'\n')
            continue
        rap_name = msu2rap[line]
        if rap_name not in map2id:
            print 'Gene: %s map to probeID failed!' % line
            miss_f.write(line+'\n')
            continue
        probeID = map2id[rap_name]
        gene_list[probeID] = line

with open(exp_file, 'r') as f3:
    line = f3.readline()
    extract_f.write(line)
    for line in f3:
        line = line.rstrip('\n')
        elements = line.split('\t')
        _id = elements[0]
        if _id not in gene_list:
            continue
        elements[0] = gene_list[_id]
        output_line = '\t'.join(elements)
        extract_f.write(output_line+'\n')

extract_f.close()
miss_f.close()
