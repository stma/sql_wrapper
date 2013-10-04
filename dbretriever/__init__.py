#This file is part of dbretriever. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

__version__ = '0.1'
__all__ = ['fetch_data_from']

from sql import Select
from functools import wraps


def die_unless_select(query):
    assert isinstance(query, Select), "not a select"


def fetch_data_from(
        connection,
        get_cursor=True,
        default_value=None,
        into='data'):

    def factory(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db_connection = DbConnection.getConnection(connection)
            with db_connection.cursor() as data_pointer:
                query = kwargs.get('query', None)
                die_unless_select(query)
                data_pointer.execute(*tuple(query))
                if get_cursor:
                    kwargs[into] = data_pointer
                else:
                    kwargs[into] = data_pointer.fetchall()
                result = func(*args, **kwargs)
            if db_connection is not None and not db_connection.closed:
                DbConnection.put(connection, db_connection)
            return result
        return wrapper

    return factory


class DbConnection(object):
    POSTGRES = 'postgres'
    SQLITE3 = 'sqlite3'
    __map = {}

    def __init__(self, config):
        self.__configuration = config

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    @staticmethod
    def getConnection(configuration):
        assert isinstance(configuration, dict), \
            'db_conn descriptor is not a dict'
        con_name = configuration['name']
        assert con_name is not None, \
            'db_conn should have name provided with "name" key'
        db_conn = DbConnection.__map.get(con_name, None)
        if not db_conn:
            db_conn = DbConnection(configuration)
            DbConnection.__map[con_name] = db_conn
        return db_conn.connection

    @staticmethod
    def put(configuration, connection):
        assert isinstance(configuration, dict), \
            'db_conn descriptor is not a dict'
        con_name = configuration['name']
        assert con_name is not None, \
            'db_conn should have name provided with "name" key'
        db_conn = DbConnection.__map.get(con_name, None)
        assert db_conn is not None, \
            'db_conn should have been inicialized'
        server_type = configuration['server_type']
        if (server_type == DbConnection.POSTGRES):
            db_conn.__pgsql_pool.putconn(connection)

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
        import psycopg2.pool as pgpool
        if not getattr(self, '_DbConnection__pgsql_pool', None):
            self.__pgsql_pool = pgpool.SimpleConnectionPool(
                1, 5, **self.__configuration['details']
            )
        return self.__pgsql_pool.getconn()

    def create_sqlite2_connection(self, connection_details):
        assert False, 'this connection type has not been implemented yet'
