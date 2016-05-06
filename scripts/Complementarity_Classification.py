#!/usr/bin/python
import sys
from complementaryMOD import *
'''This script aims to classify the complementarity pattern for each interaction pair with the notation
drafted in our note'''
__author__ = 'Thomas'

inputfile = sys.argv[1]
with open(inputfile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        mir_name = elements[0]
        target_name = elements[1]
        mir_seq = elements[2]
        target_seq = elements[3]
        temp_cpt = Complementarity(mir_name, mir_seq, target_name, target_seq)
        pattern = cpattern(temp_cpt)
        mis_num = mismatch(temp_cpt)
        centralPattern = pattern[8:11]
        region5_num = mismatch(temp_cpt, 2, 8)
        region3_num = mismatch(temp_cpt, 13, 24)
        print '%s\t%s::%s\t%s\t%s\t%s\t%s' % (pattern, mir_name, target_name, mis_num, region5_num, region3_num, centralPattern)
