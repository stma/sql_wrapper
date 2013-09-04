sql_wrapper
===========

Data retriever from relational databases by queries writen in python-sql.
Right now **only for postgre** sql connection.

Requisites
----------

* python 2.7
* python-sql http://code.google.com/p/python-sql/

Usages
------

* defualt usage where you define a query in python-sql and a connection meta dict.
  then use them with fetch\_data\_from decorator on a function you want to have a data from database.
  A cursor on a data will be available in the variable **data** (kw['data'])

```python
from sql import Table
import dbretriever as db

query = Table('cars').select()
connection = {
  'name': 'test_pool',
  'server_type': 'postgres',
  'details': {
    'database':'testdb',
    'user':'stma',
  }
}

@db.fetch_data_from(query, connection)
def test_fv(data):
   pass # change with your code e.g. return data
```

* you can change the behaviour on what will be the name of where you can reach the data, the data will be a cursor or a list of rows

```python
  def fetch_data_from(query, connection, get_cursor = True, default_value = None, into = 'data')
```
* data variable name

```python
@db.fetch_data_from(query, connection, into='d')
def test_fv(d):
  return d
```
* cursor or list

```python
@data_provider(query, connection, get_cursor=False)
def test_fv(data):
  return data
```
* default value (BUG - default value is not used)

```python
@data_provider(query, connection, default_value=[('semmi',)])
def test_fv(data):
  return data
```

Future improvements
-------------------

* BUGFIX default_value
* setup.py for install
* sqlite3 connection
* mysql connection
* mssql connection
