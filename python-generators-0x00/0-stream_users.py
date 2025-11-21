#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that connects to the ALX_prodev database
    and yields rows from the user_data table one by one.
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',             
            password='####',
            database='ALX_prodev'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")

        #  Yield each row one at a time
        for row in cursor:
            yield row

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


