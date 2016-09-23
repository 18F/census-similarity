import re

import distance as dist_lib

from census_similarity.clustering import ClusterTechnique


class SetDistance(ClusterTechnique):
    @staticmethod
    def distance(left, right):
        return 1 - (len(left & right) / len(left | right))


class CharacterBag(SetDistance):
    @staticmethod
    def transform(string):
        return frozenset(string.upper())


class Trigrams(SetDistance):
    @staticmethod
    def transform(string):
        string = string.upper() + "  "
        trigrams = []
        for i in range(len(string) - 2):
            trigrams.append(string[i:i+3])
        return frozenset(trigrams)


class UppercaseOnly(ClusterTechnique):
    nonletter = re.compile('[^A-Z]')

    @classmethod
    def transform(cls, string):
        return cls.nonletter.sub('', string.upper())


class Levenshtein(UppercaseOnly):
    @staticmethod
    def distance(left, right):
        return dist_lib.levenshtein(left, right, normalized=True)


class Jaccard(UppercaseOnly):
    @staticmethod
    def distance(left, right):
        return dist_lib.jaccard(left, right)
