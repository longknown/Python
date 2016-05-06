#!/usr/bin/python
import sys
import re
'''This script aims to sum up number of mismatches/G:U pairs (counted as 0.5 mismatches) at each site'''

__author__ = 'Thomas'


# for only miRNA named like osa-miRXXXa or osa-miRXXX would be reserved.
def reserve(_pair):
    pattern1 = re.compile('(osa-miR\d+a)')
    pattern2 = re.compile('(osa-miR\d+)[^0-9a-z]')
    if re.match(pattern1, _pair) or re.match(pattern2, _pair):
        return True
    return False


filename = sys.argv[1]
site_data = {}  # site: mismatch info

ln = 0
with open(filename, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        pattern = elements[0]
        pair = elements[1]
        if not reserve(pair):
            continue

        ln += 1  # only reserved interaction pairs would be reserved
        for ind, ele in enumerate(pattern):
            site_num = ind + 1
            if ele == '0':
                continue
            if site_num not in site_data:
                site_data[site_num] = {}
            if ele not in site_data[site_num]:
                site_data[site_num][ele] = 0
            site_data[site_num][ele] += 1

for i in sorted(site_data.keys()):
    line2print = '%s:\t' % i
    for ele in site_data[i]:
        if ele == '1':
            temp = 'Mismatch'
        elif ele == '*':
            temp = 'G:U'
        else:
            temp = 'INDEL'
        line2print += temp + '==>'
        line2print += '{0:.2%}\t'.format(site_data[i][ele] / float(ln))
    line2print.rstrip('\t')
    print line2print

print 'Total number of interaction pairs: %s' % ln
