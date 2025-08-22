""" Here goes the code to connect to the database and perform CRUD operations. We used the SQLAlchemy library to connect to the database and to extract data from it. SQLAlchemy is a SQL toolkit and Object Relational Mapper (ORM) for Python. It is a library that allows us to interact with the database using Python code. It is a wrapper around the database driver. It is a layer of abstraction that allows us to interact with the database using Python code instead of SQL queries. It is a ORM because it allows us to interact with the database using Python objects instead of SQL queries.

We did a version check to ensure that we are using the correct version of SQLAlchemy. The version number is stored in the __version__ attribute of the sqlalchemy module. 

We used the create_engine function to create a new database engine. The create_engine function takes a database URL as an argument. The database URL is a string that specifies the database driver, the database name, the database user, the database password, and the database host. The database driver is the library that allows us to connect to the database. The database name is the name of the database. The database user is the user that we use to connect to the database. The database password is the password that we use to connect to the database. The database host is the host that we use to connect to the database.

We can use a connection string from MariaDB, of the type:
mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4
taken from (https://docs.sqlalchemy.org/en/21/dialects/mysql.html#mariadb-support) and adapt it to our case. IT HAS BEEN ADAPTED BY ADDING THE PORT NUMBER JUST AFTER THE HOST NAME. @some_mariadb:PORTNUMBER/dbname?charset=utf8mb4

database.py cannot be included in the future repository, as it contains sensitive information.

We import text from sqlalchemy to be able to use the text function to execute raw SQL queries. engine.connet() is used to create a connection to the database. The connection is used to execute SQL queries. The connection is closed after the queries are executed. 

"conn" is an alias for the connection (engine.connect()).
Anything we wrtie inside the "with" token will be executed inside the connection. Once out of the "with" token required indentation, the connection will be closed automatically.

So we craft a very basic query in a "result" object, and then we print it. The connection did NOT work, so we add a connect_args parameter to the create_engine function to allow the connection to the database. The connection_args parameter is a dictionary that specifies the connection arguments. The connection arguments are the arguments that we use to connect to the database. 

connect_args={
    "ssl": {
        "ca": "/home/gord/client-ssl/ca.pem",
        "cert": "/home/gord/client-ssl/client-cert.pem",
        "key": "/home/gord/client-ssl/client-key.pem",
    }
},

From aivencloud documentation, we get:
import pymysql

timeout = 10
connection = pymysql.connect(
  charset="",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="joviancareers",
  host="mysql-fcc-db-fcc-webapp-python-flask.k.aivencloud.com",
  password="",
  read_timeout=timeout,
  port=,
  user="",
  write_timeout=timeout,
)

try:
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
  cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
  cursor.execute("SELECT * FROM mytest")
  print(cursor.fetchall())
finally:
  connection.close()

It seems we have a connection timeout problem. Considering that replit public IP is (for now) 104.196.34.59, we need to add it to the allowed IP list in Aivencloud. And with port number, correct db name, and ssl certificate, the connection works and the query is succeessful. It also works without any ssl certificate. It also works with total IP range 0.0.0.0/0. So we can use the connection string without any ssl certificate.

Now, analyzing the types we obtained CursorResult and Row objects, we want to convert them in basic dictionaries and lists. We cannot use dict(Row) because it does not work anymore in the latest version of sqlalchemy 2.x. So we need to use a different approach, so the mappings() function is used to map the Row object to a dictionary. The mappings() function takes a Row object as an argument and returns a dictionary. The dictionary is a basic Python dictionary.

In order to manipulate a result object, you have to repeat the query, because result and result_all get wasted after the first use. That's why we used result2 = conn.execute(text("select * from jobs")) to repeat the query and then we used result2.mappings().all() to get a list of RowMapping, immutable dictionaries, each dictionary-like is a row from the database.

The we converted the list of RowMapping to a list of dictionaries using a list comprehension. The list comprehension is a way to create a new list by applying an expression to each item in an existing list. The expression is applied to each item in the existing list, and it was dict(row) for row in rows. The result is a list of dictionaries, this time they are modifiable.

IT IS IMPORTANT TO UNDERSTAND THAT YOU CANNOT CONVERT ROW OBJECTS INTO FULL DICTIONARIES, BUT YOU CAN CONVERT ROWMAPPING OBJECTS INTO FULL DICTIONARIES, STARTING FROM ROW OBJECTS, CONVERTING THEM INTO ROWMAPPING OBJECTS USING listofRowMapping= listofrows.mappings().all(), AND THEN CONVERTING THEM INTO DICTIONARIES with list_of_dict = [dict(row) for row in listofrows].

The big problem we have with this file, database.py, is that it contains sensitive information, so it cannot be included in the future repository. So we need to create a new secret inside replit, and then we need to use it in the code. We can use the replit secrets manager to store sensitive information. The replit secrets manager is a way to store sensitive information in replit. After adding a sectret (for example the connection string in the value section of the secret), we can use it in the code using the os module. The os module is a way to interact with the operating system. The syntax to use a secret is os.environ['SECRET_NAME']. In this case, the secret name is DB_CONNECTION_STRING.

And by using urlparse() function from urllib.parse module, we can parse the secret AIVEN connection string and extract the host, port, user, password, and database name. So now we can connect safely to the database by using both sqlalchemy and pymysql libraries.

TODO: Solve the mystery of the SSL certificate. Aivencloud documentation says that we need to use a SSL certificate to connect to the database, but it seems that we don't need it. We need to investigate this issue.

load_job_from_db(id) is a function that takes an id as an argument and returns a single job from the database. The function uses the text function to execute raw SQL queries. The function uses the engine object to create a connection to the database. :val is the syntax to use a parameter in a raw SQL query. STRANGE: text("SELECT * FROM jobs WHERE id = :val"), {"val": id}) works, but text("SELECT * FROM jobs WHERE id = :val"), val=id) returns an error :
"No overloads for "execute" match the provided arguments Argument types: (TextClause, Unknown)". As a matter of fact it accepts a second parameter, but in the form of a dictionary, not a single variable.

In documentation, the signature of the method is:
method sqlalchemy.engine.Connection.execute(statement: Executable, parameters: _CoreAnyExecuteParams | None = None, *, execution_options: CoreExecuteOptionsParameter | None = None) -> CursorResult[Any] 

parameters: parameters which will be bound into the statement. This may be either a dictionary of parameter names to values, or a mutable sequence (e.g. a list) of dictionaries. When a list of dictionaries is passed, the underlying statement execution will make use of the DBAPI cursor.executemany() method. When a single dictionary is passed, the DBAPI cursor.execute() method will be used.

The benefit of having a database which is separated from the code because the code is deployed (on render) independently from the database, the database can be changed and data just changes independently from the code. So we can have a database which is used by multiple applications, at the same time, and the data is shared between them.

In the function add_application_to_db(job_id,application), we use the text function to execute raw SQL queries. The function uses the engine object to create a connection to the database. The function uses the connection to execute SQL queries.
conn.execute() requires fundamentally two parameters: the query, and a dictionary of parameters. The query is a string, and the dictionary of parameters is a dictionary of key-value pairs. The keys are the names of the parameters in the query, and the values are the values in the dictionary.

WARNING: The developer in the tutorial use a configuration/version of SQLAlchemy in which autocommit is enabled by default. In the latest version of SQLAlchemy, autocommit is disabled by default. So we need to use the begin() method to start a transaction, and end it as well.
"""

