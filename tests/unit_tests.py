import unittest
from flask_testing import TestCase
from Order import OrderFactory
#from PizzaParlour import create_app, order_fac
import PizzaParlour as PP
from Product import Pizza, Drink
import json

class PizzaParlourTest(TestCase):
    ''' General testing class copied from flask testing tutorial.
    Should contain all tests of http requests and databases.'''

    def create_app(self):
        # used at the start of the tests in this class to create the app (I think)
        # pass in test configuration
        # Currently using in memory database to be a bit faster. to write to a db use 'tests.db' instead of :memory:
        return PP.create_app(True)

    def setUp(self):
        # Used before every test to set up the database.

        # Maybe add random amount of info in database? Non-deterministic tests sound bad though...

        PP.order_fac = OrderFactory()

    #def tearDown(self):
        # Used after every test to clean up the database.

        #db.session.remove()
        #db.drop_all()

    def test_pizza(self):
        '''Tests if there is a repsonse given'''
        response = self.client.get('/pizza')

        assert response.status_code == 200
        assert response.data == b'Welcome to Pizza Planet!'
    
    def test_new_order(self):
        '''Tests if the new_order gives expected output
        '''

        #assert Order.query.count() > 0
        # Tests if new_order gives 1 as first id
        response = self.client.get('/new_order') #crucial line: queries test server for response
        assert response.status_code == 200
        assert response.data == ('1').encode('utf-8')

        '''
        porders = Order.query.order_by(Order.id).all()
        print(porders)
        for por in porders:
            print(por.id, por.price)
        '''
        # Tests if new_order gives 2 as next id
        response = self.client.get('/new_order') 
        assert response.status_code == 200
        assert response.data == ('2').encode('utf-8')

    def test_order_is_valid(self):
        '''Tests if the order_is_valid gives expected output
        '''

        PP.order_fac.create_new_order()
        PP.order_fac.create_new_order()
        PP.order_fac.create_new_order()

        #assert Order.query.count() > 0

        # Tests if order_is_valid is True for first order
        response = self.client.get('/order_is_valid/1')
        assert response.status_code == 200
        assert response.data == ('True').encode('utf-8')

        # Tests if order_is_valid is False for nonexistent 4th order
        response = self.client.get('/order_is_valid/4')
        assert response.status_code == 200
        assert response.data == ('False').encode('utf-8')

    def test_get_item(self):
        '''Tests if get_item gives expected output
        '''
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(1,[pizza1])
        PP.order_fac.create_new_order()

        # Tests if get_item returns string representation
        response = self.client.get('/get_item/1/1')
        assert response.status_code == 200
        assert response.data == (str(pizza1)).encode('utf-8')

        # Tests if get_item rejects invalid ids
        response = self.client.get('/get_item/3/1')
        assert response.status_code == 200
        assert response.data == ("None").encode('utf-8')
        response = self.client.get('/get_item/1/2')
        assert response.status_code == 200
        assert response.data == ("None").encode('utf-8')

    def test_get_order(self):
        '''Tests if get_order returns info about the right order
        '''
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")
        PP.order_fac.create_new_order()
        
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])

        # Tests if get_order returns vital info, regardless of formatting
        response = self.client.get('/get_order/2')
        assert response.status_code == 200
        assert ("2").encode('utf-8') in response.data
        assert ("pepperoni_pizza").encode('utf-8') in response.data
        assert ("tomatoes").encode('utf-8') in response.data

        # Tests if get_item rejects invalid ids
        response = self.client.get('/get_order/3')
        assert response.status_code == 200
        assert ("3").encode('utf-8') not in response.data
        assert ("valid").encode('utf-8') in response.data

    def test_cancel_order(self):
        '''Tests if cancel_order cancels the right order
        '''

        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")
        PP.order_fac.create_new_order()
        
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])
        PP.order_fac.create_new_order()

        # Tests if cancel_order rejects invalid ids
        response = self.client.get('/cancel_order/4')
        assert response.status_code == 200
        assert ("invalid").encode('utf-8') in response.data

        # Tests if cancel_order removes the order, regardless of formatting
        response = self.client.get('/cancel_order/2')
        assert "invalid" in PP.order_fac.get_order(2)
        assert response.status_code == 200
        assert ("2").encode('utf-8') in response.data

        # Tests if cancel_order rejects invalid ids, including previous ids
        response = self.client.get('/cancel_order/2')
        assert response.status_code == 200
        assert ("invalid").encode('utf-8') in response.data

    def test_get_all_orders(self):
        '''Tests if get_all_orders does as it says, and no more
        '''
        
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")
        PP.order_fac.create_new_order()
        
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])
        PP.order_fac.create_new_order()

        # Tests if it returns all current orders, regardless of formatting
        response = self.client.get('/get_order_list')
        assert response.status_code == 200
        assert ("1 ").encode('utf-8') in response.data
        assert ("2 ").encode('utf-8') in response.data
        assert ("3 ").encode('utf-8') in response.data
        assert ("4 ").encode('utf-8') not in response.data

        # Tests if it continues to work once an order is removed
        PP.order_fac.cancel_order(2)
        response = self.client.get('/get_order_list')
        assert response.status_code == 200
        assert ("1 ").encode('utf-8') in response.data
        assert ("2 ").encode('utf-8') not in response.data
        assert ("3 ").encode('utf-8') in response.data
        assert ("4 ").encode('utf-8') not in response.data

        # Tests if it continues to work once an order is added
        PP.order_fac.create_new_order()
        response = self.client.get('/get_order_list')
        assert response.status_code == 200
        assert ("1 ").encode('utf-8') in response.data
        assert ("2 ").encode('utf-8') not in response.data
        assert ("3 ").encode('utf-8') in response.data
        assert ("4 ").encode('utf-8') in response.data
        assert ("5 ").encode('utf-8') not in response.data

    def test_create_delivery(self):
        '''Tests if create_delivery does as it says, and no more
        '''
        
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")
        PP.order_fac.create_new_order()
        
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])

        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(3,[pizza1])

        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(3,[pizza1])

        address = '321 qwert'

        # Tests if it returns a relevent message for pickup
        data = {'address': '321 qwert', 'delivery_type':'pickup' }
        response = self.client.post('/create_delivery/1', data = data)
        assert response.status_code == 200
        assert ("pickup").encode('utf-8') in response.data

        # Tests if it returns a relevent message for PP delivery
        data = {'address': address, 'delivery_type':'pizzaparlour' }
        response = self.client.post('/create_delivery/2', data = data)
        assert response.status_code == 200
        assert ("We").encode('utf-8') in response.data
        assert ("deliver").encode('utf-8') in response.data

        # Tests if it returns a relevent message for ubereats delivery, and makes a json file
        data = {'address': address, 'delivery_type':'ubereats' }
        response = self.client.post('/create_delivery/3', data = data)
        assert response.status_code == 200
        assert ("Uber Eats").encode('utf-8') in response.data
        assert ("deliver").encode('utf-8') in response.data
        with open('delivery.json') as f:
            info = json.load(f)
            assert info['Address'] == address
            assert info['Order Number'] == 3

        # Tests if it returns a relevent message for foodora delivery, and makes a csv file
        data = {'address': address, 'delivery_type':'foodora' }
        response = self.client.post('/create_delivery/4', data = data)
        assert response.status_code == 200
        assert ("Foodora").encode('utf-8') in response.data
        assert ("deliver").encode('utf-8') in response.data
        with open('delivery.csv') as f:
            info=f.read()
            assert address in info
            assert '4' in info

        # Tests if it rejects invalid ids
        data = {'address': address, 'delivery_type':'pickup' }
        response = self.client.post('/create_delivery/5', data = data)
        assert response.status_code == 200
        assert ("deliver").encode('utf-8') not in response.data

    def test_is_pizza(self):
        '''Tests if is_pizza gives meaningful info about the Product type
        '''
        
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")
        drink1 = Drink("drink", 0, "Coke")
        PP.order_fac.create_new_order()
        
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(3,[drink1])

        # Tests if it returns True when it is a pizza
        response = self.client.get('/item_type/2/1')
        assert response.status_code == 200
        assert ("True").encode('utf-8') in response.data

        # Tests if it returns False when it is a drink
        response = self.client.get('/item_type/3/1')
        assert response.status_code == 200
        assert ("False").encode('utf-8') in response.data

        # Tests if it returns None when the order does not exist
        response = self.client.get('/item_type/4/1')
        assert response.status_code == 200
        assert ("None").encode('utf-8') in response.data

        # Tests if it returns None when the product does not exist
        response = self.client.get('/item_type/1/1')
        assert response.status_code == 200
        assert ("None").encode('utf-8') in response.data

    def test_get_toppings(self):
        '''Tests if get_toppings gives the toppings of the given pizza
        '''
        
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium", toppings = ['pepperoni','tomatoes','mushroom'])
        pizza2 = Pizza("custom_pizza", 5.0, "medium", toppings = ['olives','tomatoes','tomatoes'])
        drink1 = Drink("drink", 0, "Coke")
        PP.order_fac.create_new_order()
        
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(3,[drink1,pizza2])

        # Tests if it returns the right dict for a pizza
        response = self.client.get('/get_toppings/2/1')
        assert response.status_code == 200
        toppings = {'pepperoni':1,'tomatoes':1,'mushroom':1}
        for key in toppings:
            assert key.encode('utf-8') in response.data
            assert str(toppings[key]).encode('utf-8') in response.data

        # Tests if it returns the right dict for a pizza with multiples
        response = self.client.get('/get_toppings/3/2')
        assert response.status_code == 200
        toppings = {'olives':1,'tomatoes':2}
        for key in toppings:
            assert key.encode('utf-8') in response.data
            assert str(toppings[key]).encode('utf-8') in response.data

        # Tests if it returns None when the item is a drink
        response = self.client.get('/get_toppings/3/1')
        assert response.status_code == 200
        assert ("None").encode('utf-8') in response.data

        # Tests if it returns None when the order does not exist
        response = self.client.get('/get_toppings/4/1')
        assert response.status_code == 200
        assert ("None").encode('utf-8') in response.data

        # Tests if it returns None when the product does not exist
        response = self.client.get('/item_type/1/1')
        assert response.status_code == 200
        assert ("None").encode('utf-8') in response.data

    def test_update_pizza(self):
        '''Tests if update_pizza does as its name implies
        '''
        
        pizza1 = Pizza("pepperoni_pizza", 5.0, "medium")#, toppings = ['pepperoni','tomatoes','mushroom'])
        pizza2 = Pizza("custom_pizza", 5.0, "medium", toppings = ['olives','tomatoes','tomatoes'])
        drink1 = Drink("drink", 0, "Coke")
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(1,[pizza1])
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza2])
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(3,[drink1,pizza2])

        # Tests if it updates the type of an existing pizza
        data = {'order_number':1,'item_number':1,'type': 'vegetarian_pizza' }
        response = self.client.post('/update_pizza/type', data = data)
        assert response.status_code == 200
        assert 'vegetarian' in PP.order_fac.orders[0].get_item_by_id(1)

        # Tests if it updates the size of an existing pizza
        data = {'order_number':1,'item_number':1,'pizza_size': 'large' }
        response = self.client.post('/update_pizza/size', data = data)
        assert response.status_code == 200
        assert 'large' in PP.order_fac.orders[0].get_item_by_id(1)

        # Tests if it updates the toppings of an existing pizza
        data = {'order_number':1,'item_number':1,'toppings': ['jalapenos','tomatoes','mushroom'], 'add_or_remove':'add' }
        response = self.client.post('/update_pizza/toppings', data = data)
        assert response.status_code == 200
        assert 'jalapenos' in PP.order_fac.orders[0].get_item_by_id(1)
        
        data = {'order_number':1,'item_number':1,'toppings': ['jalapenos','jalapenos','jalapenos','tomatoes'], 'add_or_remove':'remove' }
        response = self.client.post('/update_pizza/toppings', data = data)
        assert response.status_code == 200
        assert 'jalapenos' not in PP.order_fac.orders[0].get_item_by_id(1)

    def test_update_drink(self):
        '''Tests if update_drink does as its name implies
        '''

        drink1 = Drink("drink", 0, "Coke")
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(1,[drink1])

        # Tests if it updates the type of an existing drink
        data = {'order_number':1,'item_number':1,'drink_brand': 'Pepsi' }
        response = self.client.post('/update_drink/brand', data = data)
        assert response.status_code == 200
        assert 'Pepsi' in PP.order_fac.orders[0].get_item_by_id(1)

    def test_create_pizza(self):
        '''Tests if create_pizza does as its name implies
        '''

        PP.order_fac.create_new_order()
        PP.order_fac.create_new_order()

        # Tests if it will create multiple pizzas
        data = {'order_number':1,'quantity':2,'pizza_type': 'vegetarian_pizza' , 'pizza_size':'medium','toppings':['olives']}
        response = self.client.post('/create_pizza', data = data)
        print(PP.order_fac.orders[0].get_item_by_id(1))
        assert response.status_code == 200
        assert 'vegetarian' in PP.order_fac.orders[0].get_item_by_id(1)
        assert 'medium' in PP.order_fac.orders[0].get_item_by_id(1)
        assert ' 1' in PP.order_fac.orders[0].get_item_by_id(1)
        assert PP.order_fac.orders[0].get_item_by_id(1) != "None"
        assert PP.order_fac.orders[0].get_item_by_id(2) != "None"
        assert PP.order_fac.orders[0].get_item_by_id(3) == "None"

        # Tests if it will create a custom pizza
        data = {'order_number':2,'quantity':1,'pizza_type': 'custom_pizza' , 'pizza_size':'large','toppings':['olives','olives','olives','tomatoes']}
        response = self.client.post('/create_pizza', data = data)
        assert response.status_code == 200
        assert 'custom' in PP.order_fac.orders[1].get_item_by_id(1)
        assert 'olives' in PP.order_fac.orders[1].get_item_by_id(1)
        assert 'tomatoes' in PP.order_fac.orders[1].get_item_by_id(1)
        assert 'large' in PP.order_fac.orders[1].get_item_by_id(1)
        assert ' 3' in PP.order_fac.orders[1].get_item_by_id(1)
        assert PP.order_fac.orders[1].get_item_by_id(2) == "None"

        # Tests if it will create a undefined pizza
        data = {'order_number':2,'quantity':2,'pizza_type': 'blah' , 'pizza_size':'nah','toppings':'pah'}
        response = self.client.post('/create_pizza', data = data)
        assert response.status_code == 200
        assert PP.order_fac.orders[1].get_item_by_id(2) == "None"

    def test_create_drink(self):
        '''Tests if create_drink does as its name implies
        '''

        PP.order_fac.create_new_order()

        # Tests if it will create multiple drinks
        data = {'order_number':1,'quantity':2,'drinks':['Pepsi','Coke']}
        response = self.client.post('/create_drink', data = data)
        assert response.status_code == 200
        assert 'Pepsi' in PP.order_fac.orders[0].get_item_by_id(1)
        assert 'Coke' in PP.order_fac.orders[0].get_item_by_id(2)
        assert PP.order_fac.orders[0].get_item_by_id(1) != "None"
        assert PP.order_fac.orders[0].get_item_by_id(2) != "None"
        assert PP.order_fac.orders[0].get_item_by_id(3) == "None"

        # Tests if it will create nonsense drinks. Drinks are set up in such a way that their price is the same.
        # data = {'order_number':1,'quantity':2,'drinks':['blahza']}
        # response = self.client.post('/create_drink', data = data)
        # assert response.status_code == 200
        # assert PP.order_fac.orders[0].get_item_by_id(3) == "None"

    def test_get_data(self):
        '''Tests if get_data gives access to the various files
        '''

        # Tests if it will retrieve pizza types
        response = self.client.get('/get_data/pizza_types')
        assert response.status_code == 200
        assert "vegetarian_pizza" in response.json

        # Tests if it will retrieve pizza sizes
        response = self.client.get('/get_data/pizza_sizes')
        assert response.status_code == 200
        assert "large" in response.json

        # Tests if it will retrieve prices
        response = self.client.get('/get_data/prices')
        assert response.status_code == 200
        assert "vegetarian_pizza" in response.json

        # Tests if it will reject nonvalid datatype
        response = self.client.get('/get_data/sjlhbg')
        assert response.status_code == 200
        assert response.json is None
        assert "invalid" in str(response.data).lower()

    def test_set_price(self):
        '''Tests if set_price changes the price of the given product
        '''

        pizza1 = Pizza("pepperoni_pizza", 5.0, "small")
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(1,[pizza1])

        # Tests if it will change a price
        data = {'product_name':'pepperoni_pizza','price':9.0}
        response = self.client.post('/set_price', data = data)
        assert response.status_code == 200
        assert "price set" in str(response.data)
        assert 'pepperoni_pizza' in str(response.data)
        assert '9.0' in str(response.data)

        assert PP.order_fac.orders[0].order_total == 9.0

        # Tests if it will change a price back
        data = {'product_name':'pepperoni_pizza','price':9.3}
        response = self.client.post('/set_price', data = data)
        assert response.status_code == 200
        assert "price set" in str(response.data)
        assert 'pepperoni_pizza' in str(response.data)
        assert '9.3' in str(response.data)

        # Create a new order with the old pizza and a new order with a new pizza. All should have the new price.
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(2,[pizza1])

        PP.order_fac.create_new_order()
        pizza2 = Pizza("pepperoni_pizza", 5.0, "small")
        PP.order_fac.add_to_order(3,[pizza2])

        assert PP.order_fac.orders[2].order_total == 9.3
        assert PP.order_fac.orders[1].order_total == 9.3
        assert PP.order_fac.orders[0].order_total == 9.3

        # Tests if it will do nothing on a faulty price
        data = {'product_name':'pepperoni_pizza','price':'a'}
        response = self.client.post('/set_price', data = data)
        assert response.status_code == 200
        assert 'failure' in str(response.data).lower()

        assert PP.order_fac.orders[0].order_total == 9.3

    def test_remove_item(self):
        '''Tests if remove_item does what is says
        '''

        pizza1 = Pizza("pepperoni_pizza", 5.0, "small")
        pizza2 = Pizza("vegetarian_pizza", 5.0, "medium")
        pizza3 = Pizza("margherita_pizza", 5.0, "large")
        PP.order_fac.create_new_order()
        PP.order_fac.add_to_order(1,[pizza1,pizza2,pizza3])

        # Tests if it will remove an item
        data = {'order_number':1,'item_number':2}
        response = self.client.post('/remove_item', data = data)
        assert response.status_code == 200
        assert "delete" in str(response.data)
        assert '2 ' in str(response.data)
        assert ' 1' in str(response.data)

        assert "vegetarian_pizza" not in str(PP.order_fac.orders[0].items[1])

         # Tests if it will ignore nonexistent items
        data = {'order_number':1,'item_number':4}
        response = self.client.post('/remove_item', data = data)
        assert response.status_code == 200
        assert "invalid" in str(response.data).lower()

        assert "margherita_pizza" in str(PP.order_fac.orders[0].items[1])


