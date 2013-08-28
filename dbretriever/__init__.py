#This file is part of dbretriever.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

__version__ = '0.1'
__all__ = ['data_provider']

from sql import Select, Table
from functools import wraps
import psycopg2 as pg, psycopg2.pool as pgpool

def query_check(fn):
  def wrapper(*args, **kwargs):
    query = args[0] or kwargs['query']
    assert isinstance(query, Select), "not a select"
    return fn(*args, **kwargs)
  return wrapper

@query_check
def data_provider(query, connection, get_cursor = True, default_value = None, variant_name = 'data'):
  def factory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      data_pointer = DbConnection.getConnection(connection).cursor()
      data_pointer.execute(*tuple(query))
      if get_cursor:
        kwargs[variant_name] = data_pointer
      else:
        kwargs[variant_name] = data_pointer.fetchall()
      return func(*args, **kwargs)
    return wrapper
  return factory


class DbConnection:
  POSTGRES = 'postgres'
  SQLITE3 = 'sqlite3'
  __map = {}

  def __init__(self, config):
    self.__configuration = config

  @staticmethod
  def getConnection(configuration):
    assert isinstance(configuration, dict), 'db_conn descriptor is not a dict'
    con_name = configuration['name']
    assert con_name is not None, 'db_conn should have name provided with "name" key'
    db_conn = DbConnection.__map.get(con_name, None)
    if not db_conn:
      db_conn = DbConnection(configuration)
      DbConnection.__map[con_name] = db_conn
    return db_conn.connection

  @property
  def connection(self):
    assert self.__configuration is not None, "no connection defined"
    server_type = self.__configuration['server_type']
    if (server_type == DbConnection.POSTGRES):
      con = self.create_PSQL_connection()
    elif (server_type == DbConnection.SQLITE3):
      con = self.create_sqlite3_connection()
    return con

  def create_PSQL_connection(self):
    if not getattr(self, '__pgsql_pool', None):
      self.__pgsql_pool = pgpool.SimpleConnectionPool(1, 5, **self.__configuration['details'])
    return self.__pgsql_pool.getconn()

  def create_sqlite2_connection(self, connection_details):
    assert False, 'this connection type has not been implemented yet'
