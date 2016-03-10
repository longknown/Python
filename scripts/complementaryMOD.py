#!/usr/bin/python
'''Module that depicts class complementarity pattern and complementarity alteration;
'''

__author__ = 'Thomas'

rna_dict = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}


class HandlingException(Exception):
    pass


def unpair(cpt):  # browse and return the unpaired position list
    pos_list = []
    for index, base in enumerate(cpt.miRNA_seq):
        target_base = cpt.target_seq[index]
        if base == '-' or target_base == '-':
            continue
        else:
            if rna_dict[base] != target_base:
                pos_list.append(index+1)
    return pos_list


def indel(cpt):
    indel_list = []
    for index, base in enumerate(cpt.miRNA_seq):
        target_base = cpt.target_seq[index]
        if base == '-' or target_base == '-':
            indel_list.append(index+1)
    return indel_list


def notation(cpt):
    pos_list = [1, 10, 11]
    mis_list = []
    indel_list = []
    flag = 0
    for index, base in enumerate(cpt.miRNA_seq):
        target_base = cpt.target_seq[index]
        if base == '-' or target_base == '-':
            indel_list.append(index+1)
        elif rna_dict[base] != target_base:
            mis_list.append(index+1)
    for pos in pos_list:
        if pos in mis_list:
            print 'Pos(%s) is matched;' % pos
            flag = 1
        elif pos in indel_list:
            print 'Pos(%s) is an INDEL;' % pos
            flag = 1
    if flag == 0:
        print 'Pos(1, 10, 11) is perfectly matched! No Special Notation!'


class Complementarity:
    def __init__(self, _mirna_name, _mirna_seq, _target_name, _target_seq):
        if len(_mirna_seq) != len(_target_seq):
            print 'Provided sequences are not aligned, please input aligned sequences instead!'
            raise HandlingException
        self.miRNA_name = _mirna_name
        self.miRNA_seq = _mirna_seq
        self.target_name = _target_name
        self.target_seq = _target_seq
