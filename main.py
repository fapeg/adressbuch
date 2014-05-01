from flask import Flask, render_template, g, flash, redirect
import sqlite3
import datetime, hashlib, os, re
from flask.ext.wtf import Form
from flask.ext.login import LoginManager
from wtforms import TextField, BooleanField
from wtforms.validators import Required



app = Flask(__name__)
app.config['SECRET_KEY'] = 'jHgFtjjGFdE5678ijbDDegh'
app.config.from_object('config')

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = TextField('password', validators = [Required()]) 
	
    remember_me = BooleanField('remember_me', default = False)


DATABASE = 'adressen.sqlite' 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def hello_world(): 
    db = get_db()
    cur = db.execute('select vorname, name, titel, strasse, plz, ort, geburtsdatum, festnetz, mobil, email, homepage, twitter from daten order by id desc')
    entries = cur.fetchall()
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