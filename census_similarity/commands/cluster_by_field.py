import sys

import click

from census_similarity import metrics, splits
from census_similarity.clustering import cluster_labels
from census_similarity.io import read_csv_write_header


@click.command()
@click.option('--eps', type=float, default=0.10,
              help='Similarity threshold (> 0.0, < 1.0)')
@click.option('--min-samples', type=int, default=2,
              help='Minimum distinct examples to form a cluster')
@click.option('--distance-metric', default='jaccard',
              type=click.Choice(['cosine', 'levenshtein', 'jaccard']))
@click.option('--field', default='name', help='Field to cluster on')
@click.option('--field-split', default='character',
              help='How the field should be split',
              type=click.Choice(['character', 'bigram', 'trigram', 'comma']))
@click.option('--group-field', default='_group', help='Field to write results')
@click.argument('input_file', required=False, type=click.File('rt'),
                default=sys.stdin)
@click.argument('output_file', required=False, type=click.File('rt'),
                default=sys.stdout)
def cluster_by_field(
        eps, min_samples, distance_metric, field, field_split, group_field,
        input_file, output_file):
    """Cluster similar CSV rows together.

    INPUT_FILE - CSV to read from, defaults to stdin
    OUTPUT_FILE - CSV to write to, defaults to stdout"""
    all_rows, writer = read_csv_write_header(
        input_file, output_file, [field], lambda hdr: hdr + [group_field])

    splitter = getattr(splits, field_split)
    metric = getattr(metrics, distance_metric)

    values = [splitter(row[field]) for row in all_rows]

    groups = cluster_labels(values, metric, eps, min_samples)
    next_group_id = max(groups) + 1
    for row, group in zip(all_rows, groups):
        if group == -1:
            group = next_group_id
            next_group_id += 1
        row[group_field] = group
        writer.writerow(row)
