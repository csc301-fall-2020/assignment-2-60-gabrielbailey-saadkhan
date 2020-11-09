# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

run the CLI by running `python3 trial.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

The CLI is made up of several menues. The main menu is:

Enter 1 to create a new order
Enter 2 to add products to an order
Enter 3 to update an order
Enter 4 for delivery options
Enter 5 to display all orders
Enter 6 to exit

1 creates a new, empty order.
2 is used to add products to those orders
	Creating new custom pizzas is contained in this option
3 is used to modify orders that already have information
4 is used to add delivery information to an order

TODO:
-Add more meaningful tests for create_order and delete_order, especially for the commands side of things.
-Add more meaningful output and return values for the Commands functions (?)
-Seperate flask blueprints into another file.
-Fix Commands crashing for certain bad input or bad http request responses


Thought the features might be too big, and prof said "you might have 5 or 10 features...", so I've split them down further. Even if this is too small we can still use it as a guidline for incremental work in larger paired programming features.
Again, feel free to modify.

Program Features:
1. Submit an Order/Cancel Order
	Just the order & order number, without details. Includes getting the program and unittesting to work.
2. Add Info to Orders
	Includes implementing all the objects and classes that define an order/pizza/drink
3. Update existing order 
	Includes how request is formatted. Kinda short: merge with 2?
4. Ask for Pickup or Delivery
	Just pickup from store and inhouse delivery
5. Ask for Uber Eats Delivery
	Includes implementing writing to JSON
6. Ask for Foodora Delivery
	Includes implementing writing to csv
7. Ask for the Full Menu
	Details up to us so can be short?
8. Ask for the price of an Item
	Includes coming up with pricing.

Bonus Features:
- Non-command line UI or API
- Storage of info of session using SQLAlchemy or whatever

Pair Programming Features:

    Should explain which features were pair programmed
    Should explain who the driver and navigator was for different parts of the features
    Should give a reflection on how it went, and what you liked and disliked about this process

1. Submit an Order/Cancel Order
	Just the order & order number, without details. Includes getting the program and unittesting to work.
	Driver: Gabriel
	Navigator: Saad
Gabriel: I found being the driver to be extremely stressful. Normally I just look up basic classes or syntax that I forget, but it felt like it would be embarassing in this environment. This feature especially took a lot of time, a lot more than was anticipated. It included setting up the project, and there was uncertainty about what the project structure should even be.
	