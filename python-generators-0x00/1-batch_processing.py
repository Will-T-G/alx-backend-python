#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from the user_data table in batches.
    Yields each batch as a list of tuples.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',              
            password='####',
            database='ALX_prodev'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        # yield remaining rows if total not divisible by batch_size
        if batch:
            yield batch

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            return    


def batch_processing(batch_size):
    """
    Processes each batch streamed from the database
    and yields only users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user[3] > 25]  # user[3] = age
        yield filtered
    return     


