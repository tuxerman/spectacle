import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database options
CURRENT_DATABASE_TYPE = 'mysql'

# Sqlite options
SQLITE_FILEPATH = 'documents.db'

# MySQL options
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = os.environ.get('MYSQL_PORT', 3306)
MYSQL_USER = os.environ.get('MYSQL_USER', 'sriram')
MYSQL_PASSWD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DB_NAME = 'documents'
# AWS RDS overrides
if 'RDS_HOSTNAME' in os.environ:
    MYSQL_DB_NAME = os.environ['RDS_DB_NAME']
    MYSQL_HOST = os.environ['RDS_HOSTNAME']
    MYSQL_PORT = int(os.environ['RDS_PORT'])
    MYSQL_USER = os.environ['RDS_USERNAME']
    MYSQL_PASSWD = os.environ['RDS_PASSWORD']

# ElasticSearch Options
ES_HOST = os.environ.get('ES_HOST', '127.0.0.1')
ES_PORT = os.environ.get('ES_PORT', 9200)
ES_INDEX = 'spectacle_fts_index_dev'

# S3 credentials
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
S3_PDF_BUCKET = 'spectacle-storage-dev1'

# Google recaptcha
RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')
