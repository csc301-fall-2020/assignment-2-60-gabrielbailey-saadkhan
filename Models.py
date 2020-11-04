# SQLAlchemy implementation
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Make sure that all database models are imported after db is defined to avoid circular import issues
from Order import Order

from Item import Item

def init_db(db):
    ''' Causes the db to use the data models in Models.py
    '''
    db.create_all()
    db.session.commit()
