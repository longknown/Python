#!/usr/bin/python
'''
 This script is written to parse the phenotype table downloaded from RiceVarMap and obtain the haplotype of these SNPs;
 FileFormat: columns are SNP ID, chr_id, position, Ref_allele, Major_allele, Minor allele, cultivars...
 Threshold: Every pattern containing cultivars > 10, will be shown, others will be screened out;
 Note: 'N' base will be kept; ',' is the delimiter of the file.
 Output: a .csv file would be saved, you can specify the output name in the third parameter.
'''
import sys
import csv

# Some const settings
threshold = 10  # the threshold of number of patterns (#ofPatterns >= 10 kept)
ignore_set = ['SNP ID', 'Chromosome', 'Position', 'Reference', 'Major Allele', 'Minor Allele']

csv_file = sys.argv[1]
# if just one param is passed, name the output file according to input file, otherwise specify it with the 2nd param
if len(sys.argv) > 2:
    miRname = sys.argv[2]
else:
    miRname = sys.argv[1][:-4]

output_csv = miRname + '_out.csv'
f1 = open(csv_file)
sample = {}  # This hash tab: key--cultivar name; value--corresponding pattern.

reader = csv.DictReader(f1)
for field in reader.fieldnames:  # initiate sample{}
    if field not in ignore_set:
        sample[field] = ''

for line in reader:
    for column in line:
        if column not in ignore_set:
            sample[column] += line[column]
f1.close()
# Reverse the hash tab of sample{} to pattern{}
pattern = {}  # Hash tab: key--pattern; value--list of cultivars
for s in sample:
    if sample[s] not in pattern:
        pattern[sample[s]] = [s]
    else:
        pattern[sample[s]].append(s)

# Write to .csv the result with the threshold
f2 = open(output_csv, 'w')
writer = csv.writer(f2)
csv_content = []
for p in pattern:
    if len(pattern[p]) >= threshold:
        cultivars = ';'.join(pattern[p])
        csv_column = [miRname, p, str(len(pattern[p])), cultivars]  # you can add miRNA name in this line
        csv_content.append(csv_column)
writer.writerows(csv_content)
f2.close()
