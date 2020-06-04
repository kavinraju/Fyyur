import os
from env_file import *
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Heroku DB URI
heroku_database_uri = os.environ['DATABASE_URL']
# Local DB Details
database_name = database_name_env
username = username_env
password = password_env
local_database_path = "postgres://{}:{}@{}/{}".format(username, password, 'localhost:5432', database_name)
# Database connection string
SQLALCHEMY_DATABASE_URI = heroku_database_uri
# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
