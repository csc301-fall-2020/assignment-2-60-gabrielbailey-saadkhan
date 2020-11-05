from flask import Flask
#import Item, Order
from flask import request, session

from Models import db, init_db, Order, Item

from flask import Blueprint

# The bluebrint for every backend request currently.
# Should probably be moved to another file/split up as number and complexity of requests grow.
# Also the name 'Assignment 2' maybe shouldn't be used here?
bp = Blueprint('Assignment 2', __name__)

@bp.route('/pizza')
def welcome_pizza():
    ''' A route for testing. Use to confirm feedback.
    '''

    return 'Welcome to Pizza Planet!'

@bp.route('/create_order', methods=(['POST']))
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

    return 'No new order'

@bp.route('/delete_order/<int:id>', methods=(['POST']))
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

    return 'No order deleted'


def create_app(testing, db_url):
    ''' Creates a flask app and attatches blueprints and database to it.
    testing determines where the db will write to primarily, as well as whether the app is in test mode.
    '''

    app = Flask("Assignment 2")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url #Sets the url of the database
    app.config['TESTING'] = testing
    #app.config["SQLALCHEMY_ECHO"] = True # All queries are printed if True
    db.init_app(app)
    app.app_context().push() # binds db to app

    app.register_blueprint(bp) # adds blueprints to app

    return app


if __name__ == "__main__":
    app = create_app(False, 'sqlite:///pizza.db')

    init_db(db)
    app.run()#debug=True