import sqlalchemy
from sqlalchemy import create_engine, text
import os
from sqlalchemy.engine import URL
from typing import cast
from urllib.parse import unquote, urlparse
import pymysql

def add_application_to_db(job_id, application):
  #with engine.connect() as conn:
   with engine.begin() as conn:
    query = text("INSERT INTO applications(job_id, full_name,         email, linkedin_url, education, working_experience,               resume_url) VALUES(:job_id, :full_name, :email,                   :linkedin_url, :education, :working_experience, :resume_url)")
    
    conn.execute(query, {"job_id": job_id, "full_name":               application['full_name'], "email": application['email'],          "linkedin_url": application['linkedin_url'], "education":         application['education'], "working_experience":                   application['working_experience'], "resume_url":                  application['resume_url']})

def load_jobs_from_db():
  with engine.connect() as conn:
      result = conn.execute(text("select * from jobs"))
      rows = result.mappings().all()
      jobs = [dict(row) for row in rows]
      return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
      result = conn.execute(
        text("SELECT * FROM jobs WHERE id = :val"), {"val":            id})
      rows = result.mappings().all()
      jobs = [dict(row) for row in rows]
      if len(rows)!=0 :
        return jobs[0]
      else:
        return None


print(sqlalchemy.__version__)

db_connection_string = os.environ['DB_CONNECTION_STRING']
engine = create_engine(db_connection_string,
                       connect_args={
                         "ssl": {
                           "ssl_ca": "/etc/ssl/ca.pem"
                         }
                       })

