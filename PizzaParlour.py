from flask import Flask
#import Item, Order
from flask import request, session

from flask import Blueprint

# The bluebrint for every backend request currently.
# Should probably be moved to another file/split up as number and complexity of requests grow.
# Also the name 'Assignment 2' maybe shouldn't be used here?
bp = Blueprint('Assignment 2', __name__)

from Order import OrderFactory
from Product import Product, Pizza
order_fac = OrderFactory()

@bp.route('/pizza')
def welcome_pizza():
    ''' A route for testing. Use to confirm feedback.
    '''

    return 'Welcome to Pizza Planet!'

@bp.route('/new_order')
def new_order():
    ''' Creates a new empty order. Returns that order's id.
    '''
    
    return order_fac.create_new_order().split()[-1]

@bp.route('/order_is_valid/<int:order_id>')
def order_is_valid(order_id):
    ''' Returns whether or not the given order id is valid.
    '''

    return str(order_fac.is_valid_order_number(order_id) != None)

@bp.route('/get_item/<int:order_id>/<int:item_id>')
def get_item(order_id, item_id):
    ''' Returns an item given its order and its id.
    '''
    
    return order_fac.get_item_in_order_by_id(order_id, item_id)

@bp.route('/get_order/<int:order_id>')
def get_order(order_id):
    ''' Returns a description of the order with the given id
    '''

    return order_fac.get_order(order_id)

@bp.route('/get_order_list')
def get_all_orders():
    ''' Returns a description of all current orders
    '''

    return order_fac.get_order_list()

@bp.route('/create_delivery/<int:order_id>', methods = ['POST'])
def create_delivery(order_id):
    ''' Creates a delivery for the given order id
    '''

    if request.method == 'POST':
        delivery_type = request.form.get('delivery_type',type=str)
        address = request.form.get('address',type=str)
        return order_fac.schedule_delivery(order_id, delivery_type, address)

@bp.route('/item_type/<int:order_id>/<int:item_id>')
def is_pizza(order_id, item_id):
    ''' Returns whether or not the specified item is a pizza.
    '''
    
    return order_fac.is_pizza(order_id, item_id)

@bp.route('/get_toppings/<int:order_id>/<int:item_id>', methods = ['POST'])
def get_toppings(order_id, item_id):
    ''' Returns the toppings of the specified pizza.
    '''

    return order_fac.get_toppings(order_id, item_id)

@bp.route('/update_pizza/<update_type>', methods = ['POST'])
def update_pizza(update_type):
    ''' Edits the item indicated in the update_type way using the provided data.
    '''

    if request.method == 'POST':
        order_number = request.form.get('order_number',type=int)
        item_number = request.form.get('item_number',type=int)
        if update_type == 'type':
            pizza_type = request.form.get(update_type,type=str)
            order_fac.update_item(order_number, item_number, update_type, pizza_type)
        elif update_type == 'size':
            pizza_size = request.form.get('pizza_size',type=str)
            order_fac.update_item(order_number, item_number, update_type, pizza_size)
        elif update_type == 'toppings':
            toppings = request.form.get('toppings',type=list)
            add_or_remove = request.form.get('add_or_remove',type=bool)
            order_fac.update_item(order_number, item_number, update_type, toppings, add_or_remove)

@bp.route('/create_pizza', methods = ['POST'])
def create_pizza():
    ''' Edits the item indicated in the update_type way using the provided data.
    '''

    if request.method == 'POST':
        order_number = request.form.get('order_number',type=int)
        quantity = request.form.get('quantity',type=int)
        pizza_type = request.form.get('pizza_type',type=str)
        pizza_size = request.form.get('pizza_size',type=str)
        toppings = request.form.getlist('toppings',type=str)
        
        items = []
        for i in range(0, int(quantity)):
            items.append(Pizza(pizza_type, 0, pizza_size, toppings))
            
        return(order_fac.add_to_order(order_number, items))


@bp.route('/create_order')
def create_order():
    ''' Creates a new, empty order
    '''
    return order_fac.create_new_order()


def create_app(testing):
    ''' Creates a flask app and attatches blueprints and database to it.
    testing determines where the db will write to primarily, as well as whether the app is in test mode.
    '''

    app = Flask("Assignment 2")
    #app.config['SQLALCHEMY_DATABASE_URI'] = db_url #Sets the url of the database
    app.config['TESTING'] = testing
    #app.config["SQLALCHEMY_ECHO"] = True # All queries are printed if True
    #db.init_app(app)
    #app.app_context().push() # binds db to app

    app.register_blueprint(bp) # adds blueprints to app

    return app


if __name__ == "__main__":
    app = create_app(False)

    #init_db(db)
    app.run()#debug=True
