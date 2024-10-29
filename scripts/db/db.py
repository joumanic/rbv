# root/scripts/db_handler.py

import psycopg2
from db.db_config import DATABASE_CONFIG
import logging
import pandas as pd

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish a database connection."""
        try:
            self.connection = psycopg2.connect(
                dbname=DATABASE_CONFIG['dbname'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                host=DATABASE_CONFIG['host'],
                port=DATABASE_CONFIG['port']
            )
            self.cursor = self.connection.cursor()
            logging.info("Database connection established.")
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")

    def execute_query(self, query, params=None):
        """Execute a single query."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None
    
    def get_current_radio_shows(self):
        try:
            self.cursor.execute(
            '''SELECT *
            FROM public.radio_show
            WHERE created_at::date < (
            show_date - (EXTRACT(DOW FROM show_date) + 1 + 1) % 7 * INTERVAL '1 day')'''
            )
            results = pd.DataFrame(self.cursor.fetchall(), columns=[desc[0] for desc in self.cursor.description])
            return results
        except Exception as e:
            logging.error(f"Error executing get_current_radio_show query: {e}")
            return None

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")
