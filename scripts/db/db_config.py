import os

DATABASE_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),  # or your database host
    'port': os.getenv("DB_PORT"),       # default PostgreSQL port
}