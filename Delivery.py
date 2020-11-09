import csv
import json


class Delivery:
    '''A delivery from a pizza parlor
    '''

    def __init__(self, order_number, address = '', type = 'pickup'):
        self.order_number = order_number
        self.address = address
        self.type = type

    def ubereats_deliver(self, details):
        '''Generates the json files that foodora requires
        '''

        jsonfile = open('data.json', 'w')
        #order_details = {}
        #for item in order:
        #    order_details['Item']

        data = {
            'Address':self.address,
            'Order Details':details,
            'Order Number':self.order_number
            }
        json.dump(data, jsonfile)

        # Should we send this file anywhere?

        return 'Uber Eats will deliver your order'

    def foodora_deliver(self, details):
        '''Generates the csv files that foodora requires
        '''

        csvfile = open('delivery.csv', 'w', newline='')
        csvwriter = csv.writer(csvfile)



        csvwriter.writerow([self.address])
        csvwriter.writerow([details])
        csvwriter.writerow([str(self.order_number)])

        # Should we send this file anywhere?

        return 'Foodora will deliver your order'

    def deliver(self, details):
        ''' "sends" a delivery base on this delivery's type and order.
        '''

        if self.type == 'pickup':
            return 'You can pickup your order from the store.'
        elif self.type == 'pizzaparlour':
            return 'We will deliver your order shortly.'
        elif self.type == 'ubereats':
            return self.ubereats_deliver(details)
        elif self.type == 'foodora':
            return self.foodora_deliver(details)
        else:
            return 'Delivery type unknown. You can pickup your order from the store.'

# Just using these strings for now
# types = ['pickup', 'pizzaparlour', 'ubereats', 'foodora']

# if __name__ == "__main__":
#     # The following is just testing
#     items = ['A','B','C']
#     order = Order(1,items)
#     delivery1 = Delivery(order, '123 Somewhere Lane', 'foodora')
#     delivery2 = Delivery(order, '321 Somewhere Lane', 'ubereats')
#     print(delivery1.deliver())
#     print(delivery2.deliver())