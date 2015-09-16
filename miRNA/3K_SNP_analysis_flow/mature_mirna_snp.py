#!/usr/bin/python
import sys
import MySQLdb as mdb
from mutate_rnaseq import mutate_seq, rela_pos

__author__ = 'Thomas'

con = mdb.connect(host='localhost', user='root', passwd='piao2551', db='3K_SNP')
infile = sys.argv[1]

if len(sys.argv) == 2:
    fout = sys.stdout
elif len(sys.argv) > 2:
    fw = sys.argv[2]
    fout = open(fw, 'w')

with con:
    cur = con.cursor()
    with open(infile, 'r') as f:
        content = ''
        for line in f:
            snp_list = []
            pos_list = []
            alleles_list = []
            ref_allele_list = []
            line = line.rstrip('\n')
            elements = line.split()
            job = elements[0]
            strand_forward = elements[1]
            chr_id = elements[2]
            start = int(elements[3])
            end = int(elements[4])
            mature_sequence = elements[5]

            # Now here comes the MySQL manipulation
            sql = 'SELECT id, position, ref_allele, allele_1, allele_2, allele_3, allele_4 FROM SNP WHERE ' \
                  'chr_id="%s" AND position BETWEEN %s AND %s;' % (chr_id, start, end)
            cur.execute(sql)
            for row in cur.fetchall():
                snp_list.append(row[0])
                pos_list.append(int(row[1]))
                ref_allele_list.append(row[2])
                alleles = ''
                for allele in row[3:]:
                    if allele is not None:
                        alleles += allele
                alleles_list.append(alleles)
            if len(snp_list) == 0:
                continue

            # print out the results
            content += '%s, Number of SNPs:%s\n' % (job, len(snp_list))
            for index, snp in enumerate(snp_list):
                pos = pos_list[index]
                alleles = alleles_list[index]
                ref_allele = ref_allele_list[index]
                relative_pos = rela_pos(strand_forward, start, end, pos)
                content += '%s, Relative Position:%s\n' % (snp, relative_pos+1)
                for allele in alleles:
                    if allele == ref_allele:
                        continue
                    content += 'Mutated allele: %s\n' % allele
                    altered_seq = mutate_seq(mature_sequence, strand_forward, start, end, pos_list, allele)
                    match_line = ['|'] * len(mature_sequence)
                    match_line[relative_pos] = '*'
                    content += '%s\n%s\n%s\n' % (mature_sequence, ''.join(match_line), altered_seq)
            content += '\n'
            print content
fout.write(content)
fout.close()