import requests
from unittest import mock
import trial

import io
import sys

# Method for mocking http request responses from https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
# Used to isolate the Commands tests from the PizzaParlour ones
url = 'http://127.0.0.1:5000/'
cur_id = 0

class MockResponse:
        def __init__(self, text_data, status_code, content = '', json_dict = {}):
            self.text = text_data
            self.status_code = status_code
            self.content = content
            self.json_dict = json_dict
        
        def json(self):
            return self.json_dict
# This method will be used by the mock to replace requests.get
def get_ints(string,i):
    num = ''
    while string[i] != '/':
        num += string[i]
        i += 1
    return int(num)

def mocked_requests_get(*args):

    if args[0] == url + 'new_order':
        return MockResponse(0, 200)
    if args[0][0:len(url+'order_is_valid')] == url + 'order_is_valid':
        ids = args[0][len(url+'order_is_valid'):].split('/')
        print(ids)
        return MockResponse(str(PP.order_fac.is_valid_order_number(int(ids[1]))!=None), 200)
    if args[0][0:len(url+'get_item')] == url + 'get_item':
        ids = args[0][len(url+'get_item'):-1].split('/')
        item_id = ids[1]
        order_id = ids[0]
        return MockResponse(PP.order_fac.get_item_in_order_by_id(order_id, item_id), 200)
    if args[0] == url + 'get_order':
        ids = args[0][len(url+'get_order'):-1].split('/')
        order_id = ids[0]
        return MockResponse(PP.order_fac.get_order(order_id), 200)
    if args[0] == url + 'item_type':
        ids = args[0][len(url+'get_item'):-1].split('/')
        item_id = ids[1]
        order_id = ids[0]
        return MockResponse(PP.order_fac.is_pizza(order_id,item_id), 200)


    if args[0] == url + '/get_order_list':
        return MockResponse(0, 200)
    

    elif args[0][0:len(url+'delete_order/')] == url+'delete_order/':
        return MockResponse('Order '+args[0][-1]+' deleted', 200)

    return MockResponse(None, 404)

