#!/usr/bin/python
__author__ = 'Thomas'

REF_GENOME_PATH = '/Users/Thomas/Academy/RiceGenome/msu7.0/BLAST_local_genome/all.chr.con'
from Bio import SeqIO
import MySQLdb as mdb

def obtain_N(seqrecords, chr_id, pos):
    return seqrecords[chr_id][pos-1]
records = {}
for record in SeqIO.parse(REF_GENOME_PATH, 'fasta'):
    records[record.id] = record.seq

con = mdb.connect('localhost', 'root', 'piao2551', '3K_SNP')
command = 'SELECT id, chr_id, position FROM SNP;'
snps = {}
with con:
    cur = con.cursor()
    cur.execute(command)
    for row in cur.fetchall():
        snps[row[0]] = [row[1], row[2]]
    cur.execute('SET AUTOCOMMIT = 0;')
    for snp_id in snps:
        chr_id = snps[snp_id][0]
        pos = snps[snp_id][1]
        ref_allele = obtain_N(records, chr_id, pos)
        update_command = 'UPDATE SNP SET ref_allele="%s" WHERE id="%s";' % (ref_allele, snp_id)
        cur.execute(update_command)
        print 'Update SNP: %s succeeded!!!' % snp_id
