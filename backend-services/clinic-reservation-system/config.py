from main import create_app
from flaskext.mysql import MySQL

APP = create_app()
mysql = MySQL(APP)
APP.config['MYSQL_DATABASE_USER'] = 'ahmed'
APP.config['MYSQL_DATABASE_PASSWORD'] = ''
APP.config['MYSQL_DATABASE_DB'] = 'mysql'
APP.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(APP)



