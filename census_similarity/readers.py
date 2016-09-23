from collections import namedtuple
import csv
import os


FIELDS_FILE = os.path.join('ARTS_DB_Extract', 'vars.csv')


Field = namedtuple('Field', ('id', 'name', 'description', 'dataset_ids'))


def read_columns(filename=None):
    filename = filename or FIELDS_FILE
    with open(filename) as f:
        for row in csv.DictReader(f):
            yield Field(row['id'], row['vname'], row['vdesc'],
                        row['dsids'].split(','))
