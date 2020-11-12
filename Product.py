from Data import Data
import pprint
import json
class Product:
    def __init__(self, type:str, price:float):
        self.type = type
        self.price = price
    
    def get_price(self) -> float:
        """
        Returns the price of this item
        """
        return self.price
    
    def set_price(self, price:float):
        """
        Sets the price of the product to price
        """
        self.price = price
    
    def get_type(self):
        """
        Return the type of product this is
        """
        return self.type
    def set_type(self, type: str):
        """
        Sets the type of the product to the given type
        """
        self.type = type

class Pizza(Product):

    def __init__(self, type:str, price:float, size: str, toppings=None):
        Product.__init__(self, type, price)
        self.prices_given = Data.getInstance().get_prices_dict()
        self.price_qualifier = Data.getInstance().get_size_qualifier()
        self.pizza_to_toppings = Data.getInstance().get_pizza_to_toppings() 
        self.size = size
        self.id = None
        self.toppings = self.set_up_toppings(toppings)
        self.update_prices()

    def set_id(self, id):
        self.id = id
    
    def get_toppings(self):
        return json.dumps(self.toppings, indent=4, sort_keys=True)
    
    def set_up_toppings(self, toppings=None):
        if toppings is None:
            return self.pizza_to_toppings[self.type].copy()
        return self.process_toppings(toppings)
    
    def process_toppings(self, toppings):
        result = {}
        for topping in toppings:
            if topping not in result:
                result[topping] = 0
            result[topping] += 1
        return result
    
    def update_prices(self):
        self.price = self.prices_given[self.type] * self.price_qualifier[self.size]
        for keys, values in self.toppings.items():
            if keys not in self.pizza_to_toppings[self.type]:
                self.price +=  self.prices_given[keys] * self.toppings[keys]
            elif self.toppings[keys] > self.pizza_to_toppings[self.type][keys]:
                print("here")
                self.price +=  self.prices_given[keys] * (self.toppings[keys] - self.pizza_to_toppings[self.type][keys])
                print(self.price)
                
    def update_toppings(self, add_or_remove, toppings):
        topping_dict = self.process_toppings(toppings)
        for keys, values in topping_dict.items():
            if keys not in self.toppings:
                self.toppings[keys] = 0
            if add_or_remove == "add":
                self.toppings[keys] += topping_dict[keys]
            else:
                self.toppings[keys] -= topping_dict[keys]
            if self.toppings[keys] <= 0:
                del self.toppings[keys]
    
    def update_pizza_size(self, size):
        self.size = size
    
    def __str__(self):
        return '\033[1m' + "Item with ID: " + str(self.id) + '\033[0m' + "\nPizza Type: " + str(self.type) + "\nToppings: \n" + json.dumps(self.toppings, indent=4, sort_keys=True) + "\n"


class Drink(Product):

    def __init__(self, type: str, price: float, brand: str):
        Product.__init__(self, type, price)
        self.prices_given = Data.getInstance().get_prices_dict()
        self.id = None
        self.brand = brand
        self.update_prices()    

    def set_id(self, id):
        self.id = id
    
    def get_id(self):
        return self.id
    
    def update_prices(self):
        self.price = self.prices_given[self.type]
    
    def update_brand(self, brand):
        self.brand = brand

    def __str__(self):
        return '\033[1m' + "Item with ID: " + str(self.id) + '\033[0m' + "\nDrink Brand: " + str(self.brand)
    








