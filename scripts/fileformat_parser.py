#!/usr/bin/python
__author__ = 'Thomas'
from snp import SNP
import csv


def plink_parse(mapfile, pedfile):
    snp_array = []  # to store SNPs
    with open(mapfile, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            elements = line.split()
            temp_snp = SNP(elements[1], elements[0], int(elements[3]))
            snp_array.append(temp_snp)

    with open(pedfile, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            elements = line.split()
            cultivar = elements[0]
            for i in xrange(3, len(elements)/2):
                bi_alleles = elements[2*i] + elements[2*i+1]
                snp_order = i - 3
                if bi_alleles != '00':  # '00' means miss-calling
                    snp_array[snp_order].snp_cul[cultivar] = bi_alleles
    return snp_array


def tab_parse(tabfile, chr_id):
    snp_array = []
    with open(tabfile, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fieldnames = reader.fieldnames

        pos_list = fieldnames[4:]
        for pos in pos_list:
            position = int(pos)
            snp_id = '1'+chr_id[-2:]+'{0:08}'.format(position)
            temp_snp = SNP(snp_id, chr_id, position)
            snp_array.append(temp_snp)
        for row in reader:
            jna = row['JAPONICA NIPPONBARE POSITIONS']
            iris_id = row['IRIS ID']
            if jna == 'JAPONICA NIPPONBARE ALLELES':  # the ref allele line
                for index, pos in enumerate(pos_list):
                    ref_allele = row[pos]
                    snp_array[index].ref_allele = ref_allele
            else:
                cul_name = iris_id.replace(' ', '_')  # IRIS xxx-xxxxx => IRIS_xx-xxxx
                for index, pos in enumerate(pos_list):
                    value = row[pos]
                    if value != '':
                        if len(value) == 1:
                            bi_alleles = value * 2
                        elif len(value) == 3:
                            bi_alleles = value.replace('/', '')
                        snp_array[index].snp_cul[cul_name] = bi_alleles
    return snp_array


def test():
    path = '/Users/Thomas/Downloads/snp3kvars-chrchr12-14900001-14950000.txt'
    snp_array = tab_parse(path, 'chr12')
    snp = snp_array[4]
    print snp.id, snp.snp_seq()


if __name__ == '__main__':
    test()




