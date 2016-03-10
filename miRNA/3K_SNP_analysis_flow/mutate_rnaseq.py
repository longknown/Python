#!/usr/bin/python

__author__ = 'Thomas'


def reverse_allele(_base):
    map_list = {'A': 'U', 'a': 'u', 'T': 'A', 't': 'a', 'C': 'G', 'c': 'g', 'G': 'C', 'g': 'c'}
    return map_list[_base]


def mutate_seq(_rna_seq, _strand_forward, _start, _end, _pos_list, _pattern):
    rna_list = list(_rna_seq)
    # obtain the point mutation loci
    for _index, _allele in enumerate(_pattern):
        if _allele == 'N':
            continue

        mutate_allele = _allele
        _pos = _pos_list[_index]
        if _strand_forward == '+':
            _rel_pos = _pos - _start
            if _allele == 'T':
                mutate_allele = 'U'
            elif _allele == 't':
                mutate_allele = 'u'
        else:  # if _strand_forward == '-'
            _rel_pos = _end - _pos
            mutate_allele = reverse_allele(_allele)
        rna_list[_rel_pos] = mutate_allele
    return ''.join(rna_list)


def rela_pos(_strand_forward, _start, _end, _pos):
    if _strand_forward == '+':
        return _pos - _start
    else:  # if _strand_forward == '-'
        return _end - _pos
