import sqlite3
from config.config import db_name


# Connecting to a database
def db_connect():
    try:
        connection = sqlite3.connect(f'{db_name}')
    except sqlite3.DatabaseError as err:
        print(f"Connection to a database failed.\n{err}")
    else:
        return connection


# Creating a new table
def new_table():
   connection = db_connect()
   cur = connection.cursor()
   sql_request = """CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id integer, url varchar (130), value float)"""
   try:
       cur.execute(sql_request)
   except sqlite3.DatabaseError as err:
       print(f"Table wasn't created.\n{err}")
   else:
       print("Table created successfully")
   finally:
        connection.commit()
        connection.close()


# Checking if a user is in a database
def exist_user(user_id):
    connection = db_connect()
    cur = connection.cursor()
    sql_request = f"""SELECT user_id from users WHERE user_id = '{user_id}';"""
    try:
        cur.execute(sql_request)
        result = cur.fetchall()
        if not result:
            return False
        else:
            return True
    finally:
        connection.commit()
        connection.close()


# Inserting a new user to a table
def add_user(user_id, url):
    connection = db_connect()
    cur = connection.cursor()
    try:
        cur.execute(
            f"""INSERT INTO users (user_id, url, value)
            VALUES ('{user_id}', '{url}', 0);"""
        )
    except sqlite3.DatabaseError as err:
        msg = "Something went wrong. Try again, please"
        print(f"User wasn't added.\n{err}")
        return msg
    else:
        msg = "The connection is established."
        print("Data was successfully inserted")
        return msg
    finally:
        connection.commit()
        connection.close()


# Updating a url in a database
def update_url(user_id, url):
    connection = db_connect()
    cur = connection.cursor()
    sql_search = f"""UPDATE users SET url = '{url}' WHERE user_id = '{user_id}';"""
    try:
        cur.execute(sql_search)
    except sqlite3.DatabaseError as err:
        msg = "Your url wasn't added. Try again, please"
        print(f"Url wasn't added.\n{err}")
        return msg
    else:
        msg = "Your url was successfully added"
        return msg
    finally:
        connection.commit()
        connection.close()


# Getting a url
def get_url_address(user_id):
    connection = db_connect()
    cur = connection.cursor()
    sql_search = f"""SELECT url from users WHERE user_id = '{user_id}';"""
    try:
        cur.execute(sql_search)
    except sqlite3.DatabaseError as err:
        print(f"Getting a url was failed.\n{err}")
    else:
        url = cur.fetchone()
        url_formatted = url[0]
        if not url:
            return False
        else:
            return True and url_formatted
    finally:
        connection.commit()
        connection.close()


# Updating a url
def update_value(user_id, value):
    connection = db_connect()
    cur = connection.cursor()
    sql_search = f"""UPDATE users SET value = '{value}' WHERE user_id = '{user_id}';"""
    try:
        cur.execute(sql_search)
    except sqlite3.DatabaseError as err:
        msg = "The value wasn't added. Try again, please"
        print(f"Value wasn't added.\n{err}")
        return msg
    else:
        msg = "The value was successfully added"
        return msg
    finally:
        connection.commit()
        connection.close()


# Getting a price
def get_value(user_id):
    connection = db_connect()
    cur = connection.cursor()
    sql_search = f"""SELECT value from users WHERE user_id = '{user_id}';"""
    try:
        cur.execute(sql_search)
    except sqlite3.DatabaseError as err:
        print(f"Getting a value was failed.\n{err}")
    else:
        data = cur.fetchone()
        value = float(data[0])
        return value
    finally:
        connection.commit()
        connection.close()
