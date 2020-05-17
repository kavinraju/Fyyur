import os
from env_file import heroku_database_uri_env
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Heroku DB URI
heroku_database_uri = 'postgres://itcgjeasbwgnwz:c74ab4555756357392b84e8dbb2c1ff5cb5c966bc3ab26ec91109848aa32feda@ec2-35-171-31-33.compute-1.amazonaws.com:5432/das9nsemk1dr9f'
# Local DB Details
database_name = "fyyur_heruko"
username = "postgres"
password = 'skr123'
local_database_path = "postgres://{}:{}@{}/{}".format(username, password, 'localhost:5432', database_name)
# Database connection string
SQLALCHEMY_DATABASE_URI = heroku_database_uri
# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
