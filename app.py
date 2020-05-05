#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
mirgrate = Migrate(app, db)

# TODO: connect to a local postgresql database - DONE

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Following the Rubrics:
# Code is decoupled into relevant parts across the files to construct a well-organized code base.
from models import * 

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  # Adding locale='en' in format_datetime() solved: AttributeError: 'NoneType' object has no attribute 'days'
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue. DONE
  
  # Querying all the venues
  venues = Venue.query.all()

  # Initializations
  data = []
  city_and_state = set() # to uniquely identify the city and state

  # Looping over `venues` to uniquely identify the city and state
  for venue in venues:
    city_and_state.add( (venue.city, venue.state) )

  # Looping over `city_and_state` to display venues based on City and State
  for place in city_and_state:
    list_of_venues = []
    
    # Aggregating venues for each `city_and_state` combination
    for venue in venues:
      if( venue.city == place[0] and venue.state == place[1]):
        list_of_venues.append({
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': 0
        })

    # Data to be sent
    data.append({
      'city':place[0],
      'state': place[1],
      'venues': list_of_venues
      }
    )

  ## DATA STRUCTURE ##
  """ data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }] """
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # DONE
  
  # Storing the search text into search_term
  search_term=request.form.get('search_term', '').strip()
  # Querying for the venues
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term.lower() + '%')).all()

  # Initializations
  data = []

  for venue in venues:

    # Getting the shows of the `venue`
    shows = venue.shows
    num_upcoming_shows = 0

    # Looping over shows to find the number of upcoming shows
    for show in shows:
      if datetime.today() <= show.start_time:
        num_upcoming_shows+=1

    # Add to `data` dictionary
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_upcoming_shows
    })

  # Data to be sent
  response={
    "count": len(venues),
    "data": data
  }

  ## DATA STRUCTURE ##
  """ response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }"""
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # DONE

  # Querying for the venue with `venue_id`
  venue = Venue.query.get(venue_id)
  # Storing the shows of the venue with `venue_id`
  shows = venue.shows # returns list [] of Show objects

  # initializations
  genres = []
  past_shows = []
  upcoming_shows = []
  past_shows_count = 0
  upcoming_shows_count = 0

  # Iterating shows[] list to separate the upcoming and past shows
  for show in shows:
    if datetime.today() >= show.start_time:
      past_shows_count+=1
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artists.name,
        "artist_image_link": show.artists.image_link,
        "start_time": format_datetime(str(show.start_time))
      })
    else:
      upcoming_shows_count+=1
      upcoming_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artists.name,
        "artist_image_link": show.artists.image_link,
        "start_time": format_datetime(str(show.start_time))
      })

  # Iterating the genres list to get the name of the genre
  for genre in venue.genres:
    genres.append(genre.name)
  
  # Data to be sent
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  ## DATA STRUCTURE ##
  """ data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0] """
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead. DONE
  # TODO: modify data to be the data object returned from db insertion DONE
  
  # Get the instance of the form
  venueForm = VenueForm(request.form)
  
  # Initializations
  error_occured = False

  if venueForm.validate():

    try:
      name = venueForm.name.data
      city = venueForm.city.data
      state = venueForm.state.data
      address = venueForm.address.data
      phone = venueForm.phone.data
      genres = venueForm.genres.data
      image_link = venueForm.image_link.data
      facebook_link = venueForm.facebook_link.data
      website = venueForm.website.data
      seeking_talent = venueForm.seeking_talent.data
      seeking_description = venueForm.seeking_description.data

      # Create a Venue object to insert into DB
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone,image_link=image_link,
      facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)

      # Create a Genre object to insert into DB
      for genre in genres:
        genre_in_db = Genre.query.filter_by(name=genre).one_or_none()

        # Add `genre` into db only if it's not in Genre table
        if genre_in_db:
          venue.genres.append(genre_in_db)
        else:
          new_genre = Genre(name=genre)
          db.session.add(new_genre)
          venue.genres.append(new_genre)
        
      db.session.add(venue)
      db.session.commit()
      print('Successful added the venue - ', name)
    except Exception as e:
      error_occured = True
      print('Error occured in creating the venue - ', name, '\n', e)
      db.session.rollback()
    finally:
      db.session.close()
  else:
    flash('Validation Failed!')

  if error_occured:
    # TODO: on unsuccessful db insert, flash an error instead. DONE
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database DONE

  # Querying all the artists
  artists = Artist.query.all()

  # Initializations
  data = []

  # Looping over `artists` to store the required data, which has to be sent
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  ## DATA STRUCTURE ##
  """ data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }] """
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # DONE

  # Storing the search text into search_term
  search_term=request.form.get('search_term', '').strip()

  # Querying for the artists
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term.lower() + '%')).all()

  # Initializations
  data = []

  for artist in artists:

    # Getting the shows of the `artist`
    shows = artist.shows
    num_upcoming_shows = 0

    # Looping over shows to find the number of upcoming shows
    for show in shows:
      if datetime.today() <= show.start_time:
        num_upcoming_shows+=1
    
    # Add to `data` dictionary
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_shows
    })

  # Data to be sent
  response={
    "count": len(artists),
    "data": data
  }

  ## DATA STRUCTURE ##
  """ response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  } """
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # DONE

  # Querying for the artist with `artist_id`
  artist = Artist.query.get(artist_id)
  # Storing the shows of the artist with `artist_id`
  shows = artist.shows # returns list [] of Show objects

  # initializations
  genres = []
  past_shows = []
  upcoming_shows = []
  past_shows_count = 0
  upcoming_shows_count = 0

  # Iterating shows[] list to separate the upcoming and past shows
  for show in shows:
    if datetime.today() > show.start_time:
      past_shows_count+=1
      past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venues.name,
        "venue_image_link": show.venues.image_link,
        "start_time": format_datetime(str(show.start_time))
      })
    else:
      upcoming_shows_count+=1
      upcoming_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venues.name,
        "venue_image_link": show.venues.image_link,
        "start_time": format_datetime(str(show.start_time))
      })

  # Iterating the genres list to get the name of the genre
  for genre in artist.genres:
    genres.append(genre.name)
  
  # Data to be sent
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  ## DATA STRUCTURE ##
  """ data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  } """
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead. DONE
  # TODO: modify data to be the data object returned from db insertion. DONE 

  # Get the instance of the form
  artistForm = ArtistForm(request.form)
  
  # Initializations
  error_occured = False

  if artistForm.validate():  
    try:
      name = artistForm.name.data
      city = artistForm.city.data
      state = artistForm.state.data
      phone = artistForm.phone.data
      genres = artistForm.genres.data
      image_link = artistForm.image_link.data
      facebook_link = artistForm.facebook_link.data
      website = artistForm.website.data
      seeking_venue = artistForm.seeking_venue.data
      seeking_description = artistForm.seeking_description.data

      # Create a Venue object to insert into DB
      artist =  Artist(name=name, city=city, state=state, phone=phone,image_link=image_link,
      facebook_link=facebook_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)

      # Create a Genre object to insert into DB
      for genre in genres:
        genre_in_db = Genre.query.filter_by(name=genre).one_or_none()
        
        # Add `genre` into db only if it's not in Genre table
        if genre_in_db:
          artist.genres.append(genre_in_db)
        else:
          new_genre = Genre(name=genre)
          db.session.add(new_genre)
          artist.genres.append(new_genre)

      db.session.add(artist)
      db.session.commit()
      print('Successful added the artist - ', name)
    except Exception as e:
      error_occured=True
      print('Error occured in creating the artist - ', name, '\n', e)
      db.session.rollback()
    finally:
      db.session.close()
  else:
    flash('Validation Failed!')

  if error_occured:
    # TODO: on unsuccessful db insert, flash an error instead. DONE
    flash('An error occurred. Artist ' + artistForm.name.data + ' could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Artist ' + artistForm.name.data + ' was successfully listed!')
  
  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # DONE

  # .desc() is called to show the most recent show first in /shows.
  shows = Show.query.order_by(Show.start_time.desc()).all()

  # Initializations
  data = []

  for show in shows:
    
    # Getting the venue details using backref of Venue
    venue = show.venues
    # Getting the artist details using backref of Artist
    artist = show.artists

    start_time = format_datetime(str(show.start_time))

    data.append({
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": start_time
    })

  ## DATA STRUCTURE ##
  """ data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }] """
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # DONE

  # Get the instance of the form
  showForm = ShowForm(request.form)
  
  # Initializations
  error_occured=False

  if showForm.validate():

    try:
      artist_id = showForm.artist_id.data
      venue_id = showForm.venue_id.data
      start_time = showForm.start_time.data

      # Create a Show object to insert into DB
      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
      print('Successfully added the Show at ', start_time)
    except Exception as e:
      error_occured = True
      print('Error occured in creating the show - ', '\n', e)
      db.session.rollback()
    finally:
      db.session.close()
  else:
    flash('Please try again! Enter a valid input.')
    return redirect(url_for('index'))

  if error_occured:
    # TODO: on unsuccessful db insert, flash an error instead. DONE
    flash('An error occurred. Show could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return redirect(url_for('index'))

@app.route('/shows/search', methods=['POST'])
def search_shows():

  # Storing the search text into search_term
  search_term=request.form.get('search_term', '').strip()

  # Querying for the venues
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term.lower() + '%')).all()
  
  # Initializations
  response = []

  # Iterate over venues to find the shows
  for venue in venues:
    
    # Getting the shows of the `venue`
    shows = venue.shows

    # Looping over `shows` to get the details of the venue and artist of the particular `show`
    for show in shows:

      # flag to have a track id the `show` is an upcoming show or not
      is_upComingShow  = False
      
      if datetime.today() <= show.start_time:
        # update `is_upComingShow` to True if the  `show` is an upcoming show
        is_upComingShow = True
      
      # Adding the required data to update the Front-End
      response.append({
        "venue_id": show.venues.id,
        "venue_name": show.venues.name,
        "venue_image_link": show.venues.image_link,
        "artist_id": show.artists.id,
        "artist_name": show.artists.name,
        "is_upComingShow": is_upComingShow,
        "start_time": format_datetime(str(show.start_time))
      })

  ## DATA STRUCTURE ##
  """ response = [{
    "venue_id": 4,
    "venue_name": 'Tamil Sangam',
    "venue_image_link": 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    "artist_id": 1,
    "artist_name": 'Kavin Raju',
    "is_upComingShow": True,
    "start_time": "2019-05-21T21:30:00.000Z"
  },{
    "venue_id": 4,
    "venue_name": 'Tamil Sangam',
    "venue_image_link": 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    "artist_id": 1,
    "artist_name": 'Kavin Raju',
    "is_upComingShow": True,
    "start_time": "2019-05-21T21:30:00.000Z"
  }] """

  return render_template('pages/search_shows.html', results=response, search_term=request.form.get('search_term', ''))


#  Error Handler
#  ----------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
