import Product
from Delivery import Delivery

class OrderFactory():
    def __init__(self):
        self.count = 1
        self.orders = []
    
    def create_new_order(self):
        order = Order(self.count)
        self.orders.append(order)
        self.count += 1
        return "New Order Created with ID: " + str(order.get_order_number())

    def cancel_order(self, order_number):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            self.orders.remove(order)
            return "Order "+str(order_number)+" cancelled"
        return "This order number is invalid"

    def get_order(self, order_number):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            return order.get_order()
        return "This order number is invalid"

    def get_order_list(self):
        order_info = "Current Orders:\nID     Price"
        for order in self.orders:
            order_info += "\n" + str(order.order_number) + "    " + str(order.order_total)
        return order_info
    
    def is_valid_order_number(self, order_number):
        for order in self.orders:
            if order.order_number == order_number:
                return order
        return None
        
    def add_to_order(self, order_number, items):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            for item in items:
                order.add_item(item)
            return order.get_order()
        return "This order number is invalid"
    
    def get_item_in_order_by_id(self, order_number, item_id):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            return order.get_item_by_id(item_id)
        return "None"
    
    def is_pizza(self, order_number, item_number):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            return order.is_pizza(item_number)
        return "None"       
    
    def get_toppings(self, order_number, item_number):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            return order.get_toppings(item_number)
        return "None"
        
    def schedule_delivery(self, order_number, delivery_type, address):
        order = self.is_valid_order_number(order_number)
        if order is not None:
            return order.schedule_delivery(address, delivery_type)
        return "None"
    
    def update_item(self, order_number, item_number, to_update, value, add_or_remove=None):
        order = self.is_valid_order_number(order_number)
        return order.update_item(item_number, to_update, value, add_or_remove)
    
    def update_totals(self):
        for order in self.orders:
            order.update_all_items_price()
            order.update_total()
    
    def remove_item(self, order_number, item_number):
        order = self.is_valid_order_number(order_number)
        return order.remove_item(item_number)




class Order():

    def __init__(self, order_number):
        self.items = []
        self.order_number = order_number
        self.order_total = 0
        self.id_count = 1
        self.ids_to_items = {}
        self.delivery = None
    
    def get_order_number(self):
        return self.order_number
    
    def add_item(self, item):
        self.ids_to_items[self.id_count] = item
        item.set_id(self.id_count)
        self.id_count += 1
        self.items.append(item)
        self.update_total()
    
    def update_total(self):
        self.order_total = 0
        for items in self.items:
            self.order_total += items.price
    
    def update_all_items_price(self):
        for items in self.items:
            items.update_prices()
    
    def get_order(self):
        string = "Order ID: " + str(self.order_number) + "\nOrder Total: " + str(self.order_total) + "\nItems in Order: \n"
        for items in self.items:
            string += "\n" + str(items)
        return string
    
    def get_item_by_id(self, item_id):
        if item_id in self.ids_to_items:
            return str(self.ids_to_items[item_id])
        return "None"
    
    def is_pizza(self, item_number):
        if item_number in self.ids_to_items:
            if "pizza" in self.ids_to_items[item_number].get_type():
                return "True"
            return "False"
        return "None"

    def remove_item(self, item_number):
        temp = None
        for i in range(0, len(self.items)):
            if self.items[i].id == item_number:
                temp = i
        if temp == None:
            return "Invalid item id: item_number"
        del self.items[temp]
        del self.ids_to_items[item_number]
        self.update_total()
        return "Item with item number " + str(item_number) + " has been deleted from order number " + str(self.order_number) 
    
    def get_toppings(self, item_number):
        if self.is_pizza(item_number) == "True":
            return self.ids_to_items[item_number].get_toppings()
        else:
            return "None: not a pizza"

    def get_delivery(self):
        return self.delivery

    def schedule_delivery(self, address, delivery_type):
        self.delivery = Delivery(self.order_number, address, delivery_type)
        return self.delivery.deliver(self.items)
    
    def update_item(self, item_number, to_update, value, add_or_remove = None):
        if to_update == "type":
            self.ids_to_items[item_number].set_type(value)
            self.ids_to_items[item_number].toppings  = self.ids_to_items[item_number].set_up_toppings()
        elif to_update == "size":
            self.ids_to_items[item_number].update_pizza_size(value)
        elif to_update == "toppings":
            self.ids_to_items[item_number].update_toppings(add_or_remove, value)
        elif to_update == "brand":
            self.ids_to_items[item_number].update_brand(value)
        self.ids_to_items[item_number].update_prices()
        self.update_total()
        return self.ids_to_items[item_number]


    