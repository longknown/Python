#!/usr/bin/python
import sys
import requests as req
import bs4

def search_regions(chr_id, start, end):
    '''
    :param chr_id: chromosome id;
    :param start: starting position of the region;
    :param end: ending position of the region;
    :return: a list, including SNP name, SNP position, reference allele, major allele, minor allele & major freq
    '''
    baseurl = 'http://ricevarmap.ncpgr.cn/region/?'
    user_agent = {'User-agent': 'chrome'}
    payload = {'chr': chr_id, 'pos_start': start, 'pos_end': end}

    snp_list = []
    # crawl the web
    try:
        r1 = req.get(baseurl, params=payload, headers=user_agent)
    except Exception as e:
        print('Network exception:', e)

    # BeautifulSoup to handle the returned webpage
    soup = bs4.BeautifulSoup(r1.text)

    # Step1: check whether exists SNPs within this region, if not, exit program and report
    result_span = soup.find('span', attrs={'class': 'tit'})
    snp_result = result_span.p.string
    if snp_result == '0 result found.':
        print 'No SNP is found within Chr: %s, pos_start: %s, pos_end: %s' % (chr_id, start, end)
        return snp_list
    else:
        table = soup.find('table', attrs={'class': 'imagetable'})
        snp_info = table.find_all('tr', attrs={'align': 'center'})
        for snp in snp_info:
            snp_elements = []
            snp_soup = bs4.BeautifulSoup(str(snp))
            text = str(snp_soup.text)
            elements = text.split('\n')

            # Store the elements of SNP into a list
            snp_elements.append(elements[1][0:12])
            snp_elements.append(elements[2])
            snp_elements.append(elements[3])
            snp_elements.append(elements[4])
            snp_elements.append(elements[5])
            snp_elements.append(elements[6])
            snp_elements.append(elements[7][1:-1])

            # snp_list is the list of list
            snp_list.append(snp_elements)
        return snp_list


def search_help():
    print '''Usage of program:
    1. simply pass the parameter of a searching region, including chr_id, start, end;
    2. pass a file containing miRNAs and their region infos:
        line columns are: chr_id, start, end, miRNA name;
    -f for file input
    -h for help
    '''
    exit()

if len(sys.argv) == 1:
    search_help()
    exit()
elif sys.argv[1][0] == '-':
    if sys.argv[1][1] == 'h':
        search_help()
        exit()
    elif sys.argv[1][1] == 'f':
        filename = sys.argv[2]
        f1 = file(filename)
        f2 = open('SNPs_found', 'w')

        while True:
            line = f1.readline()
            if len(line) == 0:
                break
            line = line.rstrip('\n')
            columns = line.split()  # line columns are chr_id, start, end, miRNA name;
            chr_id = columns[0]
            start = columns[1]
            end = columns[2]
            miRNA = columns[3]
            snp_list = search_regions(chr_id, start, end)
            if len(snp_list) == 0:
                continue
            else:
                output = ''
                for snp in snp_list:
                    output_line = '\t'.join(snp)
                    output += miRNA + '\t' + output_line + '\n'
                print 'SNPs has been found within region of miRNA: %s!!!' % miRNA
            f2.write(output)
        f1.close()
        f2.close()
    else:
        search_help()
        exit()
else:
    chr_id = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    snp_list = search_regions(chr_id, start, end)
    if len(snp_list) == 0:
        exit()
    else:
        for snp in snp_list:
            output_line = '\t'.join(snp)
            print output_line
        exit()