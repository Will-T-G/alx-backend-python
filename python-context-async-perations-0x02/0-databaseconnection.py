import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish connection when entering the context
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        print("Database connection opened.")
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure resources are released properly
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")
        return False  # Don’t suppress exceptions


# Use the context manager with `with` to perform the query
if __name__ == "__main__":
    with DatabaseConnection(
        host="localhost",
        user="root",
        password="your_password",   # <-- replace this
        database="ALX_prodev"
    ) as cursor:
        cursor.execute("SELECT * FROM users;")  # required query
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)

