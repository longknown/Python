__author__ = 'Thomas'

from snp import SNP, cultivars
import sys
import MySQLdb as mdb
reload(sys)
sys.setdefaultencoding('utf-8')
''' This script requires a text file containing the list for .map & .ped files;
'''

INSERT_ROW_NUMBER = 800  # A global define of the inserting row number;


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
            snp_array = plink_parse(line+'.map', line+'.ped')
            print 'Plink %s file parse succeeded!!!' % line

            snp_number_insert = 1
            command_SNP = 'INSERT INTO SNP (id, chr_id, position, population, \
                          allele_1, freq_1, allele_2, freq_2, allele_3, freq_3, allele_4, freq_4) VALUES '
            command_seq = 'INSERT INTO SNP_cultivar VALUES '
            for index, snp in enumerate(snp_array):
                if snp.id in snps:  # to avoid duplicate keys, so judge whether the SNP has been inserted before
                    continue
                else:
                    snps.append(snp.id)

                alleles = snp.alleles()
                a_f = snp.allele_freq()
                values = [snp.id, snp.chr_id, snp.position, len(snp.snp_cul)]
                if len(alleles) == 1:  # Skip those doubtful SNPs
                    continue
                for a in alleles:
                    values.append('"%s"' % a)
                    values.append(a_f[a])
                # To make 'values' contains (id, chr_id, position, allele_1..4), there shall be some NULLs to fill
                while True:
                    if len(values) == 12:
                        break
                    values.append('NULL')
                values = tuple(values)
                command_SNP += '("%s", "%s", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),' % values
                snp_seq = snp.snp_seq()
                command_seq += '("%s", "%s"),' % (snp.id, snp_seq)
                if snp_number_insert == INSERT_ROW_NUMBER or index == len(snp_array)-1:
                    command_SNP = command_SNP[:-1]+';'
                    cur.execute(command_SNP)
                    command_seq = command_seq[:-1]+';'
                    cur.execute(command_seq)
                    print '%d SNPs or rest of them along with their seq INSERTION succeeded!!!' % INSERT_ROW_NUMBER
                    command_SNP = 'INSERT INTO SNP (id, chr_id, position, population, \
                                  allele_1, freq_1, allele_2, freq_2, allele_3, freq_3, allele_4, freq_4) VALUES '
                    command_seq = 'INSERT INTO SNP_cultivar VALUES '
                    snp_number_insert = 1
                snp_number_insert += 1
            print('\n')
        con.commit()
