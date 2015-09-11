#!/usr/bin/python
__author__ = 'thomas'
import sys
import MySQLdb as mdb
THRESHOLD = 10  # global definition of the number of cultivars corresponding to each pattern
'''Usage
    :param This scripts requires the miRNA haplotype as input
    :return the haplotype pattern and their cultivars
'''


def pattern_n(_bi_allele, _alleles):  # the minor allele of the _bi_allele would be remained and lower case be returned
    if _bi_allele[0] == _bi_allele[1]:
        return _bi_allele[0]
    else:
        if _alleles.index(_bi_allele[0]) < _alleles.index(_bi_allele[1]):
            return _bi_allele[1].lower()
        else:
            return _bi_allele[0].lower()


mh_file = sys.argv[1]
if len(sys.argv) == 2:
    fout = sys.stdout
elif len(sys.argv) > 2:
    fw = sys.argv[2]
    fout = open(fw, 'a')

con = mdb.connect(host='localhost', user='root', passwd='piao2551', db='3K_SNP')
cultivars = []
with con:
    cur = con.cursor()
    # obtain the cultivars
    cul_sql = 'SELECT * FROM cultivar ORDER BY name ASC;'
    cur.execute(cul_sql)
    for row in cur.fetchall():
        cultivars.append(row[0])

    # start the haplotype analysis, first step is to obtain the corresponding snp_seq
    with open(mh_file, 'r') as f:
        for line in f:
            seqs = []
            snp_info = {}  # key: miRNA, value: list of alleles in descending order by their freq
            pattern_cultivar = {}  # key: pattern, value: cultivars(list)

            line = line.rstrip('\n')
            elements = line.split()
            job = elements[0]
            snp_list = elements[1:]
            snps = ['"%s"' % i for i in snp_list]
            # Get the alleles of the SNP in descending order
            sql1 = 'SELECT allele_1, allele_2, allele_3, allele_4 FROM SNP WHERE id IN (%s);' % ', '.join(snps)
            cur.execute(sql1)
            for index, row in enumerate(cur.fetchall()):
                snp_id = snp_list[index]
                snp_info[snp_id] = []
                for allele in row:
                    if allele is not None:
                        snp_info[snp_id].append(allele)

            sql2 = 'SELECT snp_seq FROM SNP_cultivar WHERE snp_id IN (%s);' % ', '.join(snps)
            cur.execute(sql2)
            for row in cur.fetchall():
                seqs.append(row[0])

            for index, cul in enumerate(cultivars):
                pattern = ''
                for i, snp_id in enumerate(snp_list):  # seqs[] is in the order of snp_list (in ASCENDING order)
                    bi_allele = seqs[i][index*2:index*2+2]
                    base = pattern_n(bi_allele, snp_info[snp_id])
                    pattern += base
                if pattern not in pattern_cultivar:
                    pattern_cultivar[pattern] = [cul]
                else:
                    pattern_cultivar[pattern].append(cul)

            # print out the results
            content = ''
            for pattern in pattern_cultivar:
                if len(pattern_cultivar[pattern]) >= THRESHOLD:
                    content += '%s\t%s\t%s\t%s\r' % (job, pattern, len(pattern_cultivar[pattern]), ','.join(pattern_cultivar[pattern]))
            fout.write(content)
fout.close()
