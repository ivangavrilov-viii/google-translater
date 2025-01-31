from googletrans import Translator
import requests
import json
import ast

import translate
import settings
import db


google_translator = Translator()
translate_names = list()
count = 0

for file_url in settings.NAME_URLS:
    response = requests.get(file_url)

    if response.status_code == 200:
        input_string = response.text.splitlines()[0]
        names = ast.literal_eval(input_string)
        translate_names += names
    else:
        print(f"Error: {response.status_code}. Response: {response}.")


print(f"Start translate from '{settings.START_LANG}' language.\nLength of translating dict: {len(settings.END_LANGS)}")


for names_dict in translate_names[:2]:
    print(f'#{count + 1}. DICTIONARY: "{names_dict}".')

    names_selector = [names_dict, settings.START_LANG]
    names_labels = db.db_response(settings.GET_NAMES, names_selector)

    for label in names_labels:
        for language in settings.END_LANGS:
            label_name = translate.translate_word(google_translator, label['name'], language)
            label_title = translate.translate_word(google_translator, label['title'], language)
            label_comment = translate.translate_word(google_translator, label['comment'], language)
            label_index = translate.translate_word(google_translator, label['index'], language)
            language = 'ge' if language == 'ka' else language

            label_selector = [label['key'], label_name, label_title, label_comment, label_index, settings.USER_ID, language]
            update_translate = db.db_response(settings.UPDATE_NAMES, label_selector)

    print(f"{count + 1}. DICTIONARY '{translate_name}' is translated.\n")
    count += 1



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
