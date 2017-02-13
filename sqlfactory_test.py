import io
from unittest import TestCase

from sqlfactory import value_formatter, column_formatter, csv2sql


class Csv2SqlTests(TestCase):
    def test_should_convert_csv_to_sql_insert(self):
        csv = io.StringIO('one.text,a.integer,other.float,$date,[iam.null]\n'
                          '"nice text",999,9.99,2017-12-25,,')

        statement = csv2sql(csv)

        self.assertEqual(["INSERT INTO TABLE(one_text, a_integer, other_float, date, iam_null) "
                          "VALUES('nice text', 999, 9.99, '2017-12-25', NULL);"], statement)


class ColumnFormatterTests(TestCase):
    def test_swap_dots_with_underlines(self):
        self.assertEqual('nice_column', column_formatter('nice.column'))

    def test_swap_spaces_with_underlines(self):
        self.assertEqual('nice_column', column_formatter('nice column'))

    def test_omit_special_characters(self):
        self.assertEqual('column', column_formatter('[column$]'))


class ValueFormatterTests(TestCase):
    def test_convert_to_int(self):
        self.assertEqual('123', value_formatter('123'))

    def test_convert_to_float(self):
        self.assertEqual('1.99', value_formatter('1.99'))

    def test_convert_to_string(self):
        self.assertEqual("'James'", value_formatter('James'))

    def test_convert_to_NULL(self):
        self.assertEqual("NULL", value_formatter(''))
