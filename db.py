from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import psycopg2


def start_db_connection():
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
        password=DB_PASSWORD
    )
