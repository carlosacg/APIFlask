from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://{user}:{password}@{host}/{db}'.format(
                                                                            user = os.environ.get('MYSQL_USER'),
                                                                            password = os.environ.get('MYSQL_USER'),
                                                                            host = os.environ.get('DB_HOST'),
                                                                            db =  os.environ.get('MYSQL_DB'),
                                                                        )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app) 

from controlador import *

if __name__ == '__main__':
    app.run('0.0.0.0',8084,debug=True)