def mock_filler(*args, **kwargs):
    return MockResponse(args, 200, kwargs)

def mocked_requests_post_kwargs_first(*args, **kwargs):
    return MockResponse(kwargs, 200)

def mocked_requests_post(*args, **kwargs):
 
    if args[0] == url + 'new_order':
        # data in post request is in kwargs. use print statement to see structure

        #print(args, kwargs)
        return MockResponse(0, 200)
        #'New order is: id '+str(cur_id)+', price '+str(kwargs['data']['price']),
    elif args[0][0:len(url+'delete_order/')] == url+'delete_order/':
        return MockResponse('Order '+args[0][-1]+' deleted', 200)

    return MockResponse(None, 404)

class CommandTest(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # We patch 'requests.post' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_new_order_number(self, mock_get):
        """Test whether the create_order command works"""
        
        c = trial

        #cli_output = io.StringIO()                  # Create StringIO object
        #sys.stdout = cli_output                     #  and redirect stdout.

        # Tests if creating an order works first time
        #data = c.new_order(['new_order'])

        #assert data == True
        order_number = c.get_new_order_number()
        assert order_number == 0
        #cli_output.truncate(0)
        #cli_output.seek(0)

        # We can even assert that our mocked method was called with the right parameters
        #assert mock.call('http://someurl.com/test.json') in mock_post.call_args_list
        #assert mock.call('http://someotherurl.com/anothertest.json') in mock_post.call_args_list

        #sys.stdout = sys.__stdout__                     # Reset redirect.

        assert len(mock_get.call_args_list) == 1

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_valid_order_number(self, mock_get,  mocked_input):
        """Test whether the get_valid_order_number command works"""

        # Too much reliance on external libraries. Just mocking replies directly now.
        mock_get.side_effect = [MockResponse('True', 200),
                                    MockResponse('False', 200),
                                    MockResponse('True', 200)]
        mocked_input.side_effect = ['0', '1','1']


        order_number = trial.get_valid_order_number()
        assert order_number == 0

        order_number = trial.get_valid_order_number()
        assert order_number == 1

        #sys.stdout = sys.__stdout__                     # Reset redirect.

        assert len(mock_get.call_args_list) == 3

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_item(self, mock_get,  mocked_input):
        """Test whether the get_item command works"""

        # Too much reliance on backend. Just mocking replies directly now.
        mock_get.side_effect = [MockResponse('Item with ID: 1\nPizza \nType: vegetarian_pizza\nToppings:{}', 200)]


        item = trial.get_item(1,1)
        assert item == 'Item with ID: 1\nPizza \nType: vegetarian_pizza\nToppings:{}'

        item = trial.get_item('a','b')
        assert item == 'Those are not valid ids: a, b'

        #sys.stdout = sys.__stdout__                     # Reset redirect.

        assert len(mock_get.call_args_list) == 1

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_order(self, mock_get,  mocked_input):
        """Test whether the get_order command works"""

        # Too much reliance on backend. Just mocking replies directly now.
        mock_get.side_effect = [MockResponse('Something', 200),MockResponse("This order number is invalid", 200)]

        item = trial.get_order(1)
        assert item == 'Something'

        item = trial.get_order('a')
        assert item == "This order number is invalid"

        assert len(mock_get.call_args_list) == 2

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_valid_item_number(self, mock_get,  mocked_input):
        """Test whether the get_valid_item_number command works"""

        # Too much reliance on backend. Just mocking replies directly now.
        mock_get.side_effect = [MockResponse('Something1', 200),
        MockResponse("Something2", 200),MockResponse('Something3', 200)]
        mocked_input.side_effect = ['1', '0','a','2']

        item_num = trial.get_valid_item_number(1)
        assert item_num == 1

        item_num = trial.get_valid_item_number('a')
        assert item_num == "This order number is invalid: a"

        item_num = trial.get_valid_item_number(3)
        assert item_num == 2

        assert len(mock_get.call_args_list) == 3

    @mock.patch('trial.edit_drink')
    @mock.patch('trial.edit_pizza')
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_decide_item_to_edit(self, mock_get, mock_edit_pizza, mock_edit_drink):
        """Test whether the decide_item_to_edit command works"""

        mock_get.side_effect = [MockResponse('Something1', 200, content = True),MockResponse("This order number is invalid", 200, content = False)]
        mock_edit_pizza.side_effect = ['ok1']
        mock_edit_drink.side_effect = ['ok2']

        # Checks if the http request was sent
        trial.decide_item_to_edit(1,2)
        mock_edit_pizza.assert_called()

        # Checks if the http request was sent
        trial.decide_item_to_edit(3,4)
        mock_edit_drink.assert_called()

        # Method not fully implemented, so not doing much testing
        #item_num = trial.decide_item_to_edit('a', 'b')
        #assert item_num == "These ids are invalid: a, b"

        assert len(mock_get.call_args_list) == 2

    @mock.patch('trial.input', create=True)
    @mock.patch('trial.edit_pizza_type',side_effect=mock_filler)
    @mock.patch('trial.edit_pizza_size',side_effect=mock_filler)
    @mock.patch('trial.edit_pizza_toppings',side_effect=mock_filler)
    def test_edit_pizza(self, mock_top, mock_size, mock_type ,  mocked_input):
        """Test whether the get_valid_item_number command works"""

        mocked_input.side_effect = ['1', '2','3','a','4']

        trial.edit_pizza(1,1)
        mock_type.assert_called()

        trial.edit_pizza(2,2)
        mock_size.assert_called()

        trial.edit_pizza(3,3)
        mock_top.assert_called()

        trial.edit_pizza(4,4)

        assert len(mocked_input.call_args_list) == 5

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_edit_pizza_attribute(self, mock_post,  mocked_input):
        """Test whether the edit_pizza_etc commands work"""

        mock_post.side_effect = [MockResponse('Something1', 200),MockResponse("These ids are invalid: a, b", 200),
        MockResponse('Something2', 200),MockResponse('Something3', 200),
        MockResponse('Something4', 200),MockResponse('Something5', 200)]
        mocked_input.side_effect = ['1', 'x','2','2','y','3','3','z','4']

        # edit type testing
        trial.edit_pizza_type(1,1)
        mock_post.assert_called()

        trial.edit_pizza_type('a','b')
        mock_post.assert_called()

        # edit size testing
        trial.edit_pizza_size(2,2)
        mock_post.assert_called()

        trial.edit_pizza_size('c','d')
        mock_post.assert_called()

        # edit toppings testing
        trial.edit_pizza_size(3,3)
        mock_post.assert_called()

        trial.edit_pizza_size('e','f')
        mock_post.assert_called()

        assert len(mock_post.call_args_list) == 5



    @mock.patch('trial.input', create=True)
    @mock.patch('requests.post', side_effect=mocked_requests_post_kwargs_first)
    def test_create_new_pizza(self, mock_post,  mocked_input):
        """Test whether the edit_pizza_etc commands work"""

        mocked_input.side_effect = ['1', '1','1', '2','2','2','3','3','3','4','4','4','a','1','b','2','c','3']
        cli_output = io.StringIO()                  # Create StringIO object
        sys.stdout = cli_output                     #  and redirect stdout.

        # These tests are effectively hard-coded, but the pizza types should be dynamic
        # TODO: make tests dynamic as well

        trial.create_new_pizza(1)
        mock_post.assert_called()

        assert cli_output.getvalue().split('\n')[-2] == "{'data': {'order_number': 1, 'quantity': 1, 'pizza_type': 'vegetarian_pizza', 'pizza_size': 'small', 'toppings': None}}"

        trial.create_new_pizza(2)
        mock_post.assert_called()

        assert cli_output.getvalue().split('\n')[-2] == "{'data': {'order_number': 2, 'quantity': 2, 'pizza_type': 'pepperoni_pizza', 'pizza_size': 'medium', 'toppings': None}}"

        trial.create_new_pizza(3)
        mock_post.assert_called()

        assert cli_output.getvalue().split('\n')[-2] == "{'data': {'order_number': 3, 'quantity': 3, 'pizza_type': 'margherita_pizza', 'pizza_size': 'large', 'toppings': None}}"

        trial.create_new_pizza(4)
        mock_post.assert_called()

        assert cli_output.getvalue().split('\n')[-2] == "{'data': {'order_number': 4, 'quantity': 4, 'pizza_type': 'neapolitan_pizza', 'pizza_size': 'x-large', 'toppings': None}}"

        trial.create_new_pizza(5)
        mock_post.assert_called()

        assert cli_output.getvalue().split('\n')[-2] == "{'data': {'order_number': 5, 'quantity': 3, 'pizza_type': 'vegetarian_pizza', 'pizza_size': 'medium', 'toppings': None}}"

        assert len(mock_post.call_args_list) == 5

        sys.stdout = sys.__stdout__                     # Reset redirect.

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.post')
    def test_custom_pizza_route(self, mock_post,  mocked_input):
        """Test whether the edit_pizza_etc commands work"""
        
        mock_post.side_effect = [MockResponse('Something1', 200),MockResponse("These ids are invalid: a, b", 200),
        MockResponse('Something2', 200),MockResponse('Something3', 200),
        MockResponse('Something4', 200),MockResponse('Something5', 200)]
        mocked_input.side_effect = ['1', '2','8','9','y','3','3','z','8','4','2','5','1','8']

        toppings = trial.custom_pizza_route(True)
        assert toppings == ['olives','olives']

        toppings = trial.custom_pizza_route(True)
        assert toppings == None

        toppings = trial.custom_pizza_route(True)
        assert toppings == ['tomatoes','tomatoes','tomatoes']

        toppings = trial.custom_pizza_route(True)
        assert toppings == ['mushroom','mushroom','chicken']


        assert len(mocked_input.call_args_list) == 14


    @mock.patch('trial.input', create=True) 
    @mock.patch('requests.get')
    def test_cancel_order(self, mock_get,  mocked_input):
        """Test whether the edit_pizza_etc commands work"""
        
        cli_output = io.StringIO()                  # Create StringIO object
        sys.stdout = cli_output                     #  and redirect stdout.

        mock_get.side_effect = [MockResponse('True', 200),
        MockResponse('Something1', 200),MockResponse('True', 200),MockResponse('Something2', 200),MockResponse('False', 200),MockResponse('True', 200),MockResponse('Something3', 200)]
        mocked_input.side_effect = ['1', 'y', 'a', '2', '3', '4']

        trial.cancel_order()
        assert cli_output.getvalue().split('\n')[-2]  == 'Something1'

        trial.cancel_order()
        assert cli_output.getvalue().split('\n')[-2]  == 'Something2'

        trial.cancel_order()
        assert cli_output.getvalue().split('\n')[-2]  == 'Something3'

        assert len(mocked_input.call_args_list) == 6

        sys.stdout = sys.__stdout__                     # Reset redirect.

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.post')
    def test_create_delivery(self, mock_post,  mocked_input):
        """Test whether the edit_pizza_etc commands work"""
        
        mock_post.side_effect = [MockResponse('Something1', 200),
        MockResponse('Something2', 200),MockResponse('Something3', 200),
        MockResponse('Something4', 200),MockResponse('Something5', 200)]
        mocked_input.side_effect = ['1', '2','3','4','y','1','2','1']

        delivery = trial.create_delivery(1)
        assert delivery == 'Something1'

        delivery = trial.create_delivery(1)
        assert delivery == 'Something2'

        delivery = trial.create_delivery(1)
        assert delivery == 'Something3'

        delivery = trial.create_delivery(1)
        assert delivery == 'Something4'

        assert len(mocked_input.call_args_list) == 8

    @mock.patch('trial.input', create=True)
    @mock.patch('requests.get')
    @mock.patch('requests.post',side_effect=mocked_requests_post_kwargs_first)
    def test_set_price(self, mock_post, mock_get, mocked_input):
        """Test whether the set_price commands work"""

        cli_output = io.StringIO()                  # Create StringIO object
        sys.stdout = cli_output                     #  and redirect stdout.

        mock_get.side_effect = [MockResponse('Something1', 200,json_dict={'a':1.5,'b':2.75,'c':4}), MockResponse('Something2', 200,json_dict={'a':1.5,'b':2.75,'c':4})]

        mocked_input.side_effect = ['1', '7.2','b','2','y','-1','3']

        def result_gen(name,price):
            return str({'data':{'product_name': name,'price': price}})

        trial.set_price()
        assert cli_output.getvalue().split('\n')[-2]  == result_gen('a',7.2)

        trial.set_price()
        assert cli_output.getvalue().split('\n')[-2]  == result_gen('b',3.0)

        assert len(mocked_input.call_args_list) == 7

        sys.stdout = sys.__stdout__                     # Reset redirect.

if __name__ == '__main__':
    unittest.main()