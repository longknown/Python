#!/usr/bin/python
''' Usage: for each miRNA precursor, and every haplotype, this script aims to get the mutated RNA seq
    :param 1) precursor strand +/-, 2) chromosome ID, 3) start & end position, 4) haplotype pattern,
      5) SNPs order and their position, 6) SNP alleles;
    :argument a) miRNA info including haplotype, b) SNP info, c) SNP order in each miRNA precursor;
    :return a table containing miRNA name, haplotype, original RNA seq, mutated RNA seq
'''
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


def Mutate_seq(miRname, pattern, miRNA, snp, mi_snp):
    '''
    :param miRname: Specify miRNA name
    :param pattern: In fact this is the trinary pattern (0-Ref_allele, 1-nonRef_allele, 2-N)
    :param miRNA: miRNA{} stores the basic information of a miRNA: seq, strand, chr_id, start, end
    :param snp: snp{} stores the basic info of a SNP: chr_id, position, ref_allele, nonRef_allele
    :param mi_snp: mi_snp{} stores the SNP within a miRNA precursor in order
    :return: original RNA seq & a mutated sequence according to the trinary pattern
    '''
    orig_seq = miRNA[miRname][0]
    strand = miRNA[miRname][1]
    miRstart = miRNA[miRname][3]
    miRend = miRNA[miRname][4]
    mutated_seq_temp = orig_seq
    for i in range(0, len(pattern)):
        snp_name = mi_snp[miRname][i]
        snp_position = snp[snp_name][1]
        trinary_element = pattern[i]
        if trinary_element == '0':
            continue
        elif trinary_element == '1':
            allele = snp[snp_name][3]
        else:  # trinary_element == '2'
            allele = 'N'
        mutated_seq_temp = SingleMutate(mutated_seq_temp, strand, miRstart, miRend, snp_position, allele)
    return orig_seq, mutated_seq_temp


# miRinfo file columns are: "precursor, sequence, strand +/-, chr_id, start, end"
miRinfo_file = sys.argv[1]
# hap_tab file columns are: "precursor, trinary pattern"
hap_tab = sys.argv[2]
# snp_info file columns are: "SNP ID, chr_id, position, Ref_allele, NonRef_allele"
snp_info_file = sys.argv[3]
# snp_order file: "miRNA: SNP1, SNP2, SNP3..."
snp_order = sys.argv[4]

miRNA = {}  # to store basic miRNA info
snp = {}  # to store basic snp info
mi_snp = {}  # to store SNPs within a miRNA in order

# Read in the miRinfo_file to store all the miRNA info into miRNA{}
f1 = file(miRinfo_file)
while True:
    line = f1.readline()
    if len(line) == 0:
        break
    line = line.rstrip('\n')
    elements = line.split()
    name = elements[0]
    seq = elements[1]
    strand = elements[2]
    chr_id = elements[3]
    start = elements[4]
    end = elements[5]
    if name not in miRNA:
        miRNA[name] = [seq, strand, chr_id, start, end]
f1.close()

# Read in the snp_info_file to store snp info into snp{}
f2 = file(snp_info_file)
while True:
    line = f2.readline()
    if len(line) == 0:
        break
    line = line.rstrip('\n')
    elements = line.split()
    snp_name = elements[0]
    chr_id = elements[1]
    position = elements[2]
    ref_allele = elements[3]
    nonRef_allele = elements[4]
    if snp_name not in snp:
        snp[snp_name] = [chr_id, position, ref_allele, nonRef_allele]
f2.close()

# miRNA-SNP order
with open(snp_order, mode='r') as f3:
    for line in f3:
        line = line.rstrip('\n')
        elements = line.split()
        name = elements[0]
        if name not in mi_snp:
            mi_snp[name] = elements[1:]

# obtain the mutated RNA seq
with open(hap_tab, mode='r') as f4:
    for line in f4:
        line = line.rstrip('\n')
        elements = line.split()
        miRname = elements[0]
        pattern = elements[1]
        (orig_seq, mutated_seq) = Mutate_seq(miRname, pattern, miRNA, snp, mi_snp)
        print miRname + '\t' + pattern + '\t' + orig_seq + '\t' + mutated_seq
