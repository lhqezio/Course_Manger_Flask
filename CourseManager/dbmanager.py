import os
import click
from flask import current_app, g
from .db import Database

def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    get_db().run_file(os.path.join(current_app.root_path, "sql", "setup.sql"))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initialized the database")