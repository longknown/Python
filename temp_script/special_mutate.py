#!/usr/bin/python
import sys

basepair = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N': 'N'}  # DNA base pairing, 'N-N' is added to avoid error
def RNA_base(base):
    if base == 'T':
        return 'U'
    return base

def SingleMutate(seq, strand, miRstart, miRend, snp_position, allele):
    '''
    :param seq: the original RNA sequence
    :param strand: strand forward: +/-
    :param miRstart: miRNA starting position
    :param miRend: miRNA end position
    :param snp_position: SNP position
    :param allele: mutated allele
    :return: a RNA seq with a single SNP mutation
    '''
    if strand == '+':
        rela_pos = int(snp_position) - int(miRstart)
        mutated_base = RNA_base(allele)
    else:  # elif strand == '-'
        rela_pos = int(miRend) - int(snp_position)  # relative to the ending position, because the strand is reversed
        mutated_base = RNA_base(basepair[allele])  # the - strand, means the complementary base to the + strand
    mutated_seq = seq[:rela_pos] + mutated_base + seq[rela_pos+1:]  # mutate just one position
    return  mutated_seq

seq = sys.argv[1]
strand = sys.argv[2]
start = sys.argv[3]
end = sys.argv[4]
position = sys.argv[5]
allele = sys.argv[6]

print SingleMutate(seq, strand, start, end, position, allele)