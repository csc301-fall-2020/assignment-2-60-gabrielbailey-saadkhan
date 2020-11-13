

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

def get_new_order_number():    
    path = '/new_order'
    order_number = requests.get(url+path)

    return int(order_number.text)

def get_valid_order_number():
    err = ""
    path = '/order_is_valid'
    order_number=-1
    while order_number <0 or not requests.get(url+path+'/'+str(order_number)).text == 'True':
        order_number = input(err+"Type a valid order number for this request: ")
        while type(order_number) != int:
            try:
                order_number = int(order_number)
            except ValueError:
                order_number = input("Invalid Order Number. Please type a valid order number for this request: ")
        err = "Not a current order. "
                
    return order_number

def get_item(order_number, item_number):
    if type(order_number) != int or type(item_number)!=int:
        return 'Those are not valid ids: '+str(order_number)+', '+str(item_number)
    path = '/get_item'
    response = requests.get(url+path+'/'+str(order_number)+'/'+str(item_number))
    return(response.text)

def get_order(order_number):
    path = '/get_order'
    response = requests.get(url+path+'/'+str(order_number))
    return(response.text)

def get_valid_item_number(order_number):
    if type(order_number) != int:
        return "This order number is invalid: "+str(order_number)
    path = '/get_item'
    item = "None"
    item_number = input("Type a valid item number for this request or type 0 to see all items in this order: ")
    while type(item_number)!=int or item_number == 0 or item == "None":
        try:
            item_number = int(item_number)
            if item_number == 0:
                response = requests.get(url+'/get_order'+'/'+str(order_number))
                print(response.text)
                item_number = input("Now type a valid item number for this request or type 0 to see all items in this order: ")
            else:
                response = requests.get(url+path+'/'+str(order_number)+'/'+str(item_number))
                item = response.text
                if item == "None":
                    item_number = input("Invalid Item Number")
        except ValueError:
            item_number = input("Invalid item number. Please type a valid item number: ")
    return item_number

def decide_item_to_edit(order_number, item_number):
    path = '/item_type'
    is_pizza = requests.get(url+path+'/'+str(order_number)+'/'+str(item_number)).content
    
    # ^This should be item type probably
    if is_pizza:
        edit_pizza(order_number, item_number)
    else:
        edit_drink(order_number, item_number)

def edit_drink(order_number, item_number):
    print("Enter 1 to edit Drink Brand")
    print("Enter 2 to cancel")
    choice = input("Enter your choice: ")
    while choice not in ["1", "2"]:
        choice = input("Please enter a valid choice: ")
    if choice == "2":
        return 
    if choice == "1":
        edit_drink_brand(order_number, item_number)

def edit_drink_brand(order_number, item_number):
    path = '/update_drink'
    drink_brands = ["Coke", "Diet Coke", "Coke Zero", "Pepsi", "Diet Pepsi", "Dr. Pepper", "Water", "Juice"]
    for i in range(1,len(drink_brands)+1):
        print("Enter "+str(i)+" if you would like to change drink brand to "+ str(drink_brands[i - 1]))
    print("Enter "+str(len(drink_brands)+1)+" to cancel and exit")
    drinks = input("Enter your choice: ")
    #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings wrtie 'done'. Type cancel to exit: ")
    while drinks not in [str(i) for i in range(1,len(drink_brands)+2)]:
        drinks = input("Invalid input. Enter choice again: ")
    if drinks == str(len(drink_brands)+1):
        return None    
    data = {'order_number': order_number, 'item_number':item_number, 'drink_brand':drink_brands[int(drinks) - 1]}
    requests.post(url+path+'/brand', data = data).text

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
    path = '/get_toppings'
    print(requests.get(url+path+'/'+str(order_number)+'/'+str(item_number)))
    print("Enter 1 if you would like to add toppings")
    print("Enter 2 if you would like to remove toppings")
    print("Enter 3 to cancel")
    add_or_remove = input("Enter your choice: ")
    while add_or_remove not in ["1", "2", "3"]:
        add_or_remove = input("Invalid input. Enter choice again: ")
    if add_or_remove == "3":
        return
    elif add_or_remove == "1":
        add_or_remove = "add"
    else: 
        add_or_remove = "remove"
    toppings = custom_pizza_route(add_or_remove)
    path = '/update_pizza'
    data = {'order_number': order_number, 'item_number':item_number, 'toppings': ",".join(toppings), 'add_or_remove': add_or_remove }
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
    if pizza_type == str(pt_len+1):
        return
    if pizza_type_dict[pizza_type] == 'custom_pizza':
        toppings_list = custom_pizza_route()
        
        if toppings_list is None:
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
    while type(quantity) != int:
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = input("Invalid quantity. Please enter a number: ")
    
    path = '/create_pizza'
    print(toppings_list)
    data = {'order_number': order_number, 'quantity':quantity, 'pizza_type':pizza_type_dict[pizza_type], 'pizza_size': pizza_size_dict[pizza_size], 'toppings': toppings_list}
    print(requests.post(url+path, data = data).text)

