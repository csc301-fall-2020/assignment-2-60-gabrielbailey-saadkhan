

import requests

# TODO These two dictionaries need to be base on the json files, and have update functions
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
url = 'http://127.0.0.1:5000'

def get_valid_order_number():    
    path = '/new_order'
    order_number = requests.get(url+path)

    return int(order_number.text)

def get_valid_item_number(order_number):

    item_number = int(input("Type a valid item number for this request or type 0 to see all items in this order: "))
    path = '/get_item'
    response = requests.get(url+path+'/'+str(order_number)+'/'+str(item_number))
    item = response.text
    while item_number == 0 or item is None:
        if item_number == 0:
            response = requests.get(url+'/get_order'+'/'+str(order_number))
            print(response.text)
            item_number = int(input("Now type a valid item number: "))
        else:
            item_number = int(input("Invalid item number. Please type a valid item number: "))
        response = requests.get(url+path+'/'+str(order_number)+'/'+str(item_number))
        item = response.text
    return item_number

def decide_item_to_edit(order_number, item_number):
    path = '/item_type'
    is_pizza = requests.get(url+path+'/'+str(order_number)+'/'+str(item_number)).content
    # ^This should be item type probably
    if is_pizza:
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
    pt_len = len(pizza_type_dict)
    for i in range(1,pt_len+1):
        print("Enter "+str(i)+" if you would like to change this pizza to a "+pizza_type_dict[str(i)][:-6]+" Pizza")
    print("Enter "+str(pt_len+1)+" to cancel")
    pizza_type = input("Enter your choice: ")
    while pizza_type not in [str(i) for i in range(1,pt_len+2)]:
        pizza_type = input("Invalid input. Enter choice again: ")
    if pizza_type == str(pt_len):
        return
    path = '/update_pizza'
    data = {'order_number': order_number, 'item_number':item_number, 'type': pizza_type_dict[pizza_type]}
    requests.post(url+path+'/type', data = data)

def edit_pizza_size(order_number, item_number):
    ps_len = len(pizza_size_dict)
    for i in range(1,ps_len+1):
        print("Enter "+str(i)+" if you would like to change this pizza to a "+pizza_size_dict[str(i)]+" size pizza")
    print("Enter 5 to cancel")
    pizza_size = input("Enter your choice: ")
    while pizza_size not in [str(i) for i in range(1,ps_len+2)]:
        pizza_size = input("Invalid input. Enter choice again: ")
    if pizza_size == str(ps_len):
        return
    path = '/update_pizza'
    data = {'order_number': order_number, 'item_number':item_number, 'size': pizza_size_dict[pizza_size]}
    requests.post(url+path+'/size', data = data)

def edit_pizza_toppings(order_number, item_number):
    print("Here are the current toppings in this pizza: ")
    path = '/toppings'
    print(requests.get(url+path+'/'+str(order_number)+'/'+str(item_number)))
    print("Enter add if you would like to add toppings")
    print("Enter remove if you would like to remove toppings")
    print("Enter cancel to cancel")
    add_or_remove = input("Enter your choice: ")
    while add_or_remove not in ["add", "remove", "cancel"]:
        add_or_remove = input("Invalid input. Enter choice again: ")
    if add_or_remove == "cancel":
        return
    toppings = custom_pizza_route()
    path = '/update_pizza'
    data = {'order_number': order_number, 'item_number':item_number, 'toppings': toppings, 'add_or_remove': 'add_or_remove' }
    requests.post(url+path+'/toppings', data = data)
    


def create_new_pizza(order_number):
    toppings_list = None
    pt_len = len(pizza_type_dict)
    for i in range(1,pt_len+1):
        print("Enter "+str(i)+" if you would like a "+pizza_type_dict[str(i)][:-6]+" Pizza")
    print("Enter "+str(pt_len+1)+" to cancel")
    pizza_type = input("Enter your choice: ")
    while pizza_type not in [str(i) for i in range(1,pt_len+2)]:
        pizza_type = input("Invalid input. Enter choice again: ")
    if pizza_type_dict[pizza_type] == 'custom_pizza':
        toppings_list = custom_pizza_route()
        if toppings_list is None:
            return
    if pizza_type == str(pt_len+1):
        return

    ps_len = len(pizza_size_dict)
    for i in range(1,ps_len+1):
        print("Enter "+str(i)+" if you would like a "+pizza_size_dict[str(i)]+" size pizza")
    print("Enter "+str(ps_len+1)+" to cancel")
    pizza_size = input("Enter your choice: ")
    while pizza_size not in [str(i) for i in range(1,ps_len+2)]:
        pizza_size = input("Invalid input. Enter choice again: ")
    if pizza_size == str(ps_len+1):
        return

    quantity = input("Enter quantity needed: ")
    path = '/create_pizza'
    data = {'order_number': order_number, 'quantity':quantity, 'pizza_type':pizza_type_dict[pizza_type], 'pizza_size': pizza_size_dict[pizza_size], 'toppings': toppings_list}
    print(requests.post(url+path, data = data).text)

def custom_pizza_route():
    toppings = ["olives", "jalapenos", "tomatoes", "mushroom", "chicken", "beef", "pepperoni"]
    #print(toppings)
    for i in range(1,len(toppings)+1):
        print("Enter "+str(i)+" if you would like "+toppings[i]+" on your pizza")
    print("Enter "+(len(toppings)+1)+" if you are finished adding toppings")
    print("Enter "+(len(toppings)+2)+" to cancel and exit adding toppings")
    topping = input("Enter your choice: ")
    to_return = []
    #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings wrtie 'done'. Type cancel to exit: ")
    while topping != str(len(toppings)+1):
        while topping not in toppings and topping != "cancel":
            topping = input("Invalid input. Enter choice again: ")
        if topping == str(len(toppings)+2):
            return None
        quantity = input("Enter the quantity of the topping: ")
        for i in range(0, int(quantity)):
            to_return.append(topping)
        topping = input("Enter your choice: ")
        #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings write 'done'. Type cancel to exit:  ")
    return to_return



while(True):
    print("Enter 1 to create new Order")
    print("Enter 2 to create new pizza")
    print("Enter 3 to update an order")
    choice = input("Enter your choice: ")
    if choice == "1":
        print(requests.get(url+'/create_order').text)
    elif choice == "2":
        create_new_pizza(get_valid_order_number())
    elif choice == "3":
        order_number = get_valid_order_number()
        item_number = get_valid_item_number(order_number)
        decide_item_to_edit(order_number, item_number)




