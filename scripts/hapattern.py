#!/usr/bin/python
import MySQLdb as mdb
'''
This module is a sub-function to grasp the haplotype and corresponding cultivar data from the local machine.
It will be called in the main.py, and finally produce a file containing the haplotype pattern and cultivar set.
'''

__author__ = 'thomas'


def pattern_n(_bi_allele, _alleles):  # the minor allele of the _bi_allele would be remained and lower case be returned
    if _bi_allele == '00':
        return 'N'
    elif _bi_allele[0] == _bi_allele[1]:
        return _bi_allele[0]
    else:
        if _alleles.index(_bi_allele[0]) < _alleles.index(_bi_allele[1]):
            return _bi_allele[1].lower()
        else:
            return _bi_allele[0].lower()


def pentanary(haplotype, _snp_info, _snp_list, _ref_alleles):
    penta = ''
    # Convert all the alleles in haplotype to upper-case
    haplotype = haplotype.upper()

    for ind, temp_allele in enumerate(haplotype):
        _snp = _snp_list[ind]
        _alleles = _snp_info[_snp]
        _ref_allele = _ref_alleles[ind]
        if temp_allele == 'N':
            penta += '4'
        else:
            cut_alleles = [i for i in _alleles if i is not _ref_allele]
            if temp_allele == _ref_allele:
                penta += '0'
            else:
                penta += str(cut_alleles.index(temp_allele)+1)
    return penta


def merge_snp(hap_list):  # it combines all the SNPs of the hap_list
    all_snp = []
    for temp_hap in hap_list:
        all_snp += temp_hap.hap_mirna + temp_hap.hap_gene
    all_snp = sorted(list(set(all_snp)))
    return all_snp


def _grasp_pattern(hap_list):  # This function takes the list of 'Haplotype' Module as parameter;
    fw = open('hap_pattern', 'w')
    line_list = []  # this list stores the to-be-print lines

    con = mdb.connect(host='localhost', user='root', passwd='piao2551', db='3000osaSNP')
#    cul_set = []
    snp_union = merge_snp(hap_list)

    with con:
        cur = con.cursor()
# Here, we ignore the process of obtaining the cultivars from the database, just store the index of the corresponding
        # cultivars#######
#        cul_sql = 'SELECT * FROM cultivar_accession ORDER BY acc_id ASC;'
#        cur.execute(cul_sql)
#        for row in cur.fetchall():
#            cul_set.append(row[0])

        # obtain the SNP alleles
        snp_info = {}  # to store the alleles of SNPs
        ref_alleles = {}  # to store the reference alleles, key:snp; value:ref_allele
        seqs = {}  # to store the snp sequence against all cultivars, key:snp, value:seq;
        sql1 = 'SELECT allele_1, allele_2, allele_3, allele_4, ref_allele FROM SNP WHERE id IN (%s);' % \
               ', '.join(snp_union)
        cur.execute(sql1)
        for index, row in enumerate(cur.fetchall()):
            snp_id = snp_union[index]
            snp_info[snp_id] = []
            ref_alleles[snp_id] = row[-1]
            for allele in row[:-1]:
                if allele is not None:
                    snp_info[snp_id].append(allele)

        sql2 = 'SELECT snp_seq FROM SNP_cultivar WHERE snp_id IN (%s);' % ', '.join(snp_union)
        cur.execute(sql2)
        for index, row in enumerate(cur.fetchall()):
            snp_id = snp_union[index]
            seqs[snp_id] = row[0]

    # the following part is to search the haplotype patterns
    for hap in hap_list:
        pattern_cultivar = {}  # key: pattern; value: cultivar set.
        snp_subset = hap.hap_mirna + hap.hap_gene
        snp_subset = sorted(list(set(snp_subset)))  # to obtain the union of snp sets, merge, unique, sort

        for index in xrange(0, 3024):
            pattern = ''
            for snp_id in snp_subset:  # seqs[] is in the order of snp_union (in ASCENDING order)
                bi_allele = seqs[snp_id][index*2:index*2+2]
                base = pattern_n(bi_allele, snp_info[snp_id])
                pattern += base
            if pattern not in pattern_cultivar:
                pattern_cultivar[pattern] = [str(index+1)]
            else:
                pattern_cultivar[pattern].append(str(index+1))

        # print out the results
        ref_alleles_subset = [ref_alleles[snp_id] for snp_id in snp_subset]
        ref_pattern = ''.join(ref_alleles_subset)
        for pattern in pattern_cultivar:
            penta_pattern = pentanary(pattern, snp_info, snp_subset, ref_alleles_subset)
            culs = ', '.join(pattern_cultivar[pattern])
            temp_line = '\t'.join([hap.mirna, hap.gene, ref_pattern, pattern, penta_pattern, culs])
            line_list.append(temp_line)
    fw.write('\n'.join(line_list))
    fw.close()
