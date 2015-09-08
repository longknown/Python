#!/usr/bin/python
''' Usage: For each miRNA precursor, input SNP IDs within precursor regions to obtain the genotype (haplotype);
    Input file format: miRNA name, SNP1, SNP2, SNP3...
    Return: Grasp the CSV file from website and classify its pattern;
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests as req
import csv

threshold = 10  # the threshold of number of cultivars corresponding to each pattern
ignore_col = ['SNP ID', 'Chromosome', 'Position', 'Reference', 'Major Allele', 'Minor Allele']

def classify_pattern(csv_content, mirna):
    '''
    :param csv_content: the content of csv file from RiceVarMap
    :param mirna: name of miRNA
    :return: a list of lists, each list stands for a line in the new CSV file
    '''
    sample = {}  # This hash tab: key--cultivar name; value--corresponding pattern.

    line_list = csv_content.splitlines()
    reader = csv.DictReader(line_list)
    cultivar_column = [i for i in reader.fieldnames if i not in ignore_col]
    li_dict = []
    for lin in reader:
        li_dict.append(lin)
    li_dict.sort(key=lambda k: k['SNP ID'])  # sort the lines by the ascending order of 'SNP ID'
    for lin in li_dict:
        for cultivar in cultivar_column:
            if cultivar not in sample:
                sample[cultivar] = lin[cultivar]
            else:
                sample[cultivar] += lin[cultivar]

    # Reverse key & value for sample{}
    pattern = {}
    for s in sample:
        if sample[s] in pattern:
            pattern[sample[s]].append(s)
        else:
            pattern[sample[s]] = [s]
    double_list = []

    for p in pattern:
        if len(pattern[p]) >= threshold:
            cultivars = ';'.join(pattern[p])
            csv_line = [mirna, p, str(len(pattern[p])), cultivars]
            double_list.append(csv_line)
    return double_list


baseurl = 'http://ricevarmap.ncpgr.cn/snp_id_results/'
ingroup_list = [str(i) for i in range(1, 1492)]
payload = {'InGroup': ingroup_list, 'download': 'download'}
user_agent = {'User-agent': 'chrome'}
snp_file = sys.argv[1]
output_list = []  # stores all lines ready to be written to CSV file
with open(snp_file, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        mirna = elements[0]
        snp_str = '%09'.join(elements[1:])  # RiceVarMap receives params like this 'snp1%09snp2%09snp3'
        payload['snp_ids'] = snp_str
        try:
            r = req.post(baseurl, data=payload, headers=user_agent)
        except Exception as e:
            print('Network Exception:', e)
        print 'miRNA: "%s" genotype retrieved successfully!!!' % mirna
        csv_content = r.text
        double_list = classify_pattern(csv_content, mirna)
        output_list.extend(double_list)

with open('pattern_output.csv', 'w') as f2:
    writer = csv.writer(f2)
    writer.writerows(output_list)
