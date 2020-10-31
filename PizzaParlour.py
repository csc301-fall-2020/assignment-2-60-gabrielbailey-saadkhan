from flask import Flask
import Item, Order
from flask import jsonify, request, session, redirect

app = Flask("Assignment 2")

''' SQLAlchemy implementation
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Real, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Real, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id
'''
orders = []

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

@app.route('/neworder', methods=(['POST']))
def create_order():
    order = request.get_json() #???
    newOrd = Order(order['ID'], order['ITEMS'])
    orders.append(newOrd)

    return 'New order is:'+newOrd.id

if __name__ == "__main__":
    app.run()#debug=True
