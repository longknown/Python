#!/usr/bin/python
import csv
import sys
'''The script aims to combine replicate columns of expression pattern to get the average expression level
'''
__author__ = 'Thomas'

exp_file = sys.argv[1]
abbr_file = sys.argv[2]
output_file = sys.argv[3]

abbr_list = {}
with open(abbr_file, 'r') as f1:
    f1.readline()
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split('\t')
        sourcename = elements[0]
        abbr_name = elements[3][:-5]
        if abbr_name not in abbr_list:
            abbr_list[abbr_name] = []
        abbr_list[abbr_name].append(sourcename)

with open(output_file, 'w') as f2:
    fieldnames = sorted(abbr_list.keys())
    fieldnames = ['probeName'] + fieldnames
    writer = csv.DictWriter(f2, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    with open(exp_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        write_row_dict = {}
        for row in reader:
            write_row_dict['probeName'] = row['probeName']
            for abbr in abbr_list:
                temp_list = [float(row[i]) for i in abbr_list[abbr]]
                temp_value = reduce(lambda x, y: x+y, temp_list) / len(temp_list)
                write_row_dict[abbr] = temp_value
            writer.writerow(write_row_dict)
