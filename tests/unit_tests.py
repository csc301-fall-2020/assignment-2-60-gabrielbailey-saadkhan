import unittest
from flask_testing import TestCase
from Models import Order, init_db
from PizzaParlour import create_app, db

class PizzaParlourTest(TestCase):
    ''' General testing class copied from flask testing tutorial.
    Should contain all tests of http requests and databases.'''

    def create_app(self):
        # used at the start of the tests in this class to create the app (I think)
        # pass in test configuration
        # Currently using in memory database to be a bit faster. to write to a db use 'tests.db' instead of :memory:
        return create_app(True, 'sqlite:///:memory:')

    def setUp(self):
        # Used before every test to set up the database.

        # Maybe add random amount of info in database? Non-deterministic tests sound bad though...
        init_db(db)

    def tearDown(self):
        # Used after every test to clean up the database.

        db.session.remove()
        db.drop_all()

    def test_pizza(self):
        '''Tests if there is a repsonse given'''
        response = self.client.get('/pizza')

        assert response.status_code == 200
        assert response.data == b'Welcome to Pizza Planet!'
    
    def test_create(self):
        '''Tests if the create_order works with a price given
        '''

        order = Order(price=3.5)
        db.session.add(order)

        # Have to place something in the db to get id:
        db.session.add(order) #make transaction to add order to the database
        db.session.flush() #Actually do it, updating order's id to the next id value
        print(order.id)
        db.session.delete(order) #make transaction to delete order from the database
        db.session.flush() #Actually do it, order stays the same though

        #assert Order.query.count() > 0

        response = self.client.post('/create_order', data=dict(id=order.id, price=order.price)) #crucial line: queries test server for response
        #db.session.delete(order) #make transaction to delete the new order from the database
        #db.session.flush() #Actually do it
        '''
        porders = Order.query.order_by(Order.id).all()
        print(porders)
        for por in porders:
            print(por.id, por.price)
        '''
        assert response.status_code == 200
        assert response.data == ('New order is: id '+str(order.id)+', price '+str(order.price)).encode('utf-8')

    def test_delete(self):
        '''Tests if the delete_order works with an id given
        '''

        order = Order(price=3.5)
        db.session.add(order)
        # Have to place something in the db to get id:
        db.session.add(Order(price=2.2)) #make transaction to add order to the database
        db.session.flush() #Actually do it, updating order's id to the next id value
        print(order.id)

        assert Order.query.count() > 1

        response = self.client.post('/delete_order/'+str(order.id)) #crucial line: queries test server for response

        assert response.status_code == 200
        assert response.data == ('Order '+str(str(order.id))+' deleted').encode('utf-8')

        assert Order.query.count() > 0

import requests
from unittest import mock
import Commands

import io
import sys

# Method for mocking http request responses from https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
# Used to isolate the Commands tests from the PizzaParlour ones
url = 'http://127.0.0.1:5000/'
cur_id = 0

# This method will be used by the mock to replace requests.get
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, text_data, status_code):
            self.text = text_data
            self.status_code = status_code

    
    if args[0] == url + 'create_order':
        # data in post request is in kwargs. use print statement to see structure

        #print(args, kwargs)
        return MockResponse('New order is: id '+str(cur_id)+', price '+str(kwargs['data']['price']), 200)

    elif args[0][0:len(url+'delete_order/')] == url+'delete_order/':
        return MockResponse('Order '+args[0][-1]+' deleted', 200)

    return MockResponse(None, 404)

class CommandsTest(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # We patch 'requests.post' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_create_order(self, mock_post):
        """Test whether the create_order command works"""
        
        c = Commands

        cli_output = io.StringIO()                  # Create StringIO object
        sys.stdout = cli_output                     #  and redirect stdout.

        # Tests if creating an order works first time
        data = c.create_order(['create_order',4.2])

        assert data == True
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'New order is: id '+str(0)+', price '+str(4.2)
        cli_output.truncate(0)
        cli_output.seek(0)

        # Tests if creating an order fails if input is too small
        data = c.create_order(['create_order'])

        assert data == False
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'Not enough arguments were input. Type "create_order -help" for more information.'
        cli_output.truncate(0)
        cli_output.seek(0)

        # Tests if creating an order fails if input is -help
        data = c.create_order(['create_order','-help'])

        assert data == False
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'Create an order with a given price. Example: create_order 3.50'
        cli_output.truncate(0)
        cli_output.seek(0)

        # Tests if creating an order works second time (redundant)
        data = c.create_order(['create_order',1])
        
        assert data == True
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'New order is: id '+str(0)+', price '+str(1.0)

        # We can even assert that our mocked method was called with the right parameters
        #assert mock.call('http://someurl.com/test.json') in mock_post.call_args_list
        #assert mock.call('http://someotherurl.com/anothertest.json') in mock_post.call_args_list

        

        sys.stdout = sys.__stdout__                     # Reset redirect.

        assert len(mock_post.call_args_list) == 2

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_delete_order(self, mock_post):
        """Test whether the delete_order command works"""

        c = Commands

        cli_output = io.StringIO()                  # Create StringIO object
        sys.stdout = cli_output                     #  and redirect stdout.

        # Tests if deleting an order works
        data = c.delete_order(['delete_order',3])

        assert data == True
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'Order '+str(3)+' deleted'
        cli_output.truncate(0)
        cli_output.seek(0)

        # Tests if deleting an order fails with no id
        data = c.delete_order(['delete_order'])

        assert data == False
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'Not enough arguments were input. Type "delete_order -help" for more information.'
        cli_output.truncate(0)
        cli_output.seek(0)

        # Tests if deleting an order gives help with -help
        data = c.delete_order(['delete_order','-help'])

        assert data == False
        val = cli_output.getvalue().partition('\n')[0]
        assert val == 'Delete an order with a given id. Example: delete_order 4'
        cli_output.truncate(0)
        cli_output.seek(0)

        sys.stdout = sys.__stdout__                     # Reset redirect.

        assert len(mock_post.call_args_list) == 1

if __name__ == '__main__':
    unittest.main()