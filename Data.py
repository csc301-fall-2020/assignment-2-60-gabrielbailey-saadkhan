import json

class Data:

    prices = {}
    size_to_price_qualifier = {}
    pizza_to_toppings = {}
    __instance = None
    
    @staticmethod
    def getInstance():
        if Data.__instance == None:
            Data()
        return Data.__instance
        
    def __init__(self):
        """ Virtually private constructor. """
        if Data.__instance == None:
            Data.__instance = self
            self.read_prices()
            self.read_qualifiers()
            self.read_pizza_to_toppings()

    @staticmethod
    def read_prices():
        with open('prices.json') as f:
            Data.prices = json.load(f)

    @staticmethod
    def read_qualifiers():
        with open('size_to_price.json') as f:
            Data.size_to_price_qualifier = json.load(f)

    @staticmethod
    def read_pizza_to_toppings():
        with open('pizza_to_toppings.json') as f:
            Data.pizza_to_toppings = json.load(f)
    
    @staticmethod
    def get_prices_dict():
        return Data.prices
    
    @staticmethod
    def get_size_qualifier():
        return Data.size_to_price_qualifier
    
    @staticmethod
    def get_pizza_to_toppings():
        return Data.pizza_to_toppings
    
    @staticmethod
    def update_all():
        Data.read_prices()
        Data.read_qualifiers()
        Data.read_pizza_to_toppings()

    @staticmethod
    def set_price(name, price):
        with open('prices.json', 'w') as f:
            try:
                Data.prices[name] = price
                json.dump(Data.prices, f, indent=4)
            except:
                return False
        return True
    