def custom_pizza_route(add_or_remove = "add"):
    toppings = ["olives", "jalapenos", "tomatoes", "mushroom", "chicken", "beef", "pepperoni"]
    #print(toppings)
    cond_words = [' add ',' on ',' adding '] if add_or_remove == "add" else [' remove ',' from ',' removing ']
    for i in range(1,len(toppings)+1):
        print("Enter "+str(i)+" if you would like to"+cond_words[0]+toppings[i-1]+cond_words[1]+"your pizza")
    print("Enter "+str(len(toppings)+1)+" if you are finished"+cond_words[2]+"toppings")
    print("Enter "+str(len(toppings)+2)+" to cancel and exit"+cond_words[2]+"toppings")
    topping = input("Enter your choice: ")
    to_return = []
    #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings wrtie 'done'. Type cancel to exit: ")
    while topping != str(len(toppings)+1):
        while topping not in [str(i) for i in range(1,len(toppings)+3)]:
            topping = input("Invalid input. Enter choice again: ")
        if topping == str(len(toppings)+2):
            return None
        if topping == str(len(toppings)+1):
            return to_return
        quantity = input("Enter the quantity of the topping: ")
        while type(quantity) != int:
            try:
                quantity = int(quantity)
            except ValueError:
                quantity = input("Invalid quantity. Please enter a number: ")
        for i in range(0, int(quantity)):
            temp = int(topping) - 1
            to_return.append(toppings[temp])
            print(to_return)
        topping = input("Enter your choice: ")
        #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings write 'done'. Type cancel to exit:  ")
    return to_return

def create_delivery(order_number):
    address = input('Enter your address: ')
    types = ['pickup', 'pizzaparlour', 'ubereats', 'foodora']

    print('Enter 1 to pick it up from the store')
    print('Enter 2 to have it delivered by PizzaParlour')
    print('Enter 3 to have it delivered by Uber Eats')
    print('Enter 4 to have it delivered by Foodora')
    delivery_type = input('Enter your choice: ')
    while delivery_type not in [str(i) for i in range(1,5)]:
        delivery_type = input('Not a valid choice. Enter another: ')
    
    path = '/create_delivery'
    data = {'address': address, 'delivery_type':types[int(delivery_type)-1] }
    return requests.post(url+path+'/'+str(order_number), data = data).text


def create_drink(order_number):
    path = '/create_drink'
    drink_brands = ["Coke", "Diet Coke", "Coke Zero", "Pepsi", "Diet Pepsi", "Dr. Pepper", "Water", "Juice"]
    for i in range(1,len(drink_brands)+1):
        print("Enter "+str(i)+" if you would like a drink of brand "+ str(drink_brands[i - 1]))
    print("Enter "+str(len(drink_brands)+1)+" to cancel and exit")
    drinks = input("Enter your choice: ")
    to_return = []
    #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings wrtie 'done'. Type cancel to exit: ")
    while drinks not in [str(i) for i in range(1,len(drink_brands)+2)]:
        drinks = input("Invalid input. Enter choice again: ")
    if drinks == str(len(drink_brands)+1):
        return None
    quantity = input("Enter the quantity of the drinks: ")
    while type(quantity) != int:
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = input("Invalid quantity. Please enter a number: ")
    for i in range(0, int(quantity)):
        temp = int(drinks) - 1
        to_return.append(drink_brands[temp])
        #topping = input("Please type the ingredient that you would like from the list above. Remember the spelling must match exactly! If you are finished adding toppings write 'done'. Type cancel to exit:  ")
    data = {'order_number': order_number, 'quantity':quantity, 'drinks':to_return}
    print(requests.post(url+path, data = data).text)

