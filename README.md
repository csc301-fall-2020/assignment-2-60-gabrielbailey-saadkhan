# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`


Pair Programming Features:
1. Submit an order
	Includes implementing all the objects that define an order/pizza/drink
2. Ask for Pickup or Delivery
	Includes implementing reading of JSON and csv filetypes

3. Update existing order/ Cancel Order
	Needs to be taken into consideration during 1. but should then be quick?
4. Ask for the menu
	Either the full menu or price of an item. Details up to us so can be short?

Suggest 1 & 2 for the two pair programming sessions. If you have modifications, make them, and if you would rather be driver or navigator for one of them, claim them.

--------
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