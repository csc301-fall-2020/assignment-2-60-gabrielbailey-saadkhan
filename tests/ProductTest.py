import unittest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from Product import Product, Pizza, Drink
from unittest import mock

class ProductTest(unittest.TestCase):
    def test_create_product(self):
        product = Product("type", 1.0)
        assert isinstance(product, Product)
    
    def test_get_price(self):
        product = Product("type", 1.0)
        assert product.get_price() == 1.0
    
    def test_set_price(self):
        product = Product("type", 1.0)
        product.set_price(2.0)
        assert product.get_price() == 2.0
    
    def test_get_type(self):
        product = Product("type", 1.0)
        assert product.get_type() == "type"
    
    def test_set_type(self):
        product = Product("type", 1.0)
        product.set_type("Type2")
        assert product.get_type() == "Type2"

class PizzaTest(unittest.TestCase):

    def test_create_pizza(self):
        pizza = Pizza("vegetarian_pizza", 0, "small")
        assert isinstance(pizza, Pizza)
    
    def test_create_pizza_doesnt_exist(self):
        self.assertRaises(KeyError, Pizza, "lol", 0, "small")
    
    def test_create_pizza_size_doesnt_exist(self):
        self.assertRaises(KeyError, Pizza, "vegetarian_pizza", 0, "lol")
    
    def test_set_id(self):
        pizza = Pizza("vegetarian_pizza", 0, "small")
        pizza.set_id(1)
        assert pizza.id == 1

    def test_process_toppings(self):
        pizza = Pizza("vegetarian_pizza", 0, "small")
        value = pizza.process_toppings(["olives", "chicken", "olives"])
        assert value == {"chicken": 1, "olives": 2}
    
    def test_set_up_toppings(self):
        pizza = Pizza("pepperoni_pizza", 0, "small")
        pizza.set_up_toppings()
        pizza.get_toppings() == {"pepperoni": 1, "tomatoes": 1}
    
    def test_update_prices(self):
        pizza = Pizza("pepperoni_pizza", 0, "small")
        pizza.set_type("vegetarian_pizza")
        pizza.toppings = pizza.set_up_toppings()
        pizza.update_prices()
        assert pizza.get_price() == 9.99

    def test_update_toppings_add(self):
        pizza = Pizza("pepperoni_pizza", 0, "small")
        pizza.update_toppings("add", ["olives"])
        assert pizza.toppings == {'pepperoni': 1, 'tomatoes': 1, 'olives': 1}
    
    def test_update_toppings_remove(self):
        pizza = Pizza("pepperoni_pizza", 0, "small")
        pizza.update_toppings("remove", ["tomatoes"])
        assert pizza.toppings == {'pepperoni': 1}
    
    def test_update_pizza_size(self):
        pizza = Pizza("pepperoni_pizza", 0, "small")
        pizza.update_pizza_size("medium")
        assert pizza.size == "medium"

class DrinkTest(unittest.TestCase):
    
    def test_create_drink(self):
        drink = Drink("drink", 0, "Diet Coke")
        assert isinstance(drink, Drink)
    
    def test_set_id(self):
        drink = Drink("drink", 0, "Diet Coke")
        drink.set_id(1)
        assert drink.id == 1
    
    def test_get_id(self):
        drink = Drink("drink", 0, "Diet Coke")
        drink.set_id(1)
        assert drink.get_id() == 1
    
    def test_update_prices(self):
        drink = Drink("drink", 0, "Diet Coke")
        drink.update_prices()
        assert drink.price == 1.0
    
    def test_update_brand(self):
        drink = Drink("drink", 0, "Diet Coke")
        drink.update_brand("Coke Zero")
        assert drink.brand == "Coke Zero"


if __name__ == '__main__':
    unittest.main()