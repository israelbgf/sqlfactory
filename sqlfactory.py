import csv
import sys
from collections import OrderedDict

INSERT_STATEMENT = 'INSERT INTO TABLE({0}) VALUES({1});'


def csv2sql(csv_file):
    statements = []

    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        row = convert_to_ordered_dict(row, csv_reader.fieldnames)
        statements.append(INSERT_STATEMENT.format(
            ', '.join(map(column_formatter, row.keys())),
            ', '.join(map(value_formatter, row.values()))))

    return statements


def convert_to_ordered_dict(dict, expected_key_order):
    ordered_dict = OrderedDict()
    for key in expected_key_order:
        ordered_dict[key] = dict[key]
    return ordered_dict


def column_formatter(name):
    name = name.replace('.', '_').replace(' ', '_')
    name = name.replace('[', '').replace(']', '').replace('$', '')
    return name


def value_formatter(value):
    if not value:
        return 'NULL'

    try:
        return str(int(value))
    except ValueError:
        try:
            return str(float(value))
        except ValueError:
            return "'{0}'".format(value)


if __name__ == '__main__':
    for file in sys.argv[1:]:
        print(*csv2sql(open(file, encoding='utf-8')), sep='\n')
