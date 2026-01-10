"""
Database connection utility module
Handles MySQL connection using Flask-MySQLdb
"""
from flask import g
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def init_db(app):
    """Initialize MySQL connection with Flask app"""
    app.config['MYSQL_HOST'] = Config.MYSQL_HOST
    app.config['MYSQL_USER'] = Config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = Config.MYSQL_DB
    mysql.init_app(app)

def get_db():
    """Get MySQL cursor for executing queries"""
    if 'db' not in g:
        g.db = mysql.connection.cursor()
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()
