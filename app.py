from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import time
import os
from flask import Flask, flash, g, jsonify, redirect, render_template, request, url_for, abort
import re

app = Flask(__name__)

DATABASE = 'data.db'

def get_db_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS place104 (
                id INTEGER PRIMARY KEY,
                place STRING,
                time STRING
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS place105 (
                id INTEGER PRIMARY KEY,
                place STRING,
                time STRING
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS place106 (
                id INTEGER PRIMARY KEY,
                place STRING,
                time STRING
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS place (
                id INTEGER PRIMARY KEY,
                place STRING,
                time STRING
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signdata (
                id INTEGER PRIMARY KEY,
                firstname STRING,
                lastname STRING,
                username STRING,
                password STRING
            )
        ''')

init_db()

@app.route('/')
def sign():
    return render_template('sign.html')

@app.route('/area')
def area():
    return render_template('area.html')

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            with get_db_connection() as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO signdata (firstname, lastname, username, password) VALUES (?, ?, ?, ?)", (firstname, lastname, username, password))
                con.commit()
        except sqlite3.IntegrityError as e:
            return render_template('signup.html', error="A user with that username already exists.")
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM signdata WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                return redirect(url_for('index'))
            else:
                error = 'Invalid username or password'
    return render_template('sign.html', error=error)

@app.route('/index')
def index():
    with get_db_connection() as con:
        cursor = con.cursor()
        places = {}
        for name in ['104', '105', '106']:
            cursor.execute(f"SELECT place FROM place{name} ORDER BY id DESC LIMIT 1")
            place = cursor.fetchone()
            places[name] = place['place'] if place else '未知'
    return render_template('index.html', places=places)

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/data/place104')
def data_place104():
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM place104')
        data = cursor.fetchall()
        data_list = [{'id': row[0], 'place': row[1], 'time' : row[2]} for row in data]
    return jsonify(data_list)

@app.route('/data/place105')
def data_place105():
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM place105')
        data = cursor.fetchall()
        data_list = [{'id': row[0], 'place': row[1], 'time' : row[2]} for row in data]
    return jsonify(data_list)

@app.route('/data/place106')
def data_place106():
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM place106')
        data = cursor.fetchall()
        data_list = [{'id': row[0], 'place': row[1], 'time' : row[2]} for row in data]
    return jsonify(data_list)

@app.route('/update_data')
def update_data():
    data = {'message': 'Data updated'}
    return jsonify(data)

@app.route('/see')
def see():
    try:
        con = sqlite3.connect(DATABASE)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM place104')
        data = cursor.fetchall()
        data_list = [{'id': row[0], 'place': row[1], 'time' : row[2]} for row in data]
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'Error': str(e)})

@app.route('/get/data/<string:place>')
def getd(place):
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    
    cursor.execute("INSERT INTO place (place, time) VALUES (?, ?)", (place, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
    con.commit()
    con.close()
    return 'OK'

@app.route('/get/data/<string:place>/<string:name>/<string:where>')
def getdata(place, name, where):
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    
    realplace = ''
    
    if place == 'A' :
        realplace = '房間'
    if place == 'B' :
        realplace = '餐廳'
    if place == 'C' :
        realplace = '危險區域'
    
    if where == '1':
        if name == '104':
            cursor.execute("INSERT INTO place104 (place, time) VALUES (?, ?)", (realplace, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
            con.commit()
        elif name == '105':
            cursor.execute("INSERT INTO place105 (place, time) VALUES (?, ?)", (realplace, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
            con.commit()
        elif name == '106':
            cursor.execute("INSERT INTO place106 (place, time) VALUES (?, ?)", (realplace, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
            con.commit()
    elif where == '0':
        if name == '104':
            cursor.execute("INSERT INTO place104 (place, time) VALUES (?, ?)", (('離開了' + realplace), datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
            con.commit()
        elif name == '105':
            cursor.execute("INSERT INTO place105 (place, time) VALUES (?, ?)", (('離開了' + realplace), datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
            con.commit()
        elif name == '106':
            cursor.execute("INSERT INTO place106 (place, time) VALUES (?, ?)", (('離開了' + realplace), datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
            con.commit()
    con.close()
    return 'OK'

if __name__ == '__main__' :
    app.run(debug=True, host='0.0.0.0', port=10000)