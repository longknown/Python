#!/usr/bin/python

import sys
import MySQLdb as mdb
reload(sys)
sys.setdefaultencoding('utf-8')

def _get_var(seq, var_list, snp_id, category):
    '''
    :param seq: the encoding sequence
    :param var_list: the fetched variety name list from database
    :param snp_id: the corresponding SNP
    :param category: the name of sub-rice-species, including indica, japonica...
    :return: create a file containing the cultivar
    '''
    f = file('./'+snp_id+'_'+category, 'w')
    file_content = ''
    for i in range(1, len(seq)/2):
        allele = seq[2*i-2:2*i]
        if allele != '00':
            line = var_list[i-1] + '\t' + seq[2*i-2:2*i] + '\n'
            file_content.__add__(line)
    f.write(file_content)
    f.close()




chr_id = int(sys.argv[1])
start = int(sys.argv[2])
end = int(sys.argv[3])

chr_id = '{0:02}'.format(chr_id) # format integer to width=2, such as 1 = 01
db = mdb.connect('localhost', 'root', 'piao2551', '3Krice_SNP', charset='utf8')

# Obtain the cursor
cursor = db.cursor()

# Obtain cultivar names from 3 tables
sql_indica = 'SELECT var_name FROM indica_variety'
sql_japonica = 'SELECT var_name FROM japonica_variety'
sql_other = 'SELECT var_name FROM other_variety'
indica = []
japonica = []
other = []

try:
    # for Indica
    cursor.execute(sql_indica)
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        indica.append(row[0])

    # for japonica
    cursor.execute(sql_japonica)
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        japonica.append(row[0])

    # for other varieties
    cursor.execute(sql_other)
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        other.append(row[0])
except:
    print 'Error: unable to fetch data!!!'
    exit(1)


# SQL querying
sql = 'SELECT * FROM %s WHERE position >= %d AND position <= %d' % \
      ('chr'+chr_id+'_snps', start, end)
print 'SNP_id\tposition\tpopulation\tminor_allele\tmajor_allele\tminor_allele frequence\tminor_allele freq in Indica\tminor allele freq in japonica'
try:
    cursor.execute(sql)
    record = cursor.fetchall()

    for row in record:
        snp_id = row[0]
        position = row[2]
        population = row[3]
        minor_allele = row[4]
        major_allele = row[5]
        minor_freq = row[6]

        minor_indica_freq = row[7]
        indica_population = row[8]
        indica_seq = row[9]
        _get_var(indica_seq, indica, snp_id, 'indica')

        minor_japonica_freq = row[10]
        japonica_population = row[11]
        japonica_seq = row[12]
        _get_var(japonica_seq, japonica, snp_id, 'japonica')

        minor_other_freq = row[13]
        other_population = row[14]
        other_seq = row[15]
        _get_var(other_seq, other, snp_id, 'other')
        print '%d\t%d\t%d\t%c\t%c\t%.2f%%\t%.2f%%\t%.2f%%' % \
              (snp_id, position, population, minor_allele, major_allele, minor_freq*100, minor_indica_freq*100, minor_japonica_freq*100)
except:
    print 'Error: unable to fetch data!!!'
    exit(1)

db.close()
