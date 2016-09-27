import sys

import click

from census_similarity.io import read_csv_write_header, read_rows


@click.command()
@click.argument('input_file', required=False, type=click.File('rt'),
                default=sys.stdin)
@click.argument('output_file', required=False, type=click.File('rt'),
                default=sys.stdout)
@click.option('--lookup-file', type=click.File('rt'),
              help='File which contains lookup values')
@click.option('--replacement-field', help='Field to replace ids with')
@click.option('--id-field', default='id',
              help="Field name in lookup-file we'll be replacing")
@click.option('--value-field', default='name',
              help='Field name in lookup-file to replace with')
def lookup(input_file, output_file, lookup_file, replacement_field, id_field,
           value_field):
    """Given a CSV, replace lookup values. The input file should contain a
    column of ids which are explained in the lookup-file. This command will
    replace those ids with names found in the lookup-file.

    \b
    INPUT_FILE - CSV to read from, defaults to stdin
    OUTPUT_FILE - CSV to write to, defaults to stdout"""
    all_rows, writer = read_csv_write_header(
        input_file, output_file, [replacement_field])

    lookup = {}
    lookup_rows, _ = read_rows(lookup_file, [id_field, value_field])
    for row in lookup_rows:
        key = row[id_field]
        value = row[value_field]
        lookup[key] = value

    for row in all_rows:
        ids = [i.strip() for i in row[replacement_field].split(',')]
        values = [lookup.get(i, '') for i in ids]
        row[replacement_field] = ','.join(values)
        writer.writerow(row)
