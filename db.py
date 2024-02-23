import sqlite3

# import click
from flask import Flask, g, current_app
# from flask import current_app

# app = Flask(__name__)

from app import app

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql') as f:
            db.executescript(f.read())
            cur = db.cursor()

            cur.execute("INSERT INTO todos (title, description, status, due_to) VALUES (?, ?, ?, ?)",
                        (
                            'Learn Flask', 'connect sqlite db',
                            'pending', '26/2/2024'
                        )
                        )
            db.commit()
            db.close()
