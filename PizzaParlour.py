from flask import Flask
#import Item, Order
from flask import request, session

from flask import Blueprint

# The bluebrint for every backend request currently.
# Should probably be moved to another file/split up as number and complexity of requests grow.
# Also the name 'Assignment 2' maybe shouldn't be used here?
bp = Blueprint('Assignment 2', __name__)

from Order import OrderFactory
from Data import Data
from Product import Product, Pizza, Drink
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

@bp.route('/cancel_order/<int:order_id>')
def cancel_order(order_id):
    ''' Returns a description of the order with the given id
    '''

    return order_fac.cancel_order(order_id)

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

@bp.route('/update_drink/<update_type>', methods = ['POST'])
def update_drink(update_type):
    ''' Edits the item indicated in the update_type way using the provided data.
    '''

    if request.method == 'POST':
        order_number = request.form.get('order_number',type=int)
        item_number = request.form.get('item_number',type=int)
        drink_brand = request.form.get('drink_brand',type=str)
        return order_fac.update_item(order_number, item_number, update_type, drink_brand)

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
        if len(toppings) == 0:
            toppings = None
        items = []
        for i in range(0, int(quantity)):
            print(toppings)
            items.append(Pizza(pizza_type, 0, pizza_size, toppings))
            
        return(order_fac.add_to_order(order_number, items))

@bp.route('/get_data/<data_type>')
def get_data(data_type):
    ''' Returns a list of the specified type. Can be 'pizza_type', 'sizes', 'prices'.
    '''

    if data_type == 'pizza_types':
        return Data.getInstance().get_pizza_to_toppings()
    if data_type == 'pizza_sizes':
        return Data.getInstance().get_size_qualifier()
    if data_type == 'prices':
        return Data.getInstance().get_prices_dict()
    else:
        return ["Not a valid datatype. Try 'pizza_type', 'sizes', or 'prices'."]

@bp.route('/set_price', methods = ['POST'])
def set_price():
    ''' Returns a list of the specified type. Can be 'pizza_type', 'sizes', 'prices'.
    '''

    if request.method == 'POST':
        product_name = request.form.get('product_name',type=str)
        price = request.form.get('price',type=float)
        
        if Data.getInstance().set_price(product_name,price):
            Data.getInstance().update_all()
            order_fac.update_totals()
            return product_name+"'s price set to "+str(price)
        else:
            return "Failure to set "+product_name+"'s price to "+str(price)
@bp.route('/create_drink', methods = ['POST'])
def create_drink():
    ''' Edits the item indicated in the update_type way using the provided data.
    '''

    if request.method == 'POST':
        order_number = request.form.get('order_number',type=int)
        quantity = request.form.get('quantity',type=int)
        drinks = request.form.getlist('drinks',type=str)
        items = []
        for i in range(0, int(quantity)):
            items.append(Drink("drink", 0, drinks[i]))
            
        return(order_fac.add_to_order(order_number, items))

@bp.route('/remove_item', methods = ['POST'])
def remove_item():
    ''' Edits the item indicated in the update_type way using the provided data.
    '''

    if request.method == 'POST':
        order_number = request.form.get('order_number',type=int)
        item_number = request.form.get('item_number',type=int)
        return(order_fac.remove_item(order_number, item_number))


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
