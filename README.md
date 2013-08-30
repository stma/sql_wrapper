sql_wrapper
===========

Data retriever from relational databases by queries writen in python-sql.
Right now **only for postgre** sql connection.

Requisites
----------

* python 2.7
* python-sql

Usages
------

* defualt usage where you define a query in python-sql and a connection meta dict.
  then use them with data_provider decorator on a function you want to have a data from database.
  For the appropriate work you have to add \*args and \*\*kw to the parameter list.
  A cursor on a data will be available in the variable **kw['data']**

```python
query = Table('cars').select()
connection = {
  'name': 'test_pool',
  'server_type': 'postgres',
  'details': {
    'database':'testdb',
    'user':'stma',
  }
}

@data_provider(query, connection)
def test_fv(*a, **kw):
   pass # change with your code e.g. return kw['data']
```

* you can change the behaviour on what will be the name of where you can reach the data, the data will be a cursor or a list of rows

```python
  def data_provider(query, connection, get_cursor = True, default_value = None, variant_name = 'data')
```
* data variable name

```python
@data_provider(query, connection, variant_name='d')
def test_fv(*a, **kw):
  return kw['d']
```
* cursor or list

```python
@data_provider(query, connection, get_cursor=False)
def test_fv(*a, **kw):
  return kw['data']
```
* default value

```python
@data_provider(query, connection, default_value=[('semmi',)])
def test_fv(*a, **kw):
  return kw['data']
```

Future improvements
-------------------

* setup.py for install
* sqlite3 connection
* mysql connection
* mssql connection
