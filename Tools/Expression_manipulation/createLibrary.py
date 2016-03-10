#!/usr/bin/python
import sys
import matlab.engine
__author__ = 'thomas'

eng = matlab.engine.start_matlab()
output = open('fail.log', 'w')

geneFile = sys.argv[1]
mirnaFile = sys.argv[2]
pairFile = sys.argv[3]

gene_list = []
with open(geneFile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        gene_list.append(line)

mirna_list = []
with open(mirnaFile, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        mirna_list.append(line)

# Create a sparse matrix with MatLab API
M = len(gene_list)
N = len(mirna_list)
eng.eval('mat = sparse(%s, %s);' % (M, N), nargout=0)
num = 0

with open(pairFile, 'r') as f3:
    for line in f3:
        line = line.rstrip('\n')
        pair = line.split()
        mirna = pair[0]
        gene = pair[1]
        flag = 0
        for ind, x in enumerate(gene_list):
            if x in gene:
                m = ind + 1
                flag = 1
                break
        if not flag:
            output.write('Interaction pair (%s, %s), gene(%s) failed mapping!\n' % (mirna, gene, gene))
            continue

        flag = 0
        for ind, x in enumerate(mirna_list):
            if x in mirna:
                n = ind + 1
                flag = 1
                break
        if not flag:
            output.write('Interaction pair (%s, %s), mirna(%s) failed mapping!\n' % (mirna, gene, mirna))
            continue
        eng.eval('mat(%s, %s) = 1;' % (m, n), nargout=0)
        num += 1
        print 'Pair(%s, %s) succeeded!!!' % (mirna, gene)

print num
eng.eval('save interaction.mat mat;', nargout=0)
output.close()


