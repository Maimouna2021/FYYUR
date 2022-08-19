#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from pprint import pprint
import re
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from model import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment  = Moment(app)
migrate = Migrate(app, db)

db.create_all()

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
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
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = Venue.query.distinct(Venue.city, Venue.state).all()
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = ''
  data = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  return render_template('pages/search_venues.html', results=data, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = db.session.query(Venue).filter(Venue.id == venue_id).first()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  name                 = request.form['name']
  city                 = request.form['city'] 
  state                = request.form['state']
  address              = request.form['address']
  phone                = request.form['phone']
  phone                = re.sub('\D', '', phone)
  genres               = request.form['genres']
  image_link           = request.form['image_link']
  facebook_link        = request.form['facebook_link']
  website_link         = request.form['website_link']
  seeking_talent       = True if 'seeking_talent' in request.form else False
  seeking_description  = request.form['seeking_description']
  new_venue = Venue( 
    name =  name, 
    city = city, 
    state = state, 
    address = address, 
    phone = phone, 
    genres = genres, 
    image_link = image_link, 
    facebook_link = facebook_link,
    seeking_talent = seeking_talent, 
    website_link =  website_link, 
    seeking_description = seeking_description
  ) 
  try:
    db.session.add(new_venue) 
    db.session.commit() 
    flash('Venue enregistré avec succés')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' impossible d\'enregistré.')
    return url_for('/forms/new_venue.html')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
  finally:
    db.session.close()
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = ''
  data = db.session.query(Artist).filter(Artist.name.ilike('%' + search_term + '%')).all()
  return render_template('pages/search_artists.html', results=data, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = db.session.query(Artist).filter(Artist.id == artist_id).first()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  if form.validate_on_submit():
    artist                      = db.session.query(Artist).filter(Artist.id == artist_id).first()
    artist.name                 = form.name.data
    artist.city                 = form.city.data
    artist.state                = form.state.data
    artist.phone                = form.phone.data
    artist.genres               = form.genres.data
    artist.facebook_link        = form.facebook_link.data
    artist.image_link           = form.image_link.data
    artist.website              = form.website.data
    artist.seeking_venue        = form.seeking_venue.data
    artist.seeking_description  = form.seeking_description.data
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' est modifier avec succés!')
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' n\'a pas été modifier!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  if form.validate_on_submit():
    venue                      = db.session.query(Venue).filter(Venue.id == venue_id).first()
    venue.name                 = form.name.data
    venue.city                 = form.city.data
    venue.state                = form.state.data
    venue.phone                = form.phone.data
    venue.genres               = form.genres.data
    venue.facebook_link        = form.facebook_link.data
    venue.image_link           = form.image_link.data
    venue.website              = form.website.data
    venue.seeking_talent       = form.seeking_talent.data
    venue.seeking_description  = form.seeking_description.data
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' Modifier avec succés')
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' n\'a pas été modifier!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  name                 = request.form['name']
  city                 = request.form['city'] 
  state                = request.form['state']
  phone                = request.form['phone']
  phone                = re.sub('\D', '', phone)
  genres               = request.form['genres']
  facebook_link        = request.form['facebook_link']
  image_link           = request.form['image_link']
  website_link         = request.form['website_link']
  seeking_venue        = True if 'seeking_venue' in request.form else False
  seeking_description  = request.form['seeking_description']
  new_artists = Artist( name =  name, city = city, state = state, phone = phone, genres = genres, facebook_link = facebook_link, image_link = image_link,  website_link =  website_link, seeking_venue=seeking_venue, seeking_description = seeking_description) 
  try:
    db.session.add(new_artists) 
    db.session.commit()
    flash('Artist' + request.form['name'] + 'est enrégistré avec succés') 
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' n\'a pas été d\'enregistré.')
    return url_for('/forms/new_artist.html')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = Show.query.all()
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
  artist_id   = request.form['artist_id']
  venue_id    = request.form['venue_id']
  start_time  = request.form['start_time']
  show = Show(
    artist_id=artist_id,
    venue_id=venue_id,
    start_time=start_time
  )
  try:
    db.session.add(show)
    db.session.commit()
    
    flash('Show ajouter avec succés!')
  except:
    db.session.rollback()
    flash('Une erreur c\'est produit')
  return render_template('pages/home.html')

@app.route('/show/search')
def search_show():
  return render_template('pages/show.html')


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
