# −*−coding:utf−8−*−   
# Autor: Giulia Kirstein, Daniel Gros, Fabian Pegel
# Mai 2014
# Projektseminar Angewandte Informationswissenschaft                      
from flask import Flask, render_template, g, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime, hashlib, os, re
from flask.ext.wtf import Form
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField
from wtforms.validators import Required



app = Flask(__name__)
app.config['SECRET_KEY'] = 'jHgFtjjGFdE5678ijbDDegh'
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/fabian/adressbuch/adressen.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
  # Setting the table name and
  # creating columns for various fields
  __tablename__ = 'benutzer' 
  id = db.Column('id', db.Integer, primary_key=True)
  verknuepfte_daten_id = db.Column(db.Integer)
  passwort = db.Column(db.String(100))
  username = db.Column(db.String(200))
  
  def __init__(self, id, verknuepfte_daten_id, passwort, username):
      # Initializes the fields with entered data
      # and sets the published date to the current time
      self.id = id
      self.verknuepfte_daten_id = verknuepfte_daten_id
      self.passwort = passwort
      self.username = username

class Entry(db.Model):
  # Setting the table name and
  # creating columns for various fields
  __tablename__ = 'daten' 
  id = db.Column('id', db.Integer, primary_key=True)
  vorname = db.Column(db.String(200))
  name = db.Column(db.String(200))
  titel = db.Column(db.String(200))
  strasse = db.Column(db.String(200))
  plz = db.Column(db.Integer)
  ort = db.Column(db.String(200))
  geburtsdatum = db.Column(db.String(200))
  festnetz = db.Column(db.String(200))
  mobil = db.Column(db.String(200))
  email = db.Column(db.String(200))
  homepage = db.Column(db.String(200))
  twitter = db.Column(db.String(200))
  
  
  
  def __init__(self, id, vorname, nachname, titel, strasse, plz, ort, geburtsdatum, festnetz, mobil, email, homepage, twitter):
      # Initializes the fields with entered data
      # and sets the published date to the current time
      self.id = id
      self.vorname = vorname
      self.name = name   
      self.titel = titel
      self.strasse = strasse
      self.plz = plz
      self.ort = ort
      self.geburtsdatum = geburtsdatum
      self.festnetz = festnetz
      self.mobil = mobil
      self.email = email
      self.homepage = homepage
      self.twitter = twitter
	  


class LoginForm(Form):
    username = TextField('username', validators = [Required("Bitte einen Benutzernamen eingeben!")])
    password = TextField('password', validators = [Required("Bitte ein Passwort eingeben!")]) 
	
    remember_me = BooleanField('remember_me', default = False)



@app.route('/')
def hello_world(): 
	entries=Entry.query.with_entities(Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort,Entry.geburtsdatum,Entry.festnetz,Entry.mobil,Entry.email,Entry.homepage,Entry.twitter)    
	return render_template('anzeige.htm', entries=entries) 
	
	
	
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user="' + form.username.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/')
    return render_template('login.htm', 
        title = 'Sign In',
        form = form)
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')     