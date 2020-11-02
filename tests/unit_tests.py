from PizzaParlour import app, Order, db

#from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db'

context = app.app_context()
context.push()

#db = SQLAlchemy(app)
#db.create_all()
#db.session.commit()

def test_pizza():
    '''Tests if there is a repsonse given'''
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

def test_create():
    '''Tests if the create_order works with a price given'''

    #app.test_client.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db' # can't do after creation

    order = Order(price=3.5)
    #print(order.id)
    db.session.add(order) #make transaction to add order to the database
    db.session.flush() #Actually do it, updating order's id to the next id value
    #print(order.id)
    db.session.delete(order) #make transaction to delete order from the database
    db.session.flush() #Actually do it, order stays the same though
    #print(order.id)
    #assert Order.query.count() > 0

    response = app.test_client().post('/create_order', data=dict(id=order.id, price=order.price)) #crucial line: queries test server for response
    db.session.delete(order) #make transaction to delete the new order from the database
    db.session.flush() #Actually do it

    assert response.status_code == 200
    assert response.data == ('New order is: id '+str(order.id)+', price '+str(order.price)).encode('utf-8')
    #assert response.data == b'New order is: id 3, price 3.5'

    db.session.rollback() # does nothing, flush autocommits, and commit autoflushes (on sqlite)