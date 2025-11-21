#!/usr/bin/python3
import csv
import uuid
import mysql.connector
from mysql.connector import Error

# Connect to MySQL server


def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='####'   
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Create database if not exists
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


# Connect to ALX_prodev
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='####',  
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


# Create user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


# Insert CSV data
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, email, age = row
                user_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name.strip(), email.strip(), float(age)))
        connection.commit()
        print("Data inserted successfully from CSV.")
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")


# Main execution (for manual run)
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        print("connection successful")

        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, "user_data.csv")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            conn.close()

