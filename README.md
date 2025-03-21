# MySQL Python Project

A project with the aim of learning how to set up and interact with a MySQL database using Python.

## Prerequisites

- Python
- MySQL server


### Project Structure

- src: source code
    - db: database modules
            - db_connection.py: containing class for managing db connections
            - crud.py: class which can perform operations on the database
            - load_data.py: script that creates tables and loads the data into the database (actually belongs in scr, but had to go here due to module issues)
    - setup_database.py: script that sets up a database
- data: CSV data files to be loaded into the database

#### Setup Instructions

1. Clone this repository
2. Create a virtual environment ---> python -m venv .venv
3. Activate the virtual environment
4. Install dependencies ---> pip install -r requirements.txt
5. Set up environment variables (copy ".env.example" to ".env" and update values)
6. Run the setup script to set up a database ---> python src/setup_database.py
7. Next create tables and load the data into them by running --> src/db/load_data.py
8. That's it. If successful the database should now consist of three tables relating to each other (customers, products and orders tables)