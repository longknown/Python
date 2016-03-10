#!/usr/bin/python
import sys
from complementaryMOD import *
from HaplotypeMOD import *

__author__ = 'Thomas'

mirnaFILE = sys.argv[1]  # table columns: mirna, snp;
geneFILE = sys.argv[2]  # table columns: gene, snp;
interactionFILE = sys.argv[3]  # table columns: mirna::gene;

mir_hap_dict = {}  # key: mirna; value: SNP list;
with open(mirnaFILE, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        mirna = elements[0]
        snp = elements[1]
        if mirna not in mir_hap_dict:
            mir_hap_dict[mirna] = []
        if snp in mir_hap_dict[mirna]:
            continue
        mir_hap_dict[mirna].append(snp)  # Notice: SNPs here are not sorted!!!
for mir in mir_hap_dict:
    mir_hap_dict[mir].sort()  # to guarantee the ascending order of the SNP list;

gene_hap_dict = {}  # key: gene; value: SNP list
with open(geneFILE, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        gene = elements[0]
        snp = elements[1]
        if gene not in gene_hap_dict:
            gene_hap_dict[gene] = []
        if snp in gene_hap_dict[gene]:
            continue
        gene_hap_dict[gene].append(snp)
for gene in gene_hap_dict:
    gene_hap_dict[gene].sort()

hap_list = []  # list of class Haplotype;
with open(interactionFILE, 'r') as f3:
    for line in f3:
        line = line.rstrip('\n')
        elements = line.split('::')
        mirna = elements[0]
        gene = elements[1]
        if mirna not in mir_hap_dict and gene not in gene_hap_dict:
            continue
        if mirna not in mir_hap_dict:
            mirna_hap = []
        else:
            mirna_hap = mir_hap_dict[mirna]
        if gene not in gene_hap_dict:
            gene_hap = []
        else:
            gene_hap = gene_hap_dict[gene]
        temp_hap = Haplotype(mirna, gene, mirna_hap, gene_hap)
        hap_list.append(temp_hap)

for temp in hap_list:
    print temp.mirna, temp.gene, temp.hap_mirna, temp.hap_gene
print len(hap_list)


