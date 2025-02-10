import debug_log
import settings
import psycopg2


def start_db_connection():
    return psycopg2.connect(
        database=settings.DB_NAME,
        user=settings.DB_USER,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        password=settings.DB_PASSWORD
    )


def stop_db_connection():
    CONNECTION.close()
    debug_log.logging(text=f"Connection with DataBase was closed", log_type="info")


def get_data(db_function, selector_list):
    """ Request to DB in "try-except" construction """

    try:
        response = make_callproc(db_function, selector_list)
        response = response[0][0] if response and response[0] else list()
        return response
    except Exception as error:
        debug_log.logging(text=f'Error with "{db_function}({selector_list})". Error: {error}', log_type='error')
        return list()


def db_request(db_function_name, selector_list):
    cursor = CONNECTION.cursor()
    cursor.callproc(db_function_name, selector_list)
    data = cursor.fetchall()
    CONNECTION.commit()
    return data


def make_callproc(db_function_name, selector_list):
    global CONNECTION

    try:
        return db_request(db_function_name, selector_list)
    except psycopg2.errors.ConnectionException as error:
        debug_log.logging(text=f'Error with "{cursor.query}". Error with connection: {error}', log_type='warning')
        stop_db_connection()

        while True:
            debug_log.logging(text=f'Start to reconnect to DataBase.', log_type='warning')

            try:
                CONNECTION = start_db_connection()
                return db_request(db_function_name, selector_list)
            except psycopg2.Error as error:
                debug_log.logging(text=f'Error with reconnect: {error}', log_type='critical')
    except psycopg2.DatabaseError as error:
        debug_log.logging(text=f'Error with "{cursor.query}". Error: {error}', log_type='warning')
        stop_db_connection()

        while True:
            debug_log.logging(text=f'Start to reconnect to DataBase.', log_type='warning')

            try:
                CONNECTION = start_db_connection()
                return db_request(db_function_name, selector_list)
            except Exception as error:
                debug_log.logging(text=f'Error with reconnect: {error}', log_type='critical')
                return None


def db_names(language_id):
    translate_names = list()
    with CONNECTION.cursor() as cursor:
        cursor.execute(f"""
            SELECT * 
            FROM names 
            WHERE language_id = {language_id}; 
        """)

        names = cursor.fetchall()
        CONNECTION.commit()

    if names and len(names) > 0:
        for name in names:
            translate_names.append({
                'index': name[0],
                'set': name[1],
                'key': name[2],
                'translation': name[3],
                'comment': name[4],
                'title': name[5],
                'language_id': int(name[6]),
                'verified': name[7]
            })
    return translate_names


def db_language(language):
    with CONNECTION.cursor() as cursor:
        cursor.execute(f"SELECT index FROM languages WHERE key = '{language}';")
        language_id = cursor.fetchone()
        CONNECTION.commit()
        language_id = language_id[0] if language_id and language_id[0] else None
        return language_id


def save_name(name_set, name_key, name_translation, name_comment, name_title, language_id):
    with CONNECTION.cursor() as cursor:
        cursor.execute(f"""
            SELECT index, verified
            FROM names 
            WHERE set = '{name_set}' AND key = '{name_key}' AND language_id = {language_id};
        """)
        name = cursor.fetchone()
        CONNECTION.commit()
        name_id = name[0] if name and name[0] else None
        name_verified = name[1] if name else False

        if name_id and not name_verified:
            cursor.execute(f"""
                UPDATE names
                SET translation = '{name_translation}', comment = '{name_comment}', title = '{name_title}'
                WHERE index = {name_id};
            """)
        elif name_id is None:
            cursor.execute(f"""
                INSERT INTO names (set, key, translation, comment, title, language_id, verified)
                VALUES ('{name_set}','{name_key}', '{name_translation}', '{name_comment}', '{name_title}', {language_id}, {name_verified});
            """)
        CONNECTION.commit()



def get_db_tables():
    with CONNECTION.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        tables = cursor.fetchall()
        CONNECTION.commit()

    for table in tables:
        print(table[0])


def get_names(language_id):
    global CONNECTION

    try:
        return db_names(language_id)
    except psycopg2.errors.ConnectionException as error:
        debug_log.logging(text=f'Error with "{cursor.query}". Error with connection: {error}', log_type='warning')
        stop_db_connection()

        while True:
            debug_log.logging(text=f'Start to reconnect to DataBase.', log_type='warning')

            try:
                CONNECTION = start_db_connection()
                return db_names(language_id)
            except psycopg2.Error as error:
                debug_log.logging(text=f'Error with reconnect: {error}', log_type='critical')
    except psycopg2.DatabaseError as error:
        debug_log.logging(text=f'Error with "{cursor.query}". Error: {error}', log_type='warning')
        stop_db_connection()

        while True:
            debug_log.logging(text=f'Start to reconnect to DataBase.', log_type='warning')

            try:
                CONNECTION = start_db_connection()
                return db_names(language_id)
            except Exception as error:
                debug_log.logging(text=f'Error with reconnect: {error}', log_type='critical')
                return None


CONNECTION = start_db_connection()
