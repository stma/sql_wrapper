sql_wrapper
===========

Data retriever from relational databases by queries writen in python-sql.
Right now **only for postgre** sql connection.

Requisites
----------

* python 2.7
* setup can hadle this (python-sql v0.2 (http://code.google.com/p/python-sql/))

Usages
------

* defualt usage where you define a connection meta dict.
  Then use it with fetch\_data\_from decorator on a function you want to have a data from database. And pass a query in python-sql format to the function you
  have just annotated inside the query parameter. 
  A cursor on a data will be available in the variable **data** (kw['data'])
* please see the test file

Future improvements
-------------------

* BUGFIX default_value
* sqlite3 connection
* mysql connection
* mssql connection
