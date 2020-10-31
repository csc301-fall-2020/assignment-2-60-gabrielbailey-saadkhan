
class Item:
    '''The information representing an item in an order'''
    
    def __init__(self, price):
        self.price = price

# Still unsure about the format of the types. They also need to be updated.
p_types = ['Pepperoni', 'Margherita', 'Vegetarian', 'Neapolitan']
p_toppings = ['olives', 'tomatoes', 'mushrooms', 'jalapenos', 'chicken', 'beef', 'pepperoni']
d_types = {'Coke':1.50, 'Diet Coke':1.60, 'Coke Zero':1.40, 'Pepsi':1.50, 'Diet Pepsi':1.40, 'Dr. Pepper':1.50, 'Water':0.0, 'Juice':1.00}

class Pizza(Item):
    '''The information representing a pizza in an order.
     Includes:
     price
     size
     type
     toppings'''

    def __init__(self, price, p_type, toppings, size):
        Item.__init__(self, price) 
        
        self.size = size
        self.type = p_type
        self.toppings = toppings

class Drink(Item):
    '''The information representing a pizza in an order'''

    def __init__(self, price, d_type):
        Item.__init__(self, price) 
        
        self.type = d_type