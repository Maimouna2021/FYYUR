from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import Flask

app=Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)


class Venue(db.Model):
    __tablename__ = 'venues'

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String)
    city                = db.Column(db.String(100))
    state               = db.Column(db.String(100))
    address             = db.Column(db.String(100))
    phone               = db.Column(db.String(100))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link          = db.Column(db.String(400))
    facebook_link       = db.Column(db.String(100))
    website_link        = db.Column(db.String(100))
    seeking_talent      = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(500))
    show                = db.relationship('Show', backref='Venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'artists'

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String)
    city                = db.Column(db.String(100))
    state               = db.Column(db.String(100))
    phone               = db.Column(db.String(100))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    facebook_link       = db.Column(db.String(100))
    image_link          = db.Column(db.String(400))
    website_link        = db.Column(db.String(100))
    seeking_venue       = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(500))
    show                = db.relationship('Show', backref='Artist', lazy=True)


class Show(db.Model):
    __tablename__ = 'shows'

    id         = db.Column(db.Integer, primary_key=True)
    venue_id   = db.Column(db.Integer, db.ForeignKey(Venue.id))
    artist_id      = db.Column(db.Integer, db.ForeignKey(Artist.id))
    start_time = db.Column(db.DateTime)