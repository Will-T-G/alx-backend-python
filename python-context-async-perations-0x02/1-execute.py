import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open DB connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",   # <-- replace with your real password
            database="ALX_prodev"
        )
        self.cursor = self.connection.cursor()
        print("Database connection opened.")

        # Execute query immediately and return results
        self.cursor.execute(self.query, self.params)
        result = self.cursor.fetchall()
        return result

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean up properly
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")
        return False  # Don’t suppress exceptions



if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s;"
    params = (25,)

    with ExecuteQuery(query, params) as results:
        print("Query Results:")
        for row in results:
            print(row)


