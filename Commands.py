import requests
import Item, Order

users = ['hello']
command = ['none']

def create_order(comm):
    if len(comm) < 2:
        print('Not enough arguments were input. Type "create_order -help" for more information.')
        return False
    if comm[1] == '-help':
        print('Create an order with a given price. Example: create_order 3.50')
        return False

    price = float(comm[1])
    url = 'http://127.0.0.1:5000/create_order'
    myobj = {'price': price}

    response = requests.post(url, data = myobj)

    print(response.text)

    #print('New order with price %s!' % price) 
    return True

def delete_order(comm):
    if len(comm) < 2:
        print('Not enough arguments were input. Type "delete_order -help" for more information.')
        return False
    if comm[1] == '-help':
        print('Delete an order with a given id. Example: delete_order 4')
        return False

    id = int(comm[1])
    url = 'http://127.0.0.1:5000/delete_order/'+str(id)
    #myobj = {'price': price}

    response = requests.post(url)

    print(response.text)

    #print('New order with price %s!' % price) 
    return True

if __name__ == "__main__":
    while command[0] != 'exit':
        command = input('input something: ').split()
        try:
            result = locals()[command[0]](command)
        except KeyError:
            print('No command matches that input, try again.')