def create_item():
    order_id = get_valid_order_number()
    print("Enter 1 to add a new pizza")
    print("Enter 2 to add a new drink")
    choice = input("Enter your choice: ")
    if choice == "1":
        create_new_pizza(order_id)
    if choice == "2":
        create_drink(order_id)

def remove_item(order_number, item_number):
    path = '/remove_item'
    data = {'order_number': order_number, 'item_number':item_number}
    print(requests.post(url+path, data = data).text)

def create_order():
    print(requests.get(url+'/create_order').text)

def cancel_order():
    order_number = get_valid_order_number()
    print(requests.get(url+'/cancel_order/'+str(order_number)).text)

def delivery_choices():
    order_number = get_valid_order_number()
    print(create_delivery(order_number))

def display_orders():
    path = '/get_order_list'
    print(requests.get(url+path).text)

def edit_order():
    order_number = get_valid_order_number()
    print("Enter 1 to modify an item")
    print("Enter 2 to modify the delivery")
    print("Enter 3 to remove an item from this order")
    print("Enter 4 to cancel")
    choice = input("Enter your choice: ")
    if choice == "1":
        item_number = get_valid_item_number(order_number)
        decide_item_to_edit(order_number, item_number)
    if choice == "2":
        print(create_delivery(order_number))
    if choice == "3":
        item_number = get_valid_item_number(order_number)
        remove_item(order_number, item_number)
    if choice == "4":
        return

def set_price():
    path = '/get_data/prices'
    data = requests.get(url+path).json()
    keys = list(data)
    for i in range(1,len(data)+1):
        print("Enter "+str(i)+" to change the price of "+str(keys[i-1])+": $"+str(data[keys[i-1]]))

    index = input("Enter your choice: ")
    while type(index) != int or index not in range(1,len(data)+1):
        try:
            index = int(index)
            if index not in range(1,len(data)+1):
                raise ValueError
        except ValueError:
            index = input("Invalid choice. Enter one of the numbers above: ")
    
    price = input("Enter the new price: ")
    while type(price) != float or price < 0:
        try:
            price  = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            price  = input("Invalid price. Enter a real value: ")

    path = '/set_price'
    data = {'product_name': keys[index-1], 'price':price }
    print(requests.post(url+path, data = data).text)

def exit_cli():
    #Used for indicating that orders should be saved if we get around to implementing that
    exit()

if __name__ == "__main__":
    #Update pizza types and sizes to those stored in the files
    path = '/get_data/pizza_types'
    pizza_types = list(requests.get(url+path).json())

    pizza_type_dict = {}
    for i in range(1,len(pizza_types)+1):
        pizza_type_dict[str(i)] = pizza_types[i-1]

    path = '/get_data/pizza_sizes'
    pizza_sizes = list(requests.get(url+path).json())

    pizza_size_dict = {}
    for i in range(1,len(pizza_sizes)+1):
        pizza_size_dict[str(i)] = pizza_sizes[i-1]

    #Just loops infinitely, asking the user for input and trying to send it to the relevant function if it exists.
    while(True):
        print("Enter 1 to create a new order")
        print("Enter 2 to add products to an order")
        print("Enter 3 to update an order")
        print("Enter 4 to cancel an order")
        print("Enter 5 for delivery options")
        print("Enter 6 to display all orders")
        print("Enter 7 to change prices")
        print("Enter 8 to exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_order()
        elif choice == "2":
            create_item()
        elif choice == "3":
            edit_order()
        elif choice == "4":
            cancel_order()
        elif choice == "5":
            delivery_choices()
        elif choice == "6":
            display_orders()
        elif choice == "7":
            set_price()
        elif choice == "8":
            exit_cli()




