from googletrans import Translator
import requests
import json
import ast

import translate
import debug_log
import settings
import db


google_translator = Translator()
translate_names = list()

debug_log.logging(text=f"Response to {settings.DB_NAME}.", log_type='info')
names = db.get_names()

if names and len(names) > 0:
    for name in names:
        translate_names.append({
            'index': name[0],
            'set': name[1],
            'key': name[2],
            'translation': name[3],
            'comment': name[4],
            'title': name[5],
            'language_key': name[8]
        })

debug_log.logging(text=f"List(length: {len(translate_names)}) to translate.", log_type='info')
debug_log.logging(text=f"Start translate from '{settings.START_LANG} to '{settings.END_LANG}'", log_type='info')


for name in translate_names:
    label_name = translate.translate_word(google_translator, name['translation'], settings.END_LANG)
    label_title = translate.translate_word(google_translator, name['title'], settings.END_LANG)
    label_comment = translate.translate_word(google_translator, name['comment'], settings.END_LANG)
    label_index = name['index'] if name.get('index', None) else None


    print(label_name)


# for names_dict in translate_names:
#     count += 1
#     debug_log.logging(text=f'DICTIONARY #{count}: "{names_dict}".', log_type='info')
#
#     names_selector = [names_dict, settings.START_LANG]
#     names_labels = db.get_data(settings.GET_NAMES, names_selector)
#
#     for label in names_labels:
#         label_name = translate.translate_word(google_translator, label['name'], settings.END_LANG)
#         label_title = translate.translate_word(google_translator, label['title'], settings.END_LANG)
#         label_comment = translate.translate_word(google_translator, label['comment'], settings.END_LANG)
#         label_index = label['index'] if label.get('index', None) else None
#
#         label_selector = [label['key'], names_dict, label_name, label_title, label_comment, label_index, settings.USER_ID, settings.END_LANG]
#         update_translate = db.get_data(settings.UPDATE_NAMES, label_selector)
#     debug_log.logging(text=f'Dict "{names_dict}" was translated to "{settings.END_LANG}".', log_type='success')
#
#     names_selector = [names_dict, settings.END_LANG]
#     names_labels = db.get_data(settings.GET_NAMES, names_selector)
#
#     for label in names_labels:
#         for language in settings.END_LANGS:
#             label_name = translate.translate_word(google_translator, label['name'], language)
#             label_title = translate.translate_word(google_translator, label['title'], language)
#             label_comment = translate.translate_word(google_translator, label['comment'], language)
#             label_index = label['index'] if label.get('index', None) else None
#             language = 'ge' if language == 'ka' else language
#
#             label_selector = [label['key'], names_dict, label_name, label_title, label_comment, label_index, settings.USER_ID, language]
#             update_translate = db.get_data(settings.UPDATE_NAMES, label_selector)
#
#     debug_log.logging(text=f'Dict "{names_dict}" was translated to "{settings.END_LANGS}".', log_type='success')
#
# debug_log.logging(text=f'All dictionaries were translated to {settings.END_LANGS}', log_type='success')
