import sqlite3
import pandas as pd


class Action:
    def __init__(self):
        """Initialize the database connection and create table if not exists."""
        self.conn = sqlite3.connect("temp_files.db", check_same_thread=False)  # Persistent connection
        self.create_table()

    def create_table(self):
        """Create a table for EDF file storage."""
        self.conn.execute('''CREATE TABLE IF NOT EXISTS temp_files (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                filename TEXT UNIQUE NOT NULL,
                                saturation TEXT NOT NULL,
                                desaturation TEXT NOT NULL);''')
        self.conn.commit()



    def get_existed_data(self):
        """Fetch all records from the users table."""
        df = self.conn.execute("SELECT id, filename FROM temp_files")
        return df
    
    def get_existed_files(self):
        """Fetch all records from the users table."""
        df = self.conn.execute("SELECT filename FROM temp_files")
        return df
    
    def get_existed_files_data(self):
        """Fetch all records from the users table."""
        df = self.conn.execute("SELECT filename, filedata FROM temp_files")
        return df


    def insert_files(self, filename, saturation, desaturation):
        """Insert file into the database."""
        self.conn.execute("INSERT INTO temp_files (filename, saturation, desaturation) VALUES (?, ?, ?)", (filename, saturation, desaturation))
        self.conn.commit()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()


class Button:
    pass