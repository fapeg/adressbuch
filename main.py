from flask import Flask, render_template, g
import sqlite3
import datetime, hashlib, os, re

app = Flask(__name__)


	
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

if __name__ == '__main__':
	app.debug = True
	app.run()     