with engine.connect() as conn:
  result = conn.execute(text("select * from jobs"))
  #A CursorResult object
  print("type(result): ", type(result))
  result_all = result.all()
  #A basic Python list, but of Row objects
  print("type(result_all): ", type(result_all))
  # Here we cannot use result.all() anymore, we have already     called it once, so the  cursor is "consumed".
  print("result.all(): ", result_all)
  first_result = result_all[0]
  #A Row object
  print("type(first_result): ", type(first_result))
  #A basic Python dictionary, it does not work anymore in the    latest version of sqlalchemy 2.x.
  #first_result_dict = dict(result_all[0])
  #print("type(first_result_dict): ", type(first_result_dict))
  #print(first_result_dict)
  
  #This is a list of dictionaries, each dictionary is a row      from the database.
  #Object of type "RowMapping" is not callable
  #first_result_dict = result_all[0]._mapping().all()
  #Cannot access member "mapping" for type                       "Sequence[Row[Any]]" Member "mapping" is unknown

  #rows = result_all.mapping().all()
  #print("type(rows): ", type(rows))
  #print(len(rows))
  
  #Cannot access member "mappings" for type                      #"Sequence[Row[Any]]"   Member "mappings" is unknown
  #rows = result_all.mappings().all()
  result2 = conn.execute(text("select * from jobs"))
  #list of "RowMapping", each dictionary is a row from the       database.
  rows = result2.mappings().all()
  list_of_dict = [dict(row) for row in rows]
  print("type(rows): ", type(rows))
  print("type(rows[0]): ", type(rows[0]))
  print(rows[0])
  print("type(list_of_dict): ", type(list_of_dict))
  print("Printing all the rows:")
  #Printing every single RowMapping (dict-like object)
  for row in rows:
    print(row)
  #Printing the single keys
  rows[0].keys()
  #Printing the rows directly as full dictionaries
  print("Printing the rows directly as full dictionaries:")
  [print(list_of_dict) for row in list_of_dict]


#from pymysql.cursors import DictCursor
timeout = 10
db_connection_uri = os.environ['DB_CONNECTION_URI_AIVEN']

# Parse the URL
#create() is wrong here, it is used to assemble pieces of a URL, not to parse it.
#urlparse() is used to parse a URL
#url = URL.create(db_connection_uri)
#url = urlparse(db_connection_uri)
#url = URL.create(db_connection_string)

url = urlparse(db_connection_uri)

#PARSED AND NOW WORKING
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  db="joviancareers",
  host=url.hostname,
  password= cast(str, url.password),
  read_timeout=timeout,
  port= cast(int, url.port),
  user=url.username,
  write_timeout=timeout,
)

try:
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM jobs")
  print(cursor.fetchall())
finally:
  connection.close()

