#!/usr/bin/python
import sys
import re
'''This script aims to interpret the haplotype pattern of miRNA:target interaction into
the altered form of complementarity pattern;
Required information (No header line should be included):
    a) Combined miRNA:target haplotype patterns
    b) Combined haplotype information
    c) The SNP information in both regions (Not necessary)
    d) Binding information
    e) Basic information of miRNA and target binding site coordination'''
__author__ = 'Thomas'

# DNA and RNA Watson-Crick pairing
WC_pairing = {'A': 'U', 'G': 'C', 'C': 'G', 'T': 'A', 'U': 'A'}

patternFile = sys.argv[1]
haplotypeFile = sys.argv[2]
bindingFile = sys.argv[3]
mirnaFile = sys.argv[4]


# base_in_haplotype aims to decide whose SNPs is linked with the current pattern base;
#   return: snp2proceed{} -- key: 'mirna' or 'target'; value: snp id;
def base_in_haplotype(_mirna_snps, _target_snps, _ind):
    snp2proceed = {}
    combined_snps = _mirna_snps + _target_snps
    sorted_combined_snps = sorted(list(set(combined_snps)))
    _snp = sorted_combined_snps[_ind]
    if _snp in _mirna_snps:
        snp2proceed['mirna'] = _snp
    if _snp in _target_snps:
        snp2proceed['target'] = _snp
    return snp2proceed


##########################################################################
# substitute a base in the fragment at a time with the SNP provided
# Notice: there may be '-' (INDEL) in the pattern, careful handling should be granted.
def tune_pos(_pos, frag):
    temp_pos = 0
    ind = 0
    for ind, base in enumerate(frag):
        if temp_pos == _pos:
            break
        if base == '-':
            continue
        temp_pos += 1
    return ind


def substitute_mirna_fragment(frag, _ori, _start, _end, _snp, _base):
    snp_position = int(_snp[3:])  # extract SNP position from the SNP id
    if _base == 'T':
        _base = 'U'
    if _ori == '+':
        pos = snp_position - _start
    else:
        pos = _end - snp_position
        _base = WC_pairing[_base]
    pos = tune_pos(pos, frag)  # to calibrate the relative pos when '-' appears in the fragment;
    new_frag = frag[:pos]+_base+frag[pos+1:]
    return new_frag


##########################################################################
# The following functions are for target fragment substitution;
# Here, we use regex to retrieve the info
def target_coord_parsing(_coord):
    p1 = re.compile(r'\[(?P<start>\d+), (?P<end>\d+)\]')
    coord_list = []  # store the coordination of the target fragment
    for match in p1.finditer(_coord):
        temp_start = int(match.group('start'))
        temp_end = int(match.group('end'))
        coord_list.append([temp_start, temp_end])
    return coord_list


def substitute_target_fragment(frag, _ori, _coord, _snp, _base):
    snp_pos = int(_snp[3:])
    target_coord_list = target_coord_parsing(_coord)
    pos = 0
    if _base == 'T':
        _base = 'U'
    if _ori == '+':
        # when the binding site comprises of more than 1 fragment, additional handling shall be granted.
        for coord in target_coord_list:
            if snp_pos <= coord[1]:
                pos += snp_pos - coord[0]
            else:
                pos += coord[1] - coord[0] + 1
    else:
        _base = WC_pairing[_base]
        for coord in reversed(target_coord_list):
            if snp_pos >= coord[0]:
                pos += coord[1] - snp_pos
            else:
                pos += coord[1] - coord[0] + 1
    pos = tune_pos(pos, frag)
    new_frag = frag[:pos]+_base+frag[pos+1:]
    return new_frag


