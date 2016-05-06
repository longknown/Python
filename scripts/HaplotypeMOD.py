#!/usr/bin/python
'''Modules to describe the combined haplotype pattern'''

__author__ = 'Thomas'


class Haplotype:
    def __init__(self, _mirna, _gene, _hap_mirna, _hap_gene):
        '''
        :param _hap_mirna: a list of SNPs falling into miRNAs, in ascending order;
        :param _hap_gene: a list of SNPs falling into genes, in ascending order;
        '''
        self.mirna = _mirna
        self.gene = _gene
        self.hap_mirna = _hap_mirna
        self.hap_gene = _hap_gene
