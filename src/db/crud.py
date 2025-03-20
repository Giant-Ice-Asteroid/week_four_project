from db import DatabaseConnection
import mysql.connector # mySQL driver which allows python to communitcate with mySQL databases
from dotenv import load_dotenv # loads environment variables from .env
import os # allows interaction with the os, including reading environment variables

class CRUDOps:
    """
    Class which is able to handle CRUD (Create, Read, Update, Delete) operations on the database.
    """


    def __init__(self):
        """
        constructor which creates an instance of the DatabaseConnection class
        sets the connection attribute as None to start with
        """
        self.db_connection = DatabaseConnection()
        self.connection = None


    def connect(self):
        """
        method which uses the db_connection instance to make a connection
        if connection is made, checks if database exist/is created
        else returns False
        """
        self.connection = self.db_connection.connect()
        if self.connection:
            self.db_connection.create_database()
            return True
        return False
    
    def create_table(self, table_name, columns):
        """
        method that creates a table in the database
        first ensures that connection is made
        then creates a cursor object to execute sql commands
        creates sql query that creates table if none exists
        lastly cursor executes the query and changes are commited + confirmation printed
        """
        if self.connection is None:
            self.connect()
        
        cursor = self.connection.cursor()
                
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        )
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        print(f"Yay! Table '{table_name}' created successfully")

    def insert_data(self, table_name, columns, values):
        """
        method that allows insertion of data into a table.
        like previously; ensures connection and creates cursor 
        placeholder(s) are created to avoid injection attacks, data type or escape char issues
        the %s is used to create a placeholder for any type
        allows any number of values by generating x amount of %s to be inserted via the sql 'insert' qeury further down
        as before, the sql query is executed by the cursor and changes commited
        """
        if self.connection is None:
            self.connect()
        
        cursor = self.connection.cursor()
                
        placeholders = ", ".join(['%s'] * len(values))
        
        insert_query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        """
        
        cursor.execute(insert_query, values)
        self.connection.commit()
        print(f"Success! Data has been inserted into {table_name}")


    def read_data(self, table_name, columns="*", condition=None):
        """
        method which allows reading data from a table
        the columns parameter has * as default value which means all columns
        the optional parameter "condition" allows filtering of rows returned. If present, it appends WHERE . . to the sql query
        the fetchall() retrieves all the rows returned by the sql query as tuples, where each tuple = one row
        """
        if self.connection is None:
            self.connect()
        
        cursor = self.connection.cursor()
        
        query = f"SELECT {columns} FROM {table_name}"
                
        if condition:
            query += f" WHERE {condition}"
        
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def update_data(self, table_name, set_values, condition):
        """
        method for updating data in a table
        the set_values parameter specifies which column is to be affected as well as the new value (eg "price = 15")
        the condition parameter specifies which rows is to be updated (otherwise all rows would be affected!)
        """
        if self.connection is None:
            self.connect()
        
        cursor = self.connection.cursor()
                
        update_query = f"""
        UPDATE {table_name}
        SET {set_values}
        WHERE {condition}
        """
        
        cursor.execute(update_query)
        self.connection.commit()
        print(f"Update complete! Data updated successfully in {table_name}")


    def delete_data(self, table_name, condition):
        """
        caution - method which deletes data from a table 
        the condition parameter specifies what is to be deleted

        """
        if self.connection is None:
            self.connect()
        
        cursor = self.connection.cursor()
        
        delete_query = f"""
        DELETE FROM {table_name}
        WHERE {condition}
        """
        
        cursor.execute(delete_query)
        self.connection.commit()
        
        print(f"All gone... Data deleted successfully from {table_name}")

    def close_connection(self):
        """
        method used to close the database connection
        """
        if self.connection:
            self.db_connection.close_connection()    