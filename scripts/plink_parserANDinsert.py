#!/usr/bin/python
import sys
import MySQLdb as mdb
from Bio import SeqIO
from fileformat_parser import plink_parse, tab_parse
import os
reload(sys)
sys.setdefaultencoding('utf-8')
''' This script requires a text file containing the list for .map & .ped files;
'''

INSERT_ROW_NUMBER = 400  # A global define of the inserting row number;
REF_GENOME_PATH = '/home/thomas/Academy/RiceGenome/all.chr.con'

records = {}
for record in SeqIO.parse(REF_GENOME_PATH, 'fasta'):
    records[record.id] = record.seq


fn = sys.argv[1]
wd = sys.argv[2]
wd = wd.rstrip('\/')+'/'
con = mdb.connect('localhost', 'root', 'piao2551', '3000osaSNP')
with con:
    # First obtain all the SNP ids from the database
    cur = con.cursor()
    cur.execute('SELECT id FROM SNP;')
    snps = []
    for i in cur.fetchall():
        snps.append(i[0])

    with open(fn, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if os.path.exists(wd+line+'.map'):
                snp_array = plink_parse(wd+line+'.map', wd+line+'.ped')
                print 'Plink %s file parse succeeded!!!' % wd+line
            elif os.path.exists(wd+line+'.txt'):
                filename_parse = line.split('-')
                chr_id = filename_parse[1][-5:]
                snp_array = tab_parse(wd+line+'.txt', chr_id)
                print 'TAB %s file parse succeeded!!!' % wd+line
            else:
                print 'No such files are found: %s' % wd+line
                continue

            # insert the intervals into the table 'cover_regions'
            line = line[13:]
            elements = line.split('-')
            chrid = elements[0]
            _start = int(elements[1])
            _end = int(elements[2])
            interval_cmd = 'SELECT * FROM cover_regions WHERE chr_id="%s" ORDER BY _start;' % chrid
            cur.execute(interval_cmd)
            insert_region_base = 'INSERT INTO cover_regions (chr_id, _start, _end) VALUES '
            region_list = []
            for row in cur.fetchall():
                region_list.append(row)
            if len(region_list) != 0:
                for row in region_list:
                    if _end < row[2]-1:
                        break
                    elif _start <= row[3]+1:
                        _start = min(_start, row[2])
                        _end = max(_end, row[3])
                        delete_cmd = 'DELETE FROM cover_regions WHERE regionNO="%s";' % row[0]
                        cur.execute(delete_cmd)
                    else:
                        continue
            insert_cmd = insert_region_base + '("%s", %s, %s);' % (chrid, _start, _end)
            cur.execute(insert_cmd)

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
