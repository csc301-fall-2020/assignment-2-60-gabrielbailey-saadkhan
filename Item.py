import Models
class Item(db.Model):
    '''An item in an order.
    Attributes:
        id: the internal id of the Item
        price: the price of the Item
    '''
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10))

    __mapper_args__ = {
        'polymorphic_identity':'item',
        'polymorphic_on':type
    }

    def __repr__(self):
        return '<Item %r: $%r>' % self.id, self.price

# These should be their own tables, with relevent pizza and drink attributes pointing into a table entry. They need to be updateable.
p_types = ['Pepperoni', 'Margherita', 'Vegetarian', 'Neapolitan']
p_toppings = ['olives', 'tomatoes', 'mushrooms', 'jalapenos', 'chicken', 'beef', 'pepperoni']
d_types = {'Coke':1.50, 'Diet Coke':1.60, 'Coke Zero':1.40, 'Pepsi':1.50, 'Diet Pepsi':1.40, 'Dr. Pepper':1.50, 'Water':0.0, 'Juice':1.00}

class Pizza(Item):
    '''The information representing a pizza in an order.
     Includes:
     price
     size
     type
     toppings'''

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    p_type = db.Column(db.Integer, nullable=False)
    toppings = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    type = db.Column(db.String(10))

    __mapper_args__ = {
        'polymorphic_identity':'pizza',
        'polymorphic_on':type
    }

class Drink(Item):
    '''The information representing a pizza in an order'''

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    d_type = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    type = db.Column(db.String(10))

    __mapper_args__ = {
        'polymorphic_identity':'drink',
        'polymorphic_on':type
    }