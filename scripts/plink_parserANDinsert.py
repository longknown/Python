#!/usr/bin/python
__author__ = 'Thomas'

import sys
import MySQLdb as mdb
from Bio import SeqIO
from fileformat_parser import plink_parse, tab_parse
import os
reload(sys)
sys.setdefaultencoding('utf-8')
''' This script requires a text file containing the list for .map & .ped files;
'''

INSERT_ROW_NUMBER = 800  # A global define of the inserting row number;
REF_GENOME_PATH = '/Users/Thomas/Academy/RiceGenome/msu7.0/BLAST_local_genome/all.chr.con'

records = {}
for record in SeqIO.parse(REF_GENOME_PATH, 'fasta'):
    records[record.id] = record.seq


fn = sys.argv[1]
con = mdb.connect('localhost', 'root', 'piao2551', '3K_SNP')
with con:
    # First obtain all the SNP ids from the database
    cur = con.cursor()
    cur.execute('SELECT id FROM SNP')
    snps = []
    for i in cur.fetchall():
        snps.append(i[0])

    cur.execute('SET AUTOCOMMIT = 0;')
    with open(fn, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if os.path.exists(line+'.map'):
                snp_array = plink_parse(line+'.map', line+'.ped')
                print 'Plink %s file parse succeeded!!!' % line
            elif os.path.exists(line+'.txt'):
                filename_parse = line.split('-')
                chr_id = filename_parse[1][-5:]
                snp_array = tab_parse(line+'.txt', chr_id)
                print 'TAB %s file parse succeeded!!!' % line

            snp_number_insert = 1
            command_SNP = 'INSERT INTO SNP VALUES '
            command_seq = 'INSERT INTO SNP_cultivar VALUES '
            for index, snp in enumerate(snp_array):
                if snp.id in snps:  # to avoid duplicate keys, so judge whether the SNP has been inserted before
                    continue
                else:
                    snps.append(snp.id)

                ref_allele = records[snp.chr_id][snp.position-1]
                alleles = snp.alleles()
                a_f = snp.allele_freq()
                values = [snp.id, snp.chr_id, snp.position, len(snp.snp_cul), ref_allele]
                if len(alleles) == 1:  # Skip those doubtful SNPs
                    continue
                for a in alleles:
                    values.append('"%s"' % a)
                    values.append(a_f[a])
                # To make 'values' contains (id, chr_id, position, population...), there shall be some NULLs to fill
                while True:
                    if len(values) == 13:
                        break
                    values.append('NULL')
                values = tuple(values)
                command_SNP += '("%s", "%s", %s, %s, "%s", %s, %s, %s, %s, %s, %s, %s, %s),' % values
                snp_seq = snp.snp_seq()
                command_seq += '("%s", "%s"),' % (snp.id, snp_seq)
                if snp_number_insert == INSERT_ROW_NUMBER or index == len(snp_array)-1:
                    command_SNP = command_SNP[:-1]+';'
                    cur.execute(command_SNP)
                    command_seq = command_seq[:-1]+';'
                    cur.execute(command_seq)
                    print '%d SNPs or rest of them along with their seq INSERTION succeeded!!!' % INSERT_ROW_NUMBER
                    command_SNP = 'INSERT INTO SNP VALUES '
                    command_seq = 'INSERT INTO SNP_cultivar VALUES '
                    snp_number_insert = 1
                snp_number_insert += 1
            print('\n')
            con.commit()
