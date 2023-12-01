from main import create_app
from flaskext.mysql import MySQL

APP = create_app()
mysql = MySQL(APP)
APP.config['MYSQL_DATABASE_USER'] = 'ahmed'
APP.config['MYSQL_DATABASE_PASSWORD'] = '123'
APP.config['MYSQL_DATABASE_DB'] = 'clinicdb'
APP.config['MYSQL_DATABASE_HOST'] = 'clinic-db-app'
# mysql.init_app(APP)



