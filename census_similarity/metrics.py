import distance
from scipy import spatial


def cosine(left, right):
    elements = set(left) | set(right)
    elements = list(sorted(elements))
    left = [int(el in left) for el in elements]
    right = [int(el in right) for el in elements]
    return spatial.distance.cosine(left, right)


def levenshtein(left, right):
    return distance.levenshtein(left, right, normalized=True)


def jaccard(left, right):
    return distance.jaccard(left, right)
