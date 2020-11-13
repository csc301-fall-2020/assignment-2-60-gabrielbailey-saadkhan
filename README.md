# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run the CLI by running `python3 trial.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

The CLI is made up of several menues whish should be mostly self-explanatory. The main menu is:

Enter 1 to create a new order
Enter 2 to add products to an order
Enter 3 to update an order
Enter 4 to cancel an order
Enter 5 for delivery options
Enter 6 to display all orders
Enter 7 to change prices
Enter 8 to exit

The options that might need clarification:
1 creates a new, empty order. It must have products added to it seperately.
5 simply adds delivery data to an order, and if the delivery is by an external member, creates the requisite json or csv file titled delivery.
7 changes the prices of base elements and updates the price of all orders with that information. Information regarding price and items is stored in json files, so is persistent.

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

Pair Programming Features:

    Should explain which features were pair programmed
    Should explain who the driver and navigator was for different parts of the features
    Should give a reflection on how it went, and what you liked and disliked about this process

We didn't entirely realize we were supposed to be flipping, so we only did 1 long session for each of us.

1. Submit an Order/Cancel Order
	Just the order & order number, without details. Includes getting the program and unittesting to work.
	Driver: Gabriel
	Navigator: Saad
A lot of time was spent just figuring out what was wanted from A2. There was ambiguity in the handout. We figured out that it was supposed to be a CLI that cantacted a flask server that performed all backend calculations. Setting this up took much longer than anticipated, so we didn't have a functional program by the time the pair programming time expired. Thus Gabriel spent some time alone finishing task 1 up before pushing it.

Gabriel: I found being the driver to be extremely stressful. Normally I just look up basic classes or syntax that I forget, but it felt like it would be embarassing in this environment. This feature especially took a lot of time, a lot more than was anticipated. It included setting up the project, and there was uncertainty about what the project structure should even be.
	
2. Add Info to Orders
	Includes implementing all the objects and classes that define an order/pizza/drink
	Driver: Saad
	Navigator: Gabriel
Once again there was some confusion of how the program was to be structured. Gabriel mistakenly thought that a database would provide bonus marks and had set one up for task 1, but we agreed it would be easier to just use in-memory objects and maybe some json files for persistence if needed. This transition once again made the length of task 2 much longer than anticipated, and Saad had to spend time finishing it alone before pushing it.

Gabriel: It was hard to be useful without direct access to the code being worked on. After high-level decisions are made, there isn't much to do while "navigating".

The rest of the features were worked on seperately.

Tools:
-We used pylint primarly to achieve consistent code style.

Design Patterns:
-?