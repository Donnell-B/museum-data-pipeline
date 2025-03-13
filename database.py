# pylint: skip-file
from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor


load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')


def get_connection() -> connection:
    """Get Database connection"""
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    return conn


def get_cursor(conn: connection) -> cursor:
    """Get Cursor for database"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor


def upload_request_interaction(data, db_cursor):
    db_cursor.execute("""
        INSERT INTO request_interaction (exhibition_id, request_id, event_at)
                      VALUES (%s, (SELECT request_id FROM request WHERE request_value = %s), %s)
    """, data)


def upload_rating_interaction(data, db_cursor):
    db_cursor.execute("""
        INSERT INTO rating_interaction (exhibition_id, rating_id, event_at)
                      VALUES (%s, (SELECT rating_id FROM rating WHERE rating_value = %s), %s)
    """, data)
