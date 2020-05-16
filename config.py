import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Heroku DB URI
heroku_database_uri ='postgres://aerczexxbnwueh:86a424d6bdfe3c38512e3b09bf2385868cce9c0ffc5555cddf603584118407b5@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d34pitgiibc309'
# Local DB Details
database_name = "fyyur_heruko"
username = "postgres"
password = 'skr123'
local_database_path = "postgres://{}:{}@{}/{}".format(username, password, 'localhost:5432', database_name)
# Database connection string
SQLALCHEMY_DATABASE_URI = heroku_database_uri
# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
