import csv
import json

class Order:
   '''A dummy order class to use while the real one is unknown'''

   def __init__(self, id, items):
       self.id = id
       self.items = items

class Delivery:
    '''A delivery from a pizza parlor
    '''

    def __init__(self, order, address, type = 'pickup'):
        self.order = order
        self.address = address
        self.type = type

    def ubereats_deliver(self):
        '''Generates the json files that foodora requires
        '''

        jsonfile = open('data.json', 'w')
        #order_details = {}
        #for item in order:
        #    order_details['Item']
        data = {
            'Address':self.address,
            'Order Details':self.order.items,
            'Order Number':self.order.id
            }
        json.dump(data, jsonfile)

        # Should we send this file anywhere?

        return 'Uber Eats will deliver your order'

    def foodora_deliver(self):
        '''Generates the csv files that foodora requires
        '''

        csvfile = open('delivery.csv', 'w', newline='')
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow([self.address])
        for item in self.order.items:
            #Maybe this should be one line?
            csvwriter.writerow([str(item)])
        csvwriter.writerow([str(self.order.id)])

        # Should we send this file anywhere?

        return 'Foodora will deliver your order'

    def deliver(self):
        ''' "sends" a delivery base on this delivery's type and order.
        '''

        if self.type == 'pickup':
            return 'You can pickup your order from the store.'
        elif self.type == 'pizzaparlour':
            return 'We will deliver your order shortly.'
        elif self.type == 'ubereats':
            return self.ubereats_deliver()
        elif self.type == 'foodora':
            return self.foodora_deliver()
        else:
            return 'Delivery type unknown. You can pickup your order from the store.'

# Just using these strings for now
# types = ['pickup', 'pizzaparlour', 'ubereats' 'foodora']

if __name__ == "__main__":
    # The following is just testing
    items = ['A','B','C']
    order = Order(1,items)
    delivery1 = Delivery(order, '123 Somewhere Lane', 'foodora')
    delivery2 = Delivery(order, '321 Somewhere Lane', 'ubereats')
    print(delivery1.deliver())
    print(delivery2.deliver())