#!/usr/bin/python
import sys
from complementaryMOD import *
'''Script Description:
    Compare the complementarity pattern of a haplotype with that of reference pattern;
    Return: i) complementarity pattern figures of both patterns; ii) comments on the comparison.'''

__author__ = 'Thomas'

ref_file = sys.argv[1]
hap_file = sys.argv[2]

# Read from reference files and store the complementarity patterns into a dict
ref_dict = {}  # key: miRNA::target; value: Complementarity
with open(ref_file, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        concate_name = elements[0]
        mirna_name = elements[1]
        target_name = elements[2]
        mirna_seq = elements[7]
        target_seq = elements[8]
        temp_cpt = Complementarity(mirna_name, mirna_seq, target_name, target_seq)
        ref_dict[concate_name] = temp_cpt

# Read from the haplotype pattern file and perform the comparison;
sep_line = '*' * 80 + '\n'
output = ''
with open(hap_file, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split('\t')
        mirna_name = elements[0]
        target_name = elements[1]
        ref_pattern = elements[2]
        hap_pattern = elements[3]
        mirna_frag = elements[5]
        target_frag = elements[6]
        concate_name = mirna_name+'::'+target_name
        if concate_name not in ref_dict:
            print 'Interaction pair %s UNAVAILABLE!!!' % concate_name
            print sep_line
            continue
        ref_cpt = ref_dict[concate_name]
        temp_cpt = Complementarity(mirna_name, mirna_frag, target_name, target_frag)
        ref_pattern_form = show_complementarity(ref_cpt)
        hap_pattern_form = show_complementarity(temp_cpt)
        comment = pattern_comparison(ref_cpt, temp_cpt)
        # if comment is not '':
        if 'LOC_Os06g39330' in target_name and 'osa-miR818d' in mirna_name and 'Pos5: Paired to Mismatch' in comment:
            output += concate_name + '\tRef_pattern: ' + ref_pattern + '\tHap_pattern: ' + hap_pattern + '\n' \
                + 'Visualized Reference Pattern:\n' + ref_pattern_form + '\n' \
                + 'Visualized Haplotype Pattern:\n' + hap_pattern_form + '\n' \
                + comment + '\n' + sep_line
print output
