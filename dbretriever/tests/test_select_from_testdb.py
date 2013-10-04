#This file is part of dbretriever.    The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import unittest

from sql import Table
import dbretriever as db


class TestSelect(unittest.TestCase):
    '''Requisites:
    * running postgres db on localhost
    *   (or other but update connection dict)
    * testdb database with cars table
    *   (or other but update connection dict and query)
    * user information should be updated inside connection dict

    '''
    item = 'Audi'
    query = Table('cars').select()
    connection = {
        'name': 'test_pool',
        'server_type': 'postgres',
        'details': {
            'database': 'testdb',
            'user': 'stma',
        }
    }

    def test_select_cursor(self):
        @db.fetch_data_from(self.connection)
        def test_fv(data, query):
            return data.fetchone()

        row = test_fv(query = self.query)
        assert row[1] == self.item, \
            'wrong data: orig|{}, got|{}'.format(self.item, row[1])

    def test_select_fatch_all(self):
        @db.fetch_data_from(self.connection)
        def test_fv(data, query):
            return data.fetchall()

        rows = test_fv(query = self.query)
        assert len(rows) == 3, "wrong data length"
        assert rows[0][1] == self.item, \
            'wrong data: orig|{}, got|{}'.format(self.item, rows[0][1])

    def test_select_to_specified_variable(self):
        @db.fetch_data_from(self.connection, into='d')
        def test_fv(d, query):
            return d.fetchall()

        rows = test_fv(query = self.query)
        assert len(rows) == 3, "wrong data length"
        assert rows[0][1] == self.item, \
            'wrong data: orig|{}, got|{}'.format(self.item, rows[0][1])
