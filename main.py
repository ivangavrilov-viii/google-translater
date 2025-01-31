from googletrans import Translator
import requests

import db
import settings

# import datetime
# import re




# def debug_log(text, file_name):
#     """
#     This function writes the time&date and then the provided 'text' argument to a file with name made out of
#     'file_name' argument in the same folder with this the script.
#     """
#     year = str(datetime.datetime.now().year)
#     month = str(datetime.datetime.now().month)
#     day = str(datetime.datetime.now().day)
#
#     path = os.path.dirname(os.path.abspath(__file__))
#     logs_path = os.path.join(path, "debug_logs", year, month, day)
#     file_path = os.path.join(logs_path, file_name)
#     if os.path.exists(file_path):
#         with open(file_path, 'a+', encoding="utf-8") as txt_file:
#             txt_file.write(str(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S ")))
#             txt_file.write(str(text))
#             txt_file.write('\n')
#     else:
#         if not os.path.exists(logs_path):
#             os.makedirs(logs_path)
#         with open(file_path, 'a+', encoding="utf-8") as txt_file:
#             txt_file.write(str(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S ")))
#             txt_file.write(str(text))
#             txt_file.write('\n')
#
#
# def stop_db_connection(db_connection):
#     db_connection.close()
#     debug_log(f"DB (stop_db_connection) INFO. Connection with DB was closed", 'database_connect.txt')
#
#
# def make_callproc(db_function_name, selector_list):
#     global connection
#     cur = connection.cursor()
#     func_name = 'make_callproc - db.py'
#     FILE_LOG = 'database_connect.txt'
#
#     try:
#         cur.callproc(db_function_name, selector_list)
#         data = cur.fetchall()
#         connection.commit()
#         debug_log(f'{func_name} | SUCCESS | Response was get with query = {cur.query}', FILE_LOG)
#         return data
#     except psycopg2.errors.ConnectionException as error:
#         debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection: {error}", FILE_LOG)
#         stop_db_connection(connection)
#
#         while True:
#             debug_log(f"{func_name} | INFO |Start to reconnect with DB.", FILE_LOG)
#             try:
#                 stop_db_connection(connection)
#                 connection = start_db_connection(db_name, db_user, db_pass)
#                 cur = connection.cursor()
#                 cur.callproc(db_function_name, selector_list)
#                 data = cur.fetchall()
#                 connection.commit()
#                 debug_log(f'{func_name} | SUCCESS | Reconnect DB - success. Response was get with query = {cur.query}', FILE_LOG)
#                 return data
#             except psycopg2.Error as error:
#                 debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection : {error}", FILE_LOG)
#     except psycopg2.DatabaseError as error:
#         debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection: {error}",FILE_LOG)
#         while True:
#             debug_log(f"{func_name} | INFO | Start to reconnect with DB.", FILE_LOG)
#             try:
#                 stop_db_connection(connection)
#                 connection = start_db_connection(db_name, db_user, db_pass)
#                 cur = connection.cursor()
#                 cur.callproc(db_function_name, selector_list)
#                 data = cur.fetchall()
#                 connection.commit()
#                 debug_log(f'{func_name} | SUCCESS | Reconnect DB - success. Response was get with query = {cur.query}', FILE_LOG)
#                 return data
#             except Exception as error:
#                 debug_log(f"{func_name} | ERROR | Response wasn't get with query = {cur.query}. Error with connection: {error}", FILE_LOG)
#                 return None
#
#
# def try_except_callproc_request_to_db(db_function, selector_list, func_name):
#     """ Request to DB in "try-except" construction """
#
#     debug_log(f'{func_name} | INFO | DB response with selector_list = {selector_list} and db_function = {db_function}', 'db_requests.txt')
#     try:
#         response = make_callproc(db_function, selector_list)
#         debug_log(f'{func_name} | SUCCESS | Response from BD. Gotten data: {response}', 'db_requests.txt')
#         return response
#     except Exception as error:
#         debug_log(f'{func_name} | ERROR | Response from BD. Error: {error}', 'db_requests.txt')
#         return list()
#
#
# def translate_word(name_string, new_language) -> str:
#     to_translated_list, translated_list = list(), list()
#     start_spec_word = False
#
#     if not name_string or name_string is None:
#         return ''
#
#     while "{" in name_string and '}' in name_string:
#         start_index = 0
#         for letter_index in range(len(name_string)):
#             if not start_spec_word and name_string[letter_index] == '{':
#                 start_index = letter_index
#                 start_spec_word = True
#             elif start_spec_word and name_string[letter_index] == '}':
#                 to_translated_list.append(name_string[:start_index])
#                 to_translated_list.append(name_string[start_index:letter_index + 1])
#                 name_string = name_string[letter_index + 1:]
#                 start_spec_word = False
#                 break
#     else:
#         to_translated_list.append(name_string)
#
#     for word in to_translated_list:
#         if "{" not in word and '}' not in word:
#             translated_list.append(translator.translate(word, dest=new_language).text)
#         else:
#             translated_list.append(word)
#
#     return ' '.join(translated_list)


connection = db.start_db_connection()
translator = Translator()


for file_url in settings.NAME_URLS:
    print(file_url)
    response = requests.get(file_url)

    if response.status_code == 200:
        print('success')
    #     Преобразуем содержимое файла в список строк
    #     lines = response.text.splitlines()
    #
    #     # Выводим результат
    #     print(lines)
    # else:
    #     print(f"Ошибка при загрузке файла: {response.status_code}")

# translates_name = []

# # language_from = 'ru'
# language_from = 'en'
#
# # new_languages = ['en']
# # new_languages = ['ru']
# new_languages = ['fr', 'sr', 'ar', 'az','ka']
# # new_languages = ['fr', 'sr', 'en', 'ar', 'az','ka']
#
# print(f"Start translator script from '{language_from}' language. ")
# print(f"Length of translating dict: {len(translates_name)}")
#
# count = 0
# for translate_name in translates_name:
#     count += 1
#     names_labels = try_except_callproc_request_to_db('names', [translate_name, language_from], 'new_translate_main.py')
#
#     print(f'{count}. Start translate {translate_name}.')
#     for new_language in new_languages:
#         print(f'Start language {new_language}.')
#         for name in names_labels:
#             name_key = str(name[0])
#             name_name = translate_word(str(name[1]), new_language)
#             name_title = translate_word(str(name[2]), new_language) if name[2] else ''
#             name_comment = translate_word(str(name[3]), new_language) if name[3] else ''
#             name_index = name[4] if name[4] else None
#
#             if new_language == 'ka':
#                 selector_list = [name_key, translate_name, name_name, name_title, name_comment, name_index, 1, 'ge']
#             else:
#                 selector_list = [name_key, translate_name, name_name, name_title, name_comment, name_index, 1, new_language]
#
#             update_translate = try_except_callproc_request_to_db('names_update_unverified', selector_list, 'new_translate_main.py')
#     print(f"{count}. {translate_name} is translated.\n")

