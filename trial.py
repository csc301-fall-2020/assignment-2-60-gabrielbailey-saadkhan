from Order import OrderFactory
from Product import Pizza

pizza_type_dict = {
    "1": "vegetarian_pizza",
    "2": "pepperoni_pizza",
    "3": "margherita_pizza",
    "4": "neapolitan_pizza",
    "5": "custom_pizza"
}

pizza_size_dict = {
    "1": "small",
    "2": "medium",
    "3": "large",
    "4": "x-large"
}
order_fac = OrderFactory()

def get_valid_order_number():
    order_number = input("Type a valid order number for this request: ")
    order_number_int = int(order_number)
    order = order_fac.is_valid_order_number(order_number_int)
    while order is None:
        order_number = input("Invalid Order Number. Please type a valid order number for this request: ")
        order_number_int = int(order_number)
        order = order_fac.is_valid_order_number(order_number_int)
    return order_number_int

def get_valid_item_number(order_number):
    item_number = input("Type a valid item number for this request or type 0 to see all items in this order: ")
    item_number_int = int(item_number)
    item = order_fac.get_item_in_order_by_id(order_number, item_number_int)
    while item_number_int == 0 or item is None:
        if item_number_int == 0:
            print(order_fac.get_order(order_number))
            item_number = input("Now type a valid item number: ")
        else:
            item_number = input("Invalid item number. Please type a valid item number: ")
        item_number_int = int(item_number)
        item = order_fac.get_item_in_order_by_id(order_number, item_number_int)
    return item_number_int

def decide_item_to_edit(order_number, item_number):
    if order_fac.is_pizza(order_number, item_number) == "True":
        edit_pizza(order_number, item_number)

def edit_pizza(order_number, item_number):
    print("Enter 1 to edit Pizza Type")
    print("Enter 2 to edit Pizza Size")
    print("Enter 3 to edit Pizza Toppings")
    print("Enter 4 to cancel")
    choice = input("Please enter your choice: ")
    while choice not in ["1", "2", "3", "4"]:
        choice = input("Please enter a valid choice: ")
    if choice == "4":
        return 
    if choice == "1":
        edit_pizza_type(order_number, item_number)
    elif choice == "2":
        edit_pizza_size(order_number, item_number)
    elif choice == "3":
        edit_pizza_toppings(order_number, item_number)

def edit_pizza_type(order_number, item_number):
    print("Enter 1 if you would like to change this pizza to a Vegetarian Pizza")
    print("Enter 2 if you would like to change this pizza to a Pepperoni Pizza")
    print("Enter 3 if you would like to change this pizza to a Margherita Pizza")
    print("Enter 4 if you would like to change this pizza to a Neopolitan Pizza")
    print("Enter 5 if you would like to change this pizza to a Custom Pizza")
    print("Enter 6 to cancel")
    pizza_type = input("Enter your choice: ")
    while pizza_type not in ["1", "2", "3", "4", "5", "6"]:
        pizza_type = input("Invalid input. Enter choice again: ")
    if pizza_type == "6":
        return
    order_fac.update_item(order_number, item_number, "type", pizza_type_dict[pizza_type])

def edit_pizza_size(order_number, item_number):
    print("Enter 1 if you would like to change this pizza to a small size pizza")
    print("Enter 2 if you would like to change this pizza to a medium size pizza")
    print("Enter 3 if you would like to change this pizza to a large size pizza")
    print("Enter 4 if you would like to change this pizza to a x-large size pizza")
    print("Enter 5 to cancel")
    pizza_size = input("Enter your choice: ")
    while pizza_size not in ["1", "2", "3", "4", "5"]:
        pizza_size = input("Invalid input. Enter choice again: ")
    if pizza_size == "5":
        return
    order_fac.update_item(order_number, item_number, "size", pizza_size_dict[pizza_size])

def edit_pizza_toppings(order_number, item_number):
    print("Here are the current toppings in this pizza: ")
    print(order_fac.get_toppings(order_number, item_number))
    print("Enter add if you would like to add toppings")
    print("Enter remove if you would like to remove toppings")
    print("Enter cancel to cancel")
    add_or_remove = input("Enter your choice: ")
    while add_or_remove not in ["add", "remove", "cancel"]:
        add_or_remove = input("Invalid input. Enter choice again: ")
    if add_or_remove == "cancel":
        return
    toppings = custom_pizza_route()
    order_fac.update_item(order_number, item_number, "toppings", toppings, add_or_remove)
    


def create_new_pizza(order_number):
    toppings_list = None
    print("Enter 1 if you would like a Vegetarian Pizza")
    print("Enter 2 if you would like a Pepperoni Pizza")
    print("Enter 3 if you would like a Margherita Pizza")
    print("Enter 4 if you would like a Neopolitan Pizza")
    print("Enter 5 if you would like a Custom Pizza")
    print("Enter 6 to cancel")
    pizza_type = input("Enter your choice: ")
    while pizza_type not in ["1", "2", "3", "4", "5", "6"]:
        pizza_type = input("Invalid input. Enter choice again: ")
    if pizza_type == "5":
        toppings_list = custom_pizza_route()
        if toppings_list is None:
            return
    if pizza_type == "6":
        return
    print("Enter 1 if you would like a small size pizza")
    print("Enter 2 if you would like a medium size pizza")
    print("Enter 3 if you would like a large size pizza")
    print("Enter 4 if you would like a x-large size pizza")
    print("Enter 5 to cancel")
    pizza_size = input("Enter your choice: ")
    while pizza_size not in ["1", "2", "3", "4", "5"]:
        pizza_size = input("Invalid input. Enter choice again: ")
    if pizza_size == "5":
        return
    quantity = input("Enter quantity needed: ")
    items = []
    for i in range(0, int(quantity)):
        items.append(Pizza(pizza_type_dict[pizza_type], 0, pizza_size_dict[pizza_size], toppings_list))
    print(order_fac.add_to_order(order_number, items))

def custom_pizza_route():
    toppings = ["olives", "jalapenos", "tomatoes", "mushroom", "chicken", "beef", "pepperoni"]
    print(toppings)
    to_return = []
    topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings wrtie 'done'. Type cancel to exit: ")
    while topping != "done":
        while topping not in toppings and topping != "cancel":
            topping = input("You have entered an invalid topping. Check your spelling. Type cancel to exit: ")
        if topping == "cancel":
            return None
        quantity = input("Enter the quantity of the topping: ")
        for i in range(0, int(quantity)):
            to_return.append(topping)
        topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings wrtie 'done'. Type cancel to exit:  ")
    return to_return



while(True):
    print("Enter 1 to create new Order")
    print("Enter 2 to create new pizza")
    print("Enter 3 to update an order")
    choice = input("Enter your choice: ")
    if choice == "1":
        print(order_fac.create_new_order())
    elif choice == "2":
        create_new_pizza(get_valid_order_number())
    elif choice == "3":
        order_number = get_valid_order_number()
        item_number = get_valid_item_number(order_number)
        decide_item_to_edit(order_number, item_number)




