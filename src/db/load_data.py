
import os
from db_connection import DatabaseConnection
from crud import CRUDOps
import csv
import mysql.connector # mySQL driver which allows python to communitcate with mySQL databases
from dotenv import load_dotenv # loads environment variables from .env

# path to project root (used later..)
# os.path.dirname(__file__) gets the current directory and called twice more to go up two levels (path now at root)
# data_dir then becomes a path to the data folder
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_dir = os.path.join(project_root, 'data')

def main():
    """
    main function which..:
    creates instances of the DatabaseConnection and the CRUDOps classes
    connects to the mySql server and creates a database
    creates tables
    loads data from the cvs files 
    closes the connection when done
    """
    print("Starting data loading process...")
    
    db = DatabaseConnection()
    crud = CRUDOps()

    db.connect()
    db.create_database()
    
    create_tables(crud)
    
    load_data_from_csv(crud)
    
    db.close_connection()
    
    print("Success!! .. Data loading process completed!")


def create_tables(crud):
    """
    function that creates the actual tables and relationships between them
    first drops any existing tables to prevent errors
    takes the parameter "crud" which is an instance of the CRUDOps class which was passed from the main func above
    this means that this function can be used with different crud object
    the crud object already has a database connection (established in the main function)
    creates 3 tables, customers, products and orders
    """
    print("Dropping existing tables if they exist...")
    
    crud.execute_query("DROP TABLE IF EXISTS orders")
    crud.execute_query("DROP TABLE IF EXISTS products")
    crud.execute_query("DROP TABLE IF EXISTS customers")
    
    print("Creating new tables...")
        
    # customers table
    # customer_id, customer_name, email
    customers_columns = """
        customer_id INT PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    """
    crud.create_table("customers", customers_columns)
    print("Customers table has been created")
    
    # products table
    # product_id, product_name, price
    products_columns = """
        product_id INT PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    """
    crud.create_table("products", products_columns)
    print("Products table has been created")
    
    # orders table with foreign keys
    # order_id, date_time
    # customer_id, product_id which are foreign keys, linked to the other tables
    orders_columns = """
        id INT PRIMARY KEY,
        date_time DATETIME NOT NULL,
        customer_id INT NOT NULL,
        product_id INT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    """
    crud.create_table("orders", orders_columns)
    print("Orders table has now been created with foreign key relationships.")

def load_data_from_csv(crud):
    """
    function that loads data from CSV files into the database tables
    takes "crud" as a parameter (same reasons as above)
    this function calls three functions in a specific order which in turn load cvs data into each table
    """

    print("Now loading customers data...")
    load_customers(crud)
    
    print("Now loading products data...")
    load_products(crud)
    
    print("Now loading orders data...")
    load_orders(crud)
    
    print("Yay, all data has been loaded successfully!")


def load_customers(crud):
    """
    function neccesary for loading customers data from the CSV file
    first establishes the path to the CSV with the data_dir variable which contains the path
    
    next the CSV file is opened in read mode
    then a CVS reader object is created using csv.reader
    "next" tells the iterator to skip the first row in the reader object (headers)
    
    a for loop then process each row of the CSV file
    -> it assigns each element of the row list to a seperate variable (=unpacking)
    with crud.insert_data(...) the crud operation is called to insert the data into the database
    first parameter is table name, second is column names, and lastly the tuple of values to insert
    the crud operation then handles the sql commands and execution
    """

    customers_file = os.path.join(data_dir, 'customers.csv')

    with open(customers_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)        
            next(csv_reader)
            
            for row in csv_reader:
                id, name, email = row
                
                crud.insert_data(
                    "customers",  
                    "customer_id, customer_name, email",  
                    (id, name, email) 
                )

def load_products(crud):
    """
    Load products data from CSV file.
    follows similar operation as explained above, just pertaining to products 
    """

    products_file = os.path.join(data_dir, 'products.csv')
    
    with open(products_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        
        for row in csv_reader:
            id, name, price = row
            
            crud.insert_data(
                "products",  
                "product_id, product_name, price",  
                (id, name, price)  
            )


def load_orders(crud):
    """
    function has loads orders data from CSV file
    follows similar operation as explained above, just pertaining to orders
    """

    orders_file = os.path.join(data_dir, 'orders.csv')
    
    with open(orders_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        
        for row in csv_reader:            
            id, date_time, customer, product = row

            crud.insert_data(
                "orders", 
                "id, date_time, customer_id, product_id", 
                (id, date_time, customer, product)  
            )


if __name__ == "__main__":
    main()
