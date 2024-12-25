import asyncio
from config.config import db_name
import logging
import aiosqlite


logger_db = logging.getLogger("Database")


class Database:
    sql_request_tabel = """CREATE TABLE IF NOT EXISTS users
                        (id INTEGER NOT NULL PRIMARY KEY,
                        user_id INTEGER,
                        spreadsheet_id VARCHAR (130))"""

    async def connect_database(self):
        try:
            db = await aiosqlite.connect(db_name)
            cur = await db.cursor()
            await cur.execute(self.sql_request_tabel)
            await db.commit()
            return db
        except aiosqlite.DatabaseError as err:
            logger_db.error(f"Connection to a database failed.\n{err}")

    # Insert a new user to a table
    @staticmethod
    async def add_user(db, user_id, spreadsheet_id):
        sql_request = """INSERT INTO users (user_id, spreadsheet_id)
                             VALUES (?, ?);"""
        try:
            cur = await db.cursor()
            await cur.execute(sql_request, (user_id, spreadsheet_id))
            await db.commit()
            logger_db.info("The connection is established. Data was successfully inserted")
        except aiosqlite.DatabaseError as err:
            logger_db.error(f"User wasn't added.\n{err}")


    # Check if user exists in a table
    @staticmethod
    async def is_exist_user(db, user_id):
        sql_request = """SELECT user_id from users WHERE user_id = ?;"""
        try:
            cur = await db.cursor()
            await cur.execute(sql_request, (user_id,))
            result = await cur.fetchall()
            return bool(result) # Return True if a result is found, otherwise False
        except aiosqlite.DatabaseError as err:
            logger_db.error(f"Database error: {err}")
            return False


    # Getting the spreadsheet ID
    @staticmethod
    async def get_spreadsheet_id(db, user_id):
        sql_search = """SELECT spreadsheet_id from users WHERE user_id = ?;"""

        try:
            cur = await db.cursor()
            await cur.execute(sql_search, (user_id,))
            result = await cur.fetchone()  # Fetch the first row
            if result:
                return result[0]
            else:
                logger_db.warning("User's spreadsheet_id or user doesn't exist.")
        except aiosqlite.DatabaseError as err:
            logger_db.error(f"Getting the spreadsheet ID failed.\n{err}")

database = asyncio.run(Database().connect_database())

# TODO: divide into database part and models
