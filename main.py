# −*−coding:utf−8−*−   
# Autor: Giulia Kirstein, Daniel Gros, Fabian Pegel
# Mai 2014
# Projektseminar Angewandte Informationswissenschaft                      
from flask import Flask, render_template, g, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, desc
import datetime, hashlib, os, re
from flask.ext.wtf import Form
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import Required, EqualTo, Length
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
    
class SearchForm(Form): 
    searchfield = TextField('searchfield', validators = [Required(u"Bitte Feld ausfüllen!")])



class LoginForm(Form):
    username = TextField('username', validators = [Required("Bitte einen Benutzernamen eingeben!")])
    password = PasswordField('password', validators = [Required("Bitte ein Passwort eingeben!")]) 
    remember_me = BooleanField('remember_me', default = False)

class ChangePassForm(Form):
    password_old = PasswordField('password_old', validators = [Required("Bitte altes Passwort eingeben!")])
    password1    = PasswordField('password1', validators = [Required("Bitte ein neues Passwort eingeben!"), Length(min=8, message=u"Passwort muss mindestens 8 Zeichen lang sein!")]) 
    password2    = PasswordField('password2', validators = [Required("Bitte ein neues Passwort eingeben!"), EqualTo('password1', message=u'Passwörter müssen übereinstimmen!')])


@app.route('/')
def hello_world(): 
    searchform = SearchForm(csrf_enabled=False)
    entries=Entry.query.with_entities(Entry.vorname,Entry.name,Entry.titel, Entry.strasse,Entry.plz,Entry.ort,Entry.geburtsdatum,Entry.festnetz,Entry.mobil,Entry.email,Entry.homepage,Entry.twitter) 
    return render_template('anzeige.htm', entries=entries, searchform=searchform)   
	

@app.route('/profile', methods = ['GET', 'POST'])
def profile(): 
    searchform = SearchForm(csrf_enabled=False)
    passwordform = ChangePassForm()
    if passwordform.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        if user is not None and user.passwort == hashlib.md5(passwordform.password_old.data).hexdigest():
            neues_pw = hashlib.md5(passwordform.password1.data).hexdigest()
            query = text("UPDATE benutzer SET passwort=:passwort WHERE username=:username")
            db.engine.execute(query, username=session['username'], passwort=neues_pw)
            flash(u"Passwörter geändert!", 'accept')
        else:
            flash("Altes Passwort ist falsch!",'error')
        
    return render_template('profile.htm', searchform=searchform, passwordform=passwordform)   
 
   
   
@app.route('/search', methods = ['GET', 'POST'])
def search(): 
    searchform = SearchForm(csrf_enabled=False)
    if request.args['searchfield']:
        begriff = request.args['searchfield']
        begriff_trunk = '%'+begriff+'%'
        query = text("SELECT vorname,name,titel,strasse,plz,ort,geburtsdatum,festnetz,mobil,email,homepage,twitter FROM daten WHERE (vorname  || ' ' || name like :begriff_trunk) or vorname like :begriff_trunk or name like :begriff_trunk or strasse like :begriff_trunk or ort like :begriff_trunk or plz like :begriff_trunk or geburtsdatum like :begriff_trunk or homepage like :begriff_trunk or twitter like :begriff_trunk or mobil like :begriff_trunk or festnetz like :begriff_trunk or email like :begriff_trunk;")
        searchentries = db.engine.execute(query, begriff_trunk=begriff_trunk)
    else:
        return redirect('/')
    return render_template('search.htm', searchform=searchform, begriff=begriff, searchentries=searchentries)    
 

@app.route('/edit', defaults={'id': None})
@app.route('/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    form = EditForm()
    searchform = SearchForm(csrf_enabled=False)
    entries = Entry.query.with_entities(Entry.id, Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort, Entry.geburtsdatum, Entry.festnetz, Entry.mobil, Entry.email, Entry.homepage,Entry.twitter).order_by(desc(Entry.id))
    if id is not None:
        if form.validate_on_submit():
            # text funktion escapet den string
            query = text("UPDATE daten SET vorname=:vorname, name=:name, titel=:titel,strasse=:strasse, plz=:plz, ort=:ort, geburtsdatum=:geburtsdatum, festnetz=:festnetz, mobil=:mobil, email=:email, homepage=:homepage, twitter=:twitter where id=:userid ;")
            flash("Eintrag bearbeitet!", 'accept')
            
            db.engine.execute(query, vorname=form.vorname.data, name=form.name.data, titel=form.titel.data, strasse=form.strasse.data, plz=form.plz.data, ort=form.ort.data, geburtsdatum=form.geburtsdatum.data, festnetz=form.festnetz.data, mobil=form.mobil.data, email=form.email.data, homepage=form.homepage.data, twitter=form.twitter.data, userid=form.userid.data)
            
        entries = Entry.query.filter_by(id=id).with_entities(Entry.id, Entry.vorname,Entry.name,Entry.titel,Entry.strasse,Entry.plz,Entry.ort, Entry.geburtsdatum, Entry.festnetz, Entry.mobil, Entry.email, Entry.homepage,Entry.twitter).first()
    return render_template('edit.htm', entries=entries, id=id , form=form, searchform=searchform)  



@app.route('/new', methods = ['GET', 'POST'])
@login_required
def new():
    searchform = SearchForm(csrf_enabled=False)
    form = EditForm()
    if form.validate_on_submit():
        query = text("INSERT INTO daten ('id','vorname','name','titel','strasse','plz','ort','geburtsdatum','festnetz','mobil','email','homepage','twitter') VALUES (NULL, :vorname,:name,:titel,:strasse,:plz,:ort,:geburtsdatum,:festnetz,:mobil,:email,:homepage,:twitter);")
        db.engine.execute(query, vorname=form.vorname.data, name=form.name.data, titel=form.titel.data, strasse=form.strasse.data, plz=form.plz.data, ort=form.ort.data, geburtsdatum=form.geburtsdatum.data, festnetz=form.festnetz.data, mobil=form.mobil.data, email=form.email.data, homepage=form.homepage.data, twitter=form.twitter.data)
        flash("Eintrag wurde angelegt!", 'accept')
        return redirect('/edit')
    else:
        return render_template('new.htm', form=form, searchform=searchform)
    
    

@app.route('/delete/<id>')
@login_required
def delete(id):
    if id is not None:
        query = text("DELETE FROM daten WHERE id = :id;")
        db.engine.execute(query, id=id)
        flash(u"Benutzer mit der ID " + str(id) + u" gelöscht!", 'accept')
        return redirect('/edit')

	
@app.route('/login', methods = ['GET', 'POST']) 
def login():
    searchform = SearchForm(csrf_enabled=False)
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
            flash('Herzlich Willkommen, '+session['username']+'!', 'accept')
            return redirect('/')
        else:
            flash('Benutzername oder Passwort falsch!', 'error')

    return render_template('login.htm', 
        title = 'Sign In',
        form = form, searchform=searchform)
        
@app.route('/logout')
def logout():
    if session['username']:
        session.pop('username', None)
    logout_user()
    return redirect('/login')

        
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')     