#!/usr/bin/python
'''Module that depicts class complementarity pattern and complementarity alteration;
    "GU" pairs are counted as 0.5 mismatches and INDELs are counted as 1 mismatch;
'''

__author__ = 'Thomas'

rna_dict = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G', '-': '-'}  # add a key '-' in case of ERROR


def mismatch(cpt, *region):  # count the mismatch numbers (indels taken as mismatches)
    if len(region) == 0:
        start = 0
        end = len(cpt.miRNA_seq)-1
    elif len(region) == 2:
        start = region[0]
        end = region[1]
    else:
        print 'Error parameters; default (no region specified): all length search, or pass 2 int!'
        exit()
    num = 0
    for index in xrange(start-1, end):
        if index >= len(cpt.miRNA_seq):
            break
        target_base = cpt.target_seq[-index-1]
        base = cpt.miRNA_seq[index]
        if base == '-' or target_base == '-':
            num += 1
        elif base+target_base == 'GU' or base+target_base == 'UG':
            num += 0.5
        elif rna_dict[base] != target_base:
            num += 1
    return num


def indel(cpt):
    indel_list = []
    for index, base in enumerate(cpt.miRNA_seq):
        target_base = cpt.target_seq[index]
        if base == '-' or target_base == '-':
            indel_list.append(index+1)
    return indel_list


def cpattern(cpt):
    pattern = ''
    for i, base in enumerate(cpt.miRNA_seq):
        invbase = cpt.target_seq[-i-1]
        if invbase == '-' or base == '-':
            pattern += '2'
        elif invbase == rna_dict[base]:
            pattern += '0'
        elif invbase+base == 'GU' or invbase+base == 'UG':
            pattern += '*'
        else:
            pattern += '1'
    return pattern


# Defined to compare the pattern of a mutated haplotype with the reference pattern,
# to extract the effects point mutations cause on the complementarity pattern;
# In fact, just compare, for each site, whether the Watson-Crick pairing changed or NOT;
# Return: a string representing the comment of the comparison
def pattern_comparison(cpt1, cpt2):
    comment = ''
    # Check if the Complementarity patterns belong to the same interaction pairs;
    if not (cpt1.miRNA_name == cpt2.miRNA_name and cpt1.target_name == cpt2.target_name):
        print 'The patterns you passed do not belong to the same interaction pairs! Check and re-pass!'
        return comment
    if len(cpt1.miRNA_seq) != len(cpt2.miRNA_seq):
        print 'Pair %s Failed: ref miRNA seq-%s, hap miRNA seq-%s' % (cpt1.miRNA_name+'::'+cpt1.target_name,
                                                                      cpt1.miRNA_seq, cpt2.miRNA_seq)

    for ind in xrange(0, len(cpt1.miRNA_seq)):
        cpt1_mirna_base = cpt1.miRNA_seq[ind]
        cpt1_target_base = cpt1.target_seq[-ind-1]
        cpt2_mirna_base = cpt2.miRNA_seq[ind]
        cpt2_target_base = cpt2.target_seq[-ind-1]

        flag1 = (cpt1_mirna_base == cpt2_mirna_base)
        flag2 = (cpt1_target_base == cpt2_target_base)

        pair1 = (cpt1_mirna_base == rna_dict[cpt1_target_base])
        pair2 = (cpt2_mirna_base == rna_dict[cpt2_target_base])
        if flag1 and flag2:
            continue
        elif pair1 and (not pair2):
            comment += 'Pos%s: Paired to Mismatch\n' % (ind+1)
        elif (not pair1) and pair2:
            comment += 'Pos%s: Mismatch to Paired\n' % (ind+1)
        elif pair1 and pair2:
            comment += 'Pos%s: Mutated but Still Paired\n' % (ind+1)
        else:
            comment += 'Pos%s: Mutated but Still Mismatch\n' % (ind+1)
    return comment.rstrip('\n')


# This function is defined to get the forms like this:
# AUUGGAAACGGCCAA
# ||**  ||||* |||
# UAGUAAUUGCUCGUU
# For this is more visualized.
def show_complementarity(cpt):
    pairing_str = ''
    for ind, base in enumerate(cpt.miRNA_seq):
        target_base = cpt.target_seq[-ind-1]
        if target_base == rna_dict[base]:
            pairing_str += '|'
        elif base + target_base == 'GU' or base + target_base == 'UG':
            pairing_str += '*'
        else:
            pairing_str += ' '
    pattern_form = cpt.miRNA_seq + '\n' + pairing_str + '\n' + cpt.target_seq[::-1]
    return pattern_form


# Class Complementarity definition
class HandlingException(Exception):
    pass


class Complementarity:
    def __init__(self, _mirna_name, _mirna_seq, _target_name, _target_seq):
        if len(_mirna_seq) != len(_target_seq):
            print 'Provided sequences are not aligned, please input aligned sequences instead!'
            raise HandlingException
        self.miRNA_name = _mirna_name
        self.miRNA_seq = _mirna_seq
        self.target_name = _target_name
        self.target_seq = _target_seq
