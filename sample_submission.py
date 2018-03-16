from collections import Counter
from itertools import groupby
from itertools import permutations


def group_by(data, group_col, value_col, agg_function):
    """ Group by
        Inputs:
          - data: list of tuples e.g.: [('A', 2, 3), ('A', 3, 4)]
          - group_col: int, column to group by e.g.: 0
          - value_col: int, column to aggregate e.g: 1
          - agg_function: agg function, so e.g. : sum
            it is applied to list of values in value_col
            for the group
            e.g. sum([1, 2, 3])
        Output:
          - out: dict group_name -> value {'A': 5}
    """
    out = {}
    return out


def num_bad_permutations(n):
    """
    Number of permutations of length n
    where each element is not on its place
    Inputs:
      - n: int, length of permutation
    Output:
      - num_perm: int, number of such permutations
    """
    from itertools import permutations
    num_perm = 0
    for i in list(permutations(range(n))):
        f = True
        for j, k in enumerate(i):
            if i == k:
                f = False
        if f:
            num_perm += 1
    return num_perm


def count_ngrams(text, n):
    """
        Counter of symbol ngrams
        Inputs:
          - text: str, some text
          - n: int, length of symbol ngram
        Output:
          - ngrams: Counter, ngram-> number of times
                                     it was in text
        """
    ngrams = Counter()
    return ngrams
