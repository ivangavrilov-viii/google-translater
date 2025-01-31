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


def db_response(db_function, selector_list):
    """ Request to DB in "try-except" construction """

    # debug_log(f'{func_name} | INFO | DB response with selector_list = {selector_list} and db_function = {db_function}', 'db_requests.txt')
    try:
        response = make_callproc(db_function, selector_list)
        response = response[0][0] if response and response[0] else list()
        # debug_log(f'{func_name} | SUCCESS | Response from BD. Gotten data: {response}', 'db_requests.txt')
        return response
    except Exception as error:
        # debug_log(f'{func_name} | ERROR | Response from BD. Error: {error}', 'db_requests.txt')
        print(error)
        return list()


def make_callproc(db_function_name, selector_list):
    cur = CONNECTION.cursor()
    func_name = 'make_callproc - db.py'
    FILE_LOG = 'database_connect.txt'

    try:
        cur.callproc(db_function_name, selector_list)
        data = cur.fetchall()
        CONNECTION.commit()
        # debug_log(f'{func_name} | SUCCESS | Response was get with query = {cur.query}', FILE_LOG)
        return data
    except Exception as error:
        print(error)
    # except psycopg2.errors.ConnectionException as error:
    #     # debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection: {error}", FILE_LOG)
    #     stop_db_connection(connection)
    #
    #     while True:
    #         # debug_log(f"{func_name} | INFO |Start to reconnect with DB.", FILE_LOG)
    #         try:
    #             stop_db_connection(connection)
    #             connection = start_db_connection()
    #             cur = connection.cursor()
    #             cur.callproc(db_function_name, selector_list)
    #             data = cur.fetchall()
    #             connection.commit()
    #             # debug_log(f'{func_name} | SUCCESS | Reconnect DB - success. Response was get with query = {cur.query}', FILE_LOG)
    #             return data
    #         except psycopg2.Error as error:
    #             pass
    #             # debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection : {error}", FILE_LOG)
    # except psycopg2.DatabaseError as error:
    #     # debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection: {error}",FILE_LOG)
    #     while True:
    #         # debug_log(f"{func_name} | INFO | Start to reconnect with DB.", FILE_LOG)
    #         try:
    #             stop_db_connection(connection)
    #             connection = start_db_connection()
    #             cur = connection.cursor()
    #             cur.callproc(db_function_name, selector_list)
    #             data = cur.fetchall()
    #             connection.commit()
    #             # debug_log(f'{func_name} | SUCCESS | Reconnect DB - success. Response was get with query = {cur.query}', FILE_LOG)
    #             return data
    #         except Exception as error:
    #             # debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection: {error}", FILE_LOG)
    #             return None


CONNECTION = start_db_connection()
