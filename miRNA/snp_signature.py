#!/usr/bin/python
''' Usage: reads in a table containing SNPs within miRNAs, table headers are miRNA name(1), snp_id(2), ref_allele(3),
nonRef_allele(4).
Options:
-p  prints the pattern of SNPs within each miRNAs;
-s  prints the SNP name within each miRNAs
'''
import sys

fn = sys.argv[2]
f1 = file(fn)

mi_sig = {}
while True:
    line = f1.readline()
    if len(line) == 0:
        break
    line = line.rstrip('\n')
    elements = line.split()
    name = elements[0]
    ref_a = elements[2]
    nonRef_a = elements[3]
    snp_id = elements[1]

    if name in mi_sig:
        mi_sig[name][0] += ref_a
        mi_sig[name][1] += nonRef_a
        mi_sig[name][2].append(snp_id)
    else:
        mi_sig[name] = [ref_a, nonRef_a, [snp_id]]
f1.close()

# sort the snp_ids within each precursor
for i in mi_sig:
    mi_sig[i][2].sort()

option = sys.argv[1]
if option == '-p':  # print the pattern of SNPs within each miRNAs
    for i in mi_sig:
        print i + '\t' + str(len(mi_sig[i][0])) + '\t' + mi_sig[i][0] + '\t' + mi_sig[i][1]
elif option == '-s':  # print the SNP name within each miRNAs
    for i in mi_sig:
        sys.stdout.write(i + '\t' + str(len(mi_sig[i][0])))
        for j in range(0, len(mi_sig[i][0])):
            sys.stdout.write('\t'+mi_sig[i][2][j])
        print
else:
    pass
