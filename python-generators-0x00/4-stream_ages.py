import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='####',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  #  only one loop here
        yield age

    cursor.close()
    connection.close()


def calculate_average_age():
    """Uses the generator to calculate average age without loading all data into memory."""
    total = 0
    count = 0

    for age in stream_user_ages():  #  second loop
        total += age
        count += 1

    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    calculate_average_age()

