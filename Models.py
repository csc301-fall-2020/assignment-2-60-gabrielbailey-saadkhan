# SQLAlchemy implementation
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    '''An order to a pizza parlor.
    Attributes:
        id: the order number
        price: the total price of the order
    '''

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Order %r: $%r>' % self.id, self.price

class Item(db.Model):
    '''An order to a pizza parlor.
    Attributes:
        id: the internal id of the Item
        price: the price of the item
    '''

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Item %r: $%r>' % self.id, self.price


def init_db(db):
    ''' Causes the db to use the data models in Models.py
    '''
    db.create_all()
    db.session.commit()
