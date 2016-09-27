import csv
import logging
import sys


logger = logging.getLogger(__name__)


def read_rows(input_file, expected_fields):
    reader = csv.DictReader(input_file)
    all_rows = [d for d in reader]

    for field in expected_fields:
        if field not in reader.fieldnames:
            logger.error('Field "%s" not present in CSV', field)
            sys.exit(1)
    return all_rows, reader


def read_csv_write_header(input_file, output_file, expected_fields,
                          header=None):
    all_rows, reader = read_rows(input_file, expected_fields)
    if header is None:
        header = reader.fieldnames
    elif callable(header):
        header = header(reader.fieldnames)

    writer = csv.DictWriter(output_file, header)
    writer.writeheader()

    return all_rows, writer
