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


def distance_matrix(values, metric):
    """Generate a matrix of distances based on the `metric` calculation.
    :param values: list of sequences, e.g. list of strings, list of tuples
    :param metric: function (value, value) -> number between 0.0 and 1.0"""
    matrix = []
    progress = ProgressTracker(len(values))

    for lidx, left in enumerate(values):
        progress.tick(lidx)
        row = []
        for right in values:
            row.append(metric(left, right))
        matrix.append(row)
    return np.array(matrix)


def cluster_labels(values, metric, eps, min_samples):
    """Cluster data by the provided metric. Label the values by those
    clusters.
    :param values: list of sequences, e.g. list of strings, list of tuples
    :param metric: function (value, value) -> number between 0.0 and 1.0
    :param eps: maximum distance between points to be in a cluster
    :param min_samples: minimum number of points before a cluster can be
    created"""
    similarity = distance_matrix(values, metric)
    clusterer = DBSCAN(eps, min_samples, metric='precomputed')
    fit = clusterer.fit(similarity)
    return fit.labels_
