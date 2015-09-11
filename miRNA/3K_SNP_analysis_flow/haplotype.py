#!/usr/bin/python
import sys
__author__ = 'thomas'
'''Usage
        :param inputs a simple file with miRNA name & SNP id
        :return haplotype for each miRNA
'''

infile = sys.argv[1]
if len(sys.argv) == 2:
    fw = sys.stdout
else:
    outf = sys.argv[2]
    fw = open(outf, 'w')
mir_snp = {}
with open(infile, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        mirname = elements[0]
        snp = elements[1]
        if mirname not in mir_snp:
            mir_snp[mirname] = [snp]
        else:
            mir_snp[mirname].append(snp)

out_result = ''
for name in mir_snp:
    mir_snp[name].sort()  # This steps help to ensure that the miRNA haplotype is in ascending order
    out_result += name+'\t'+str(len(mir_snp[name]))+'\t'+'\t'.join(mir_snp[name])+'\n'
fw.write(out_result)
fw.close()
