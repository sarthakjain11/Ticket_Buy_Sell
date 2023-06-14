from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create app instance
project = None

def create_app():
    project = Flask(__name__, template_folder="templates")
    project.app_context().push()
    return project


project = create_app()

project.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticketdb.sqlite3"
project.config['SECRET_KEY'] = 'my_first_flask_app'

# db instance
db = SQLAlchemy(project)
from application import models, forms, login, controller
