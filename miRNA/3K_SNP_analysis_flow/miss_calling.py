#!/usr/bin/python
__author__ = 'thomas'
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'piao2551', '3K_SNP')
hetero_pair = []  # every cultivar along with the corresponding SNP is taken as a hetero_pair
cultivars = []
with con:
    cur = con.cursor()
    # Obtain all cultivar names
    sql1 = 'SELECT name FROM cultivar ORDER BY name ASC;'
    cur.execute(sql1)
    for row in cur.fetchall():
        cultivars.append(row[0])

    sql2 = 'SELECT * FROM SNP_cultivar;'
    cur.execute(sql2)
    print 'SELECT command finished!!!'
    number = 0
    for row in cur.fetchall():
        snp = row[0]
        seq = row[1]
        for ind, cul in enumerate(cultivars):
            bi_allele = seq[2*ind: 2*(ind+1)]
            if bi_allele == '00':
                number += 1
print number
