import Item
from Models import db

class Order(db.Model):
    '''An order to a pizza parlor.
    Attributes:
        id: the order number
        price: the total price of the order
    '''

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    # Note: SQLite doesn't support lists... So I guess we'll just have to set a max number of items in an order and create that many versions of item.

    def __repr__(self):
        return '<Order %r: $%r>' % self.id, self.price

#class Order:
#    '''An order to a pizza parlor'''

#    def __init__(self, id, items):
#        self.id = id
#        self.items = items
