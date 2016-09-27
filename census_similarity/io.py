import csv
import logging
import sys


logger = logging.getLogger(__name__)


def read_rows(input_file, expected_fields):
    """Read the input_file as a CSV; validate that the expected_fields are
    present. Sys.exit if not
    :return: pair of list of dicts (rows in the CSV), and a list of headers
    found in the input_file"""
    reader = csv.DictReader(input_file)
    all_rows = [d for d in reader]

    for field in expected_fields:
        if field not in reader.fieldnames:
            logger.error('Field "%s" not present in CSV', field)
            sys.exit(1)
    return all_rows, reader.fieldnames


def read_csv_write_header(
        input_file, output_file, expected_fields, header=None):
    """Read the input file as a CSV; validate the expected_fields; transform
    the CSV header and write that to an output_file
    :param header:
        if None, use the input_file's header.
        if a callable, apply it to the input_file's header.
        if a string, append it to the input_file's header (if not present)
        else, assume the header is a sequence of strings
    :return: pair of list of dicts (rows in the CSV), and a csv.DictWriter"""
    all_rows, fieldnames = read_rows(input_file, expected_fields)
    if header is None or (isinstance(header, str) and header in fieldnames):
        header = fieldnames
    elif isinstance(header, str):
        header = fieldnames + [header]
    elif callable(header):
        header = header(fieldnames)

    writer = csv.DictWriter(output_file, header)
    writer.writeheader()

    return all_rows, writer
