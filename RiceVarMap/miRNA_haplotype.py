#!/usr/bin/python
import sys
import requests as req

snp_list = sys.argv[1]
f1 = file(snp_list)
output = ''
while True:
    line = f1.readline()
    if len(line) == 0:
        break

    line = line.rstrip('\n')
    columns = line.split()
    miRname = columns[0]
    snps = columns[1:]
    snps_str = snps[0]
    for i in range(1, len(snps)):
        snps_str += '%2C' + snps[i]
    payload = {'snp_ids': snps_str, 'group': 'group2', 'download_hap': 'download'}
    user_agent = {'User-agent': 'chrome'}
    baseurl = 'http://ricevarmap.ncpgr.cn/hap_net/?'

    try:
        r = req.get(baseurl, params=payload, headers=user_agent)
    except Exception as e:
        print('Network Exception: ', e)

    print 'Request for %s SNPs succeeded!!!' % miRname
    csv_content = str(r.text)
    # csv_content = csv_content.replace(',', '\t')  there is a ',' within a cultivar name
    output += miRname + '\n' + csv_content + '\n'  # Add miRNA name to the content for distinguishing
f1.close()

f2 = open('output_tb', 'w')
f2.write(output)
f2.close()
