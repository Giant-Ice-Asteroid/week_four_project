from db.db_connection import DatabaseConnection
import mysql.connector # mySQL driver which allows python to communitcate with mySQL databases
from dotenv import load_dotenv # loads environment variables from .env
import os # allows interaction with the os, including reading environment variables


def main():
    """
    Main function to set up the database.
    main func keeps variables within a local scope
    """
    
    db = DatabaseConnection() # this creates a database connection instance
        
    db.connect() # connects to the MySQL server
        
    db.create_database() # creates the database if it doesnt exist yet
    
    db.close_connection() #closes connection
    
    print("Database setup is complete ^_^")

if __name__ == "__main__": # if run directly calls main()
    main()