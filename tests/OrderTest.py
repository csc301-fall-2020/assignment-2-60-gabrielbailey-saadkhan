import unittest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from Order import OrderFactory, Order
from Product import Pizza


class OrderTest(unittest.TestCase):

    def test_create_order(self):
        order = Order(1)
        assert isinstance(order, Order)
    
    def test_get_order_number(self):
        order = Order(1)
        assert order.get_order_number() == 1
    
    def test_add_item(self):
        order = Order(1)
        pizza = Pizza("vegetarian_pizza", 0, "small")
        order.add_item(pizza)
        assert pizza.id == 1
        assert 1 in order.ids_to_items
        assert order.ids_to_items[1] == pizza
        assert len(order.items) == 1
    
    def test_update_total(self):
        order = Order(1)
        assert order.order_total == 0
        pizza = Pizza("vegetarian_pizza", 0, "small")
        order.add_item(pizza)
        order.update_total()
        assert order.order_total == 9.99
    
    def test_get_item_by_id(self):
        order = Order(1)
        pizza = Pizza("vegetarian_pizza", 0, "small")
        order.add_item(pizza)
        assert order.get_item_by_id(1) != "None"
    
    def test_is_pizza(self):
        order = Order(1)
        pizza = Pizza("vegetarian_pizza", 0, "small")
        order.add_item(pizza)
        assert order.is_pizza(1) == "True"
    
    def test_remove_item(self):
        order = Order(1)
        pizza = Pizza("vegetarian_pizza", 0, "small")
        order.add_item(pizza)
        order.remove_item(1)
        assert 1 not in order.ids_to_items
        assert len(order.items) == 0
    
    def test_get_toppings(self):
        order = Order(1)
        pizza = Pizza("pepperoni_pizza", 0, "small")
        order.add_item(pizza)
        order.get_toppings(1) == {"pepperoni": 1, "tomatoes": 1}
    
    def test_get_delivery(self):
        order = Order(1)
        assert order.get_delivery() == None
    
    def test_update_item_type(self):
        order = Order(1)
        pizza = Pizza("pepperoni_pizza", 0, "small")
        order.add_item(pizza)
        order.update_item(1, "type", "vegetarian_pizza")
        assert pizza.get_type() == "vegetarian_pizza"
    
    def test_update_item_size(self):
        order = Order(1)
        pizza = Pizza("pepperoni_pizza", 0, "small")
        order.add_item(pizza)
        order.update_item(1, "size", "medium")
        assert pizza.size == "medium"
    
    def test_update_item_toppings(self):
        order = Order(1)
        pizza = Pizza("pepperoni_pizza", 0, "small")
        order.add_item(pizza)
        order.update_item(1, "toppings", ["olives"], "add")
        assert pizza.toppings == {"pepperoni": 1, "tomatoes": 1, "olives": 1}

class OrderFactoryTest(unittest.TestCase):

    def test_create_order_factory(self):
        order_factory = OrderFactory()
        assert isinstance(order_factory, OrderFactory)
    
    def test_add_order(self):
        order_factory = OrderFactory()
        order_factory.create_new_order()
        assert len(order_factory.orders) == 1
    
    def test_cancel_order(self):
        order_factory = OrderFactory()
        order_factory.create_new_order()
        order_factory.cancel_order(1)
        assert len(order_factory.orders) == 0
    
    def test_is_valid_order_number(self):
        order_factory = OrderFactory()
        order_factory.create_new_order()
        assert isinstance(order_factory.is_valid_order_number(1), Order)


if __name__ == '__main__':
    unittest.main()
