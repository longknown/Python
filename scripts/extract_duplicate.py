#!/usr/bin/python
import sys

__author__ = 'Thomas'

predict_file = sys.argv[1]

pair_dict = {}  # key: parental pair name; value: different records;
with open(predict_file, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        concat_name = elements[0]
        pair_parent = '::'.join([concat_name.split('::')[0],concat_name.split('::')[1].split('.')[0]])
        binding_site = elements[15]
        if pair_parent not in pair_dict:
            pair_dict[pair_parent] = {binding_site: line}
        else:
            if binding_site not in pair_dict[pair_parent]:
                pair_dict[pair_parent][binding_site] = line

for temp in pair_dict:
    if len(pair_dict[temp]) > 1:
        print temp+':'
        for b in pair_dict[temp]:
            print pair_dict[temp][b]
        print '*' * 80
