import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Heroku DB URI
heroku_database_uri ='postgres://zsfglqnhlmteob:1af5477353d7095d1fa599ed095609bbb2eeb762ac8424d36e38cedc10d92b4f@ec2-54-175-117-212.compute-1.amazonaws.com:5432/d1iafsk3io5bgl'
# Local DB Details
database_name = "fyyur_heruko"
username = "postgres"
password = 'skr123'
local_database_path = "postgres://{}:{}@{}/{}".format(username, password, 'localhost:5432', database_name)
# Database connection string
SQLALCHEMY_DATABASE_URI = heroku_database_uri
# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
