import os

from eralchemy import render_er
from flask import Flask, render_template, request, redirect, url_for, flash , session
import sqlite3
import graphviz

import requests
from sqlalchemy.testing import db

app = Flask(__name__)
app.secret_key = "secret_key"  # Used for flash messages

DATABASE = 'User_Validation.db'
# WEATHER = 'weather.db'
# API_KEY = 'your_openweathermap_api_key'
# BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# city = 'chennai'
# response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
# print(response)
def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        role TEXT,
                        place TEXT
                    )''')
    # conn1 = sqlite3.connect(WEATHER)
    # cursor = conn1.cursor()
    conn.commit()
    conn.close()


@app.route('/',methods=['GET', 'POST'])
def index():
    """Display all records."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items , names=items[1], values=items[0])



@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Add a new record."""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['place']
        role = request.form['role']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, place,role) VALUES (?, ?, ?)", (name, description,role))
        conn.commit()
        conn.close()

        flash("Item added successfully!")
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    """Edit an existing record."""
    print("id-val",id)

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['place']
        role = request.form['role']
        cursor.execute("UPDATE items SET name = ?, place = ?, role = ? WHERE id = ?", (name, description,role, id))
        conn.commit()
        conn.close()
        flash("Item updated successfully!")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    item = cursor.fetchone()
    conn.close()
    if item[2] == 'Admin' or item[2] == 'admin':
        msg = 'You are eligible to edit the records'
        return render_template('edit.html', item=item,msg = msg)
    else:
        flash("You are not eligible to edit ... only allow for Admin ")
        return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    """Delete a record."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    delete_access = cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    delete_access = cursor.fetchone()
    print("delete_access : ",delete_access)
    if delete_access[2] == 'Admin' or delete_access[2] == 'admin':
        cursor.execute("DELETE FROM items WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        flash('You are eligible to delete the records')
        flash("Item deleted successfully!")
        redirect(url_for('index'))
    else:
        flash("You are not eligible to edit ... only allow for Admin ")
        return redirect(url_for('index'))
    return redirect(url_for('index'))

def generate_erd():
    """Generate ERD for the SQLite database."""
    if not os.path.exists(DATABASE):
        print("Database file does not exist. Initializing database...")
        init_db()

    output_file = "erd_diagram.png"
    render_er(f"sqlite:///{DATABASE}", output_file)
    print(f"ERD diagram saved as {output_file}")

if __name__ == '__main__':
    init_db()
    # generate_erd()
    app.run(debug=True)
