import os
from os import getenv
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)


app.config['SECRET_KEY'] = getenv('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)
Migrate(app,db)

from cantor_application.login.views import login_blueprint 
from cantor_application.logout.views import logout_blueprint 
from cantor_application.register.views import registration_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(registration_blueprint) 
