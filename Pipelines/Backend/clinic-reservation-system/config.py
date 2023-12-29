from main import create_app
from flaskext.mysql import MySQL
from os import environ

DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_NAME = environ.get('DB_NAME')
DB_HOST = environ.get('DB_HOST')

print("MYSQL_DATABASE_USER: ", DB_USER)
print("MYSQL_DATABASE_PASSWORD: ", DB_PASS)
print("MYSQL_DATABASE_DB: ", DB_NAME)
print("MYSQL_DATABASE_HOST: ", DB_HOST)

APP = create_app()
mysql = MySQL(APP)

APP.config['MYSQL_DATABASE_USER'] = DB_USER
APP.config['MYSQL_DATABASE_PASSWORD'] = DB_PASS
APP.config['MYSQL_DATABASE_DB'] = DB_NAME
APP.config['MYSQL_DATABASE_HOST'] = DB_HOST

# APP.config['MYSQL_DATABASE_USER'] = 'ahmed'
# APP.config['MYSQL_DATABASE_PASSWORD'] = '123'
# APP.config['MYSQL_DATABASE_DB'] = 'clinicdb'
# APP.config['MYSQL_DATABASE_HOST'] = 'clinic-db-app'
# mysql.init_app(APP)



