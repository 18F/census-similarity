from collections import defaultdict
import logging
import sys

import click

from census_similarity.io import read_csv_write_header


logger = logging.getLogger(__name__)


@click.command()
@click.argument('input_file', required=False, type=click.File('rt'),
                default=sys.stdin)
@click.argument('output_file', required=False, type=click.File('rt'),
                default=sys.stdout)
@click.option('--group-field', default='_group', help='Field to group on')
@click.option('--accumulation-field', default='id', help='Field to aggregate')
def group_by(input_file, output_file, group_field, accumulation_field):
    """Group CSV rows by the requested fields.

    For example:
    id, other, group
    1, a, A
    2, b, B
    3, c, A

    becomes
    group, id
    A, "1, 3"
    B, 2

    Further, this splits by a comma:
    id, other, group
    "1, 2", a, A
    3, b, B

    generates the same

    INPUT_FILE - CSV to read from, defaults to stdin
    OUTPUT_FILE - CSV to write to, defaults to stdout"""
    all_rows, writer = read_csv_write_header(
        input_file, output_file, [group_field, accumulation_field],
        [group_field, accumulation_field])

    ids_by_group = defaultdict(set)
    for row in all_rows:
        groups = [el.strip() for el in row[group_field].split(',')]
        groups = [g for g in groups if g]
        ids = [el.strip() for el in row[accumulation_field].split(',')]
        for group in filter(bool, groups):
            ids_by_group[group].update(filter(bool, ids))

    for group in sorted(ids_by_group.keys()):
        ids = ','.join(sorted(ids_by_group[group]))
        writer.writerow({group_field: group, accumulation_field: ids})
