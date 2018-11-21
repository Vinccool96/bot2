import itertools


def mes_combs_str(iter: str, n: int):
    res = []
    if iter and n > 1:
        combs = list(itertools.combinations(iter, n))
        for comb in combs:
            st = comb[0]
            for let in comb[1:]:
                st += let
            res += [st]

    return res


def mes_combs_rep_str(iter: str, n: int):
    res = []
    if iter and n > 1:
        combs = list(itertools.combinations_with_replacement(iter, n))
        for comb in combs:
            st = comb[0]
            for let in comb[1:]:
                st += let
            res += [st]

    return res


def mes_perm_str(iter: str):
    res = []
    if iter:
        combs = list(itertools.permutations(iter, len(iter)))
        for comb in combs:
            st = comb[0]
            for let in comb[1:]:
                st += let
            res += [st]

    return res


def comb_ordr_rep_str(iter):
    res = []
    for i in range(len(iter)):
        res = add_c_of_str_to_strs(res, iter)
    return res


def add_c_of_str_to_strs(l: list, s: str):
    res = []
    if not l:
        res = list(s)
    for item in l:
        sub_l = []
        for c in s:
            sub_l += [(item+c)]
        res += sub_l
    return res


def comb_ordr_rep__of_len_str(iter: str, n: int):
    res = []
    for i in range(n):
        res = add_c_of_str_to_strs(res, iter)
    return res


def comb_ordr_rep__of_len_in_range_str(iter: str, start: int, stop: int):
    res = []
    for i in range(start, stop):
        res = comb_ordr_rep__of_len_str(iter, i)
    return res
