from flask import Flask
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

mysql = MySQL()

app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['JSON_AS_ASCII'] = False
app.config['MYSQL_DATABASE_USER'] = 'apiuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PassToUserApi'
app.config['MYSQL_DATABASE_DB'] = 'searchandratewords'
app.config['MYSQL_DATABASE_HOST'] = 'gbdb'
mysql.init_app(app)
