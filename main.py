# −*−coding:utf−8−*−   
# Autor: Giulia Kirstein, Daniel Gros, Fabian Pegel
# Mai 2014
# Projektseminar Angewandte Informationswissenschaft                      
from flask import Flask, render_template, g, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime, hashlib, os, re
from flask.ext.wtf import Form
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import Required
from flask.ext.login import login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jHgFtjjGFdE5678ijbDDegh'
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adressen.sqlite'
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)


class User(db.Model):
  # Setting the table name and
  # creating columns for various fields
  __tablename__ = 'benutzer' 
  id = db.Column('id', db.Integer, primary_key=True)
  verknuepfte_daten_id = db.Column(db.Integer)
  passwort = db.Column(db.String(100))
  username = db.Column(db.String(200))
  def is_authenticated(self):
      return True

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def get_id(self):
      return unicode(self.id)

  def __repr__(self):
      return '<User %r>' % (self.username)
  
  def __init__(self, id, verknuepfte_daten_id, passwort, username):
      # Initializes the fields with entered data
      # and sets the published date to the current time
      self.id = id
      self.verknuepfte_daten_id = verknuepfte_daten_id
      self.passwort = passwort
      self.username = username
	  
	  
	  
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

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
	  

class EditForm(Form):
    userid =      TextField('userid')
    vorname = TextField('vorname', validators = [Required(u"Bitte Feld ausfüllen!")])
    name = TextField('name', validators = [Required(u"Bitte Feld ausfüllen!")])
    titel = TextField('titel')
    strasse = TextField('strasse')
    plz = TextField('plz')
    ort = TextField('ort')
    geburtsdatum = TextField('geburtsdatum')
    festnetz = TextField('festnetz')
    mobil = TextField('mobil')
    email = TextField('email')
    homepage = TextField('homepage')
    twitter = TextField('twitter')    



class LoginForm(Form):
    username = TextField('username', validators = [Required("Bitte einen Benutzernamen eingeben!")])
    password = PasswordField('password', validators = [Required("Bitte ein Passwort eingeben!")]) 
    remember_me = BooleanField('remember_me', default = False)



@app.route('/')
def hello_world(): 
	entries=Entry.query.with_entities(Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort,Entry.geburtsdatum,Entry.festnetz,Entry.mobil,Entry.email,Entry.homepage,Entry.twitter)       
	return render_template('anzeige.htm', entries=entries)   
	
    

@app.route('/edit', defaults={'id': None})
@app.route('/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    form = EditForm()
    entries = Entry.query.with_entities(Entry.id, Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort, Entry.geburtsdatum, Entry.festnetz, Entry.mobil, Entry.email, Entry.homepage,Entry.twitter)
    if id is not None:
        if form.validate_on_submit():
            # text funktion escapet den string
            query = text("UPDATE daten SET vorname=:vorname, name=:name, titel=:titel,strasse=:strasse, plz=:plz, ort=:ort, geburtsdatum=:geburtsdatum, festnetz=:festnetz, mobil=:mobil, email=:email, homepage=:homepage, twitter=:twitter where id=:userid ;")
            flash("Eintrag bearbeitet!")
            
            db.engine.execute(query, vorname=form.vorname.data, name=form.name.data, titel=form.titel.data, strasse=form.strasse.data, plz=form.plz.data, ort=form.ort.data, geburtsdatum=form.geburtsdatum.data, festnetz=form.festnetz.data, mobil=form.mobil.data, email=form.email.data, homepage=form.homepage.data, twitter=form.twitter.data, userid=form.userid.data)
            
        entries = Entry.query.filter_by(id=id).with_entities(Entry.id, Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort, Entry.geburtsdatum, Entry.festnetz, Entry.mobil, Entry.email, Entry.homepage,Entry.twitter).first()
    return render_template('edit.htm', entries=entries, id=id , form=form)  

		
@app.route('/delete/<id>')
@login_required
def delete(id):
    if id is not None:
        query = text("DELETE FROM daten WHERE id = :id;")
        db.engine.execute(query, id=id)
        flash(u"Benutzer mit der ID " + str(id) + u" gelöscht!")
        return redirect('/edit')

	
@app.route('/login', methods = ['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #        flash('Login requested for user="' + form.username.data + '", remember_me=' + str(form.remember_me.data))
        p_username = form.username.data
        p_password = form.password.data
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        user = User.query.filter_by(username=p_username).first()
        if user is not None and user.passwort == hashlib.md5(p_password).hexdigest():
            session['username']=user.username
            login_user(user, remember = remember_me)
            return redirect('/')
        else:
            flash('Benutzername oder Passwort falsch!')

    return render_template('login.htm', 
        title = 'Sign In',
        form = form)
        
@app.route('/logout')
def logout():
    if session['username']:
        session.pop('username', None)
    logout_user()
    return redirect('/login')

        
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')     