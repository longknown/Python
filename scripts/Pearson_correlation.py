#!/usr/bin/python
import sys
from scipy.stats.stats import pearsonr

__author__ = 'Thomas'
param_len = len(sys.argv)

mirexp_file = sys.argv[param_len-3]
target_file = sys.argv[param_len-2]
mapping_file = sys.argv[param_len-1]
option = sys.argv[1]

mirna_exp = {}
with open(mirexp_file, 'r') as f1:
    header = f1.readline()
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        mirname = elements[0].split('_')[0]
        exp_data = [float(x) for x in elements[1:]]
        mirna_exp[mirname] = exp_data

target_exp = {}
with open(target_file, 'r') as f2:
    header = f2.readline()
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        target = elements[0]
        exp_data = [float(x) for x in elements[1:]]
        target_exp[target] = exp_data

with open(mapping_file, 'r') as f3:
    for line in f3:
        line = line.rstrip('\n')
        elements = line.split()
        mirna = elements[0]
        target = elements[1]
        if mirna in mirna_exp and target in target_exp:
            value = pearsonr(mirna_exp[mirna], target_exp[target])
            if option == '-f' and value[1] > 0.05:
                    continue
            print mirna, target, value
