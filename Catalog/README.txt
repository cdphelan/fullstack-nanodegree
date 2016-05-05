##TO RUN THIS PROJECT##

Prereqs: These instructions assume that you already have an environment prepped with all the necessary modules (Flask, SQLAlchemy, etc.)

1) Run: python database_setup.py
	Initializes the database 

2) Run: python db-apocalypse-populator.py
	Populates the database with books. Make sure you have the file apocalypse-books.csv, or the code will fail!

3) Run: python application.py
	Starts the app on a local server.

4) Navigate to localhost:5000 in your browser.

5) Enjoy! 

Notice that Genres are not editable; only Subgenres and Books are.