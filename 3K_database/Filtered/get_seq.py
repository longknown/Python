#!/usr/bin/python
#This file helps to extract individual snp and encode the alleles of all cultivals into a sequence
#input parameters are snp_id; plink filename;path to output the ped file

import os
import sys

snpid_file = sys.argv[1]
plinkfile = sys.argv[2]
path = sys.argv[3]

f1 = file(snpid_file)
outfile = file(path+'/seq', 'w')

while True:
    snp_interval = f1.readline()
    if len(snp_interval) == 0:
        break
    snp_interval = snp_interval.rstrip('\n') #get rid of \n

    snp_from = snp_interval.split()[0]  # every line is a interval of SNP, and the file covers the whole snp_id
    snp_to = snp_interval.split()[1]

    os.system("plink --bfile " + plinkfile + " --recode compound-genotypes --from " + snp_from + " --to " + snp_to + " --out " + path + "/snp")
    f2 = file(path+'/snp.ped')
    lists = [[] for i in range(50001)]  # create 10001 lists, in fact 2-D array
    while True:
        line = f2.readline()
        if len(line) == 0:
            break
        line = line.rstrip('\n')
        column = line.split()
        for i in range(len(column)-6):
            lists[i].append(column[i+6])
    f2.close()
    for item in lists:
        if len(item) == 0:
            continue
        w_line = ''.join(item)
        outfile.write(w_line+'\n')
    print "SNPs to "+snp_interval+" have been finished processing!"
f1.close()
outfile.close()
