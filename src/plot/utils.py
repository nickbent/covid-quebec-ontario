from itertools import islice

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def nday_avg(data, n):
    avg = []
    for ndays in window(data, n):
        avg.append(sum(ndays)/n)
    return avg

def per100k(data, population):
    return [ total/p*100000 for total, p in zip(data, population)]

def string_to_float(string):
    return float(string.replace(",", "."))