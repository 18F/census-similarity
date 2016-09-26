from collections import defaultdict
import logging
from time import time

import numpy as np
from sklearn.cluster import DBSCAN


logger = logging.getLogger(__name__)


class ProgressTracker:
    """Logs an status entry every 5 seconds"""
    def __init__(self, num_uniques):
        self.num_uniques = num_uniques
        self.next_time = time() + 5

    def tick(self, idx):
        if time() >= self.next_time:
            logger.info("%s/%s processed", idx, self.num_uniques)
            self.next_time = time() + 5


class ClusterTechnique:
    """Each clustering technique must define the "transform" and "distance"
    static methods"""
    @classmethod
    def distance_matrix(cls, uniques):
        """Generate a numpy matrix of distances between entries in the
        "uniques" list"""
        matrix = []
        progress = ProgressTracker(len(uniques))

        for lidx, left in enumerate(uniques):
            progress.tick(lidx)
            row = []
            for right in uniques:
                row.append(cls.distance(left, right))
            matrix.append(row)
        return np.array(matrix)

    @classmethod
    def cluster_groups(cls, all_strings, eps=0.10, min_samples=2):
        """Given a list of strings, cluster the uniques and return the
        groups"""
        transformed = [cls.transform(string) for string in all_strings]
        unique = list(set(transformed))     # Needs _any_ order
        similarity = cls.distance_matrix(unique)
        clusterer = DBSCAN(eps, min_samples, metric='precomputed')
        fit = clusterer.fit(similarity)

        cluster_by_input = []
        for value in transformed:
            label = fit.labels_[unique.index(value)]
            cluster_by_input.append(label)

        groups = defaultdict(set)
        for idx, cluster in enumerate(cluster_by_input):
            groups[cluster].add(all_strings[idx])
        del groups[-1]  # remove outliers
        return groups
