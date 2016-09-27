import sys

import click

from census_similarity.io import read_csv_write_header, read_rows


@click.command()
@click.argument('input_file', required=False, type=click.File('rt'),
                default=sys.stdin)
@click.argument('output_file', required=False, type=click.File('rt'),
                default=sys.stdout)
@click.option('--lookup-file', type=click.File('rt'))
@click.option('--replacement-field')
@click.option('--id-field', default='id')
@click.option('--name-field', default='name')
def lookup(input_file, output_file, lookup_file, replacement_field, id_field,
           name_field):
    """
    INPUT_FILE - CSV to read from, defaults to stdin
    OUTPUT_FILE - CSV to write to, defaults to stdout"""
    all_rows, writer = read_csv_write_header(
        input_file, output_file, [replacement_field])

    lookup = {}
    lookup_rows, _ = read_rows(lookup_file, [id_field, name_field])
    for row in lookup_rows:
        key = row[id_field]
        name = row[name_field]
        lookup[key] = name

    for row in all_rows:
        ids = [i.strip() for i in row[replacement_field].split(',')]
        names = [lookup.get(i, '') for i in ids]
        row[replacement_field] = ','.join(names)
        writer.writerow(row)
