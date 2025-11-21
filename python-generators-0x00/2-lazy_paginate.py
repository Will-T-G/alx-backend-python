import mysql.connector

def paginate_users(page_size, offset):
    """Fetch one page of users from the database."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily fetches users page by page."""
    offset = 0
    while True:  #  only one loop
        users = paginate_users(page_size, offset)
        if not users:
            break  # no more data to fetch
        yield users
        offset += page_size  # move to next page
    return  

