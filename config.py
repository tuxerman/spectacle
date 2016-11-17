import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database options
CURRENT_DATABASE_TYPE = 'mysql'

# Sqlite options
SQLITE_FILEPATH = 'documents.db'

# MySQL options
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'sriram'
MYSQL_PASSWD = 'password'
MYSQL_DB = 'documents'

# ElasticSearch Options
ES_HOST = '127.0.0.1'
ES_PORT = 9200
ES_INDEX = 'testindex_02'
