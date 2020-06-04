from datetime import datetime
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from config import database_uri
db = SQLAlchemy()

database_path = database_uri

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    return db

### Association Table Declaration

genres_venues = db.Table('genres_venues',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
)

genres_artists = db.Table('genres_artists',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
)

### Model Declaration

class Genre(db.Model):
  __tablename__ = "Genre"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

  def __repr__(self):
      return f'<ID: {self.id}, NAME: {self.name}'


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())
  
    # 'genres' describes many to many relationship between Venue-(Parent) and Genre-(Child) by an association table `genres_venues`
    genres = db.relationship('Genre', secondary=genres_venues, backref=db.backref('venues'), lazy=True)


    # 'shows' describes one to many relationship between Venue-(Parent) and Show-(Child)
    ## Most Recent shows are shown first by adding 
    # order_by='desc(Show.start_time) in 
    # Past Shows & Upcoming Shows section of venues/<int:venue_id> endpoint
    shows = db.relationship('Show', backref=db.backref('venues', lazy=True), order_by='desc(Show.start_time)')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - DONE
    def __repr__(self):
      return f'<ID: {self.id}, NAME: {self.name}, CITY & STATE: {self.city},{self.state}, ADDRESS: {self.address},\
      PHONE: {self.phone}, IMAGE_LINK: {self.image_link}, FACEBOOK_LINK: {self.facebook_link}, WEBSITE: {self.website},\
      SEEKING TALENT: {self.seeking_talent}, SEEKING DESCRIPTION: {self.seeking_description}'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())

    # 'genres' describes many to many relationship between Artist-(Parent) and Genre-(Child) by an association table `genres_artists`
    genres = db.relationship('Genre', secondary=genres_artists, backref=db.backref('artists'), lazy=True)


    # 'shows' describes one to many relationship between Artist-(Parent) and Show-(Child)
    ## Most Recent shows are shown first by adding 
    # order_by='desc(Show.start_time) in 
    # Past Shows & Upcoming Shows section of artists/<int:artist_id> endpoint
    shows = db.relationship('Show', backref=db.backref('artists', lazy=True), order_by='desc(Show.start_time)')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - DONE

    def __repr__(self):
      return f'<ID: {self.id}, NAME: {self.name}, CITY & STATE: {self.city},{self.state}, PHONE: {self.phone},\
      IMAGE_LINK: {self.image_link}, FACEBOOK_LINK: {self.facebook_link}, WEBSITE: {self.website},\
      SEEKING VENUE: {self.seeking_venue}, SEEKING DESCRIPTION: {self.seeking_description}'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. - DONE

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
  
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),  nullable=False)
  
  def __repr__(self):
      return f'<ID: {self.id}, START TIME: {self.start_time}, ARTIST ID: {self.artist_id}, VENUE ID: {self.venue_id}'