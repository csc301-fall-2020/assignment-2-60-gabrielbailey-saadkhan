from flask import Flask
#import Item, Order
from flask import jsonify, request, session, redirect

app = Flask("Assignment 2")

# SQLAlchemy implementation
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #Sets the url of the database
#app.config["SQLALCHEMY_ECHO"] = True #Sets if all queries are printed
db = SQLAlchemy(app)

class Order(db.Model):
    '''An order to a pizza parlor.
    Attributes:
        id: the order number
        price: the total price of the order
    '''

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id

class Item(db.Model):
    '''An order to a pizza parlor.
    Attributes:
        id: the internal id of the Item
        price: the price of the item
    '''

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id

db.create_all()
db.session.commit()

@app.route('/pizza')
def welcome_pizza():
    ''' A route for testing. Use to confirm feedback.
    '''

    return 'Welcome to Pizza Planet!'

@app.route('/create_order', methods=(['POST']))
def create_order():
    ''' Creates a new order with the attributes given in request.form.
    Attributes:
        -price: the total price of the order
    '''
    if request.method == 'POST':
        order_price = request.form.get('price',type=float) #.getlist('name[]')
        new_order = Order(price=order_price)
        #print('op:'+str(order_price)) #debugging line
        try:
            db.session.add(new_order)
            db.session.commit()

            ''' Code for printing all current orders
            porders = Order.query.order_by(Order.id).all()
            for por in porders:
                print(por.id, por.price)'''

            return 'New order is: id '+str(new_order.id)+', price '+str(order_price)
        except:
            return 'Issue with adding order'


    '''price = request.values #???
    print(price)
    newOrd = Order(1, price)
    order_num += 1
    orders.append(newOrd)'''

    return 'No new order'

@app.route('/delete_order/<int:id>', methods=(['POST']))
def delete_order(id):
    ''' Deletes an order with the id given in the request's url.
    Example: deleting order 4
        /delete_order/4
        result: the order with id 4 is deleted
        returns 'Order 4 deleted'
    '''
    if request.method == 'POST':
        order_to_delete = Order.query.get_or_404(id)

        try:
            db.session.delete(order_to_delete)
            db.session.commit()
            
            #print(order_to_delete.id, order_to_delete.price) #debug line; prints deleted order's info

            return 'Order '+str(id)+' deleted'
        except:
            return 'Issue with deleting order'

    return 'No new order'

if __name__ == "__main__":
    app.run()#debug=True
