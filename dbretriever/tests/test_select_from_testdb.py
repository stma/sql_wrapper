#This file is part of dbretriever.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import unittest

from sql import Table
from dbretriever import data_provider

class TestSelect(unittest.TestCase):
  '''Requisites:
  * running postgres db on localhost (or other but update connection dict)
  * testdb database with cars table (or other but update connection dict and query)
  * user information should be updated inside connection dict
  
  '''
  item = 'audi'
  query = Table('cars').select()
  connection = {
    'name': 'test_pool',
    'server_type': 'postgres',
    'details': {
      'database':'testdb',
      'user':'stma',
    }
  }

  def test_select_cursor(self):
    @data_provider(self.query, self.connection)
    def test_fv(*a, **kw):
      return kw['data']
    
    data = test_fv()
    row = data.fetchone()
    assert row[1] == self.item, 'wrong data: orig|{}, got|{}'.format(self.item, row[1])

  def test_select_fatch_all(self):
    @data_provider(self.query, self.connection)
    def test_fv(*a, **kw):
      return kw['data']
    
    data = test_fv()
    rows = data.fetchall()
    assert len(rows) == 1, "wrong data length"
    assert rows[0][1] == self.item, 'wrong data: orig|{}, got|{}'.format(self.item, rows[0][1])

  def test_select_to_specified_variable(self):
    @data_provider(self.query, self.connection, variant_name='d')
    def test_fv(*a, **kw):
      return kw['d']
    
    data = test_fv()
    rows = data.fetchall()
    assert len(rows) == 1, "wrong data length"
    assert rows[0][1] == self.item, 'wrong data: orig|{}, got|{}'.format(self.item, rows[0][1])
