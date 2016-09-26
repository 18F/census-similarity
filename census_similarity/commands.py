import csv
import logging
import sys

import click

from census_similarity import techniques


logger = logging.getLogger(__name__)


@click.command()
@click.option('--eps', type=float, default=0.10,
              help='Similarity threshold (> 0.0, < 1.0)')
@click.option('--min-samples', type=int, default=2,
              help='Minimum distinct examples to form a cluster')
@click.option('--technique', default='Jaccard', help='Similarity metric',
              type=click.Choice(['CharacterBag', 'Levenshtein', 'Jaccard',
                                 'Trigrams']))
@click.option('--field', default='name', help='Field to cluster on')
@click.argument('input_file', required=False, type=click.File('rt'),
                default=sys.stdin)
@click.argument('output_file', required=False, type=click.File('rt'),
                default=sys.stdout)
def cluster_by_field(input_file, output_file, eps, min_samples, technique,
                     field):
    """Cluster similar CSV rows together.

    INPUT_FILE - CSV to read from, defaults to stdin
    OUTPUT_FILE - CSV to write to, defaults to stdout"""
    reader = csv.DictReader(input_file)
    all_rows = [d for d in reader]
    if field not in reader.fieldnames:
        logger.error('Field "%s" not present in CSV', field)
        sys.exit(1)
    all_strs = [row[field] for row in all_rows]

    writer = csv.DictWriter(output_file, reader.fieldnames + ['_group'])
    writer.writeheader()

    technique = getattr(techniques, technique)
    groups = technique.cluster_groups(all_strs, eps, min_samples)

    # invert the groups for quick lookup
    group_lookup = {element: ident for ident, elements in groups.items()
                    for element in elements}

    next_group_id = len(groups)
    for row in all_rows:
        key = technique.transform(row[field])
        if key not in group_lookup:
            group_lookup[key] = next_group_id
            next_group_id += 1

        row['_group'] = group_lookup[key]
        writer.writerow(row)
