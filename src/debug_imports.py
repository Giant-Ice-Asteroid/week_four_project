import sys
import os

print("Python Version:", sys.version)
print("Current Working Directory:", os.getcwd())
print("sys.path:", sys.path)

try:
    import db
    print("Successfully imported db package")
    
    import db.db_connection
    print("Successfully imported db.db_connection module")
    
    from db.db_connection import DatabaseConnection
    print("Successfully imported DatabaseConnection class")
except ImportError as e:
    print(f"Import error: {e}")

print("Script completed")