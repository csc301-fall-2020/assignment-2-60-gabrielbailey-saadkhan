import requests

def create_order(comm):
    ''' Sends a http request to the server to create a new order.
    Takes the user input (in format "['create_order','price']").
    Returns if the request was succesful or not.
    '''

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

    return True

def delete_order(comm):
    ''' Sends a http request to the server to delete an order.
    Takes the user input (in format "['delete_order','id']").
    Returns if the request was succesful or not.
    '''
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

    return True

if __name__ == "__main__":
    #Just loops infinitely, asking the user for input and trying to send it to the relevant function if it exists.

    command = 'None'
    while command[0] != 'exit':
        command = input('Input something: ').split()
        if command[0] == '-help':
            print('Input one of the following commands: create_order, delete_order')
        else:
            try:
                result = locals()[command[0]](command)
            except KeyError:
                print('No command matches that input, try again.')