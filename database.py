import os
from dotenv import load_dotenv

load_dotenv()

import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="task_manager_db"
    )
    return connection