##########################################################################
# interpret_haplotype is the chief function;
# Here _target_coord is the original format from the excel table, like '[a, b]' or '[a, b], [c, d]'; so proper
# parsing is required.
def interpret_haplotype(_old_mirna_fragment, _old_target_fragment, _ref_pattern, _hap_pattern, _mirna_ori, _target_ori,
                        _mirna_start, _mirna_end, _target_coord, mirna_snps, target_snps):
    new_mirna_fragment = _old_mirna_fragment
    new_target_fragment = _old_target_fragment
    for ind, base in enumerate(_hap_pattern):
        base = base.upper()  # avoid lower-capped letter
        ref_base = _ref_pattern[ind]
        if base == ref_base or base == 'N':
            continue
        snp2proceed = base_in_haplotype(mirna_snps, target_snps, ind)
        for option in snp2proceed:
            temp_snp = snp2proceed[option]
            if option == 'mirna':
                new_mirna_fragment = substitute_mirna_fragment(new_mirna_fragment, _mirna_ori, _mirna_start, _mirna_end,
                                                               temp_snp, base)
            if option == 'target':
                new_target_fragment = substitute_target_fragment(new_target_fragment, _target_ori, _target_coord,
                                                                 temp_snp, base)
    return new_mirna_fragment, new_target_fragment

##########################################################################
# Here begins the main function
haplodict = {}  # key: miRNA::target; value: [[SNPs in mature miRNA], [SNPs in target binding site]]
with open(haplotypeFile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        temp_mirna = elements[0]
        temp_target = elements[1]
        snpInMirna = elements[2]
        snpInTarget = elements[3]
        concatName = '::'.join([temp_mirna, temp_target])  # concatenate miRNA name and target name
        if concatName in haplodict:
            continue
        if snpInMirna == '':  # if snpInMirna == '', then a NULL SNP '' would be inserted causing lots of trouble
            snpListMirna = []
        else:
            snpListMirna = snpInMirna.split(', ')
        if snpInTarget == '':
            snpListTarget = []
        else:
            snpListTarget = snpInTarget.split(', ')
        haplodict[concatName] = [snpListMirna, snpListTarget]

# store the binding information into a dict
bindingFrag = {}  # key:concatenate name; value: [miRNA fragment, target fragment]
targetRegion = {}  # key: concatenate name; value: [ori, binding region of target (not split yet)]
with open(bindingFile, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split('\t')
        name = elements[0]
        ori = elements[8]
        mirnaFragment = elements[11]
        targetFragment = elements[12]
        bindingRegionTarget = elements[15]

        bindingFrag[name] = [mirnaFragment, targetFragment]
        targetRegion[name] = [ori, bindingRegionTarget]

# store the genomic info of mature miRNAs, including strand orientation and coordination
mirnaRegion = {}  # key: mature miRNA name; value: [ori, start(int), end(int)]
with open(mirnaFile, 'r') as f3:
    for line in f3:
        line = line.rstrip('\n')
        elements = line.split('\t')
        name = elements[0]
        ori = elements[2]
        start = int(elements[4])
        end = int(elements[5])
        if name in mirnaRegion:
            continue
        mirnaRegion[name] = [ori, start, end]


# Start the main procedure, to interpret the haplotype pattern into complementarity pattern
with open(patternFile, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split('\t')
        mirnaName = elements[0]
        targetName = elements[1]
        refPattern = elements[2]
        hapPattern = elements[3]
        concatName = mirnaName + '::' + targetName
        if concatName not in bindingFrag:
            print '%s is NOT found in our prediction list! Check and retry.' % concatName
            continue
        (oldMirnaFragment, oldTargetFragment) = bindingFrag[concatName]
        if concatName not in haplodict:
            print '%s is NOT found in our haplotype list! Check and retry.' % concatName
            continue
        (mirnaSNPs, targetSNPs) = haplodict[concatName]
        (targetOri, targetCoord) = targetRegion[concatName]
        (mirnaOri, mirnaStart, mirnaEnd) = mirnaRegion[mirnaName]

        (alteredMirnaFragment, alteredTargetFragment) = \
            interpret_haplotype(oldMirnaFragment, oldTargetFragment, refPattern, hapPattern, mirnaOri, targetOri,
                                mirnaStart, mirnaEnd, targetCoord, mirnaSNPs, targetSNPs)
        print '%s\t%s\t%s' % (concatName, alteredMirnaFragment, alteredTargetFragment)
