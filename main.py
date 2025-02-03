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
count = 0

for file_url in settings.NAME_URLS:
    response = requests.get(file_url)

    debug_log.logging(text=f"Response to {file_url}. {response.status_code}: {response}.", log_type='info')

    if response.status_code == 200:
        input_string = response.text.splitlines()[0]
        names = ast.literal_eval(input_string)
        translate_names += names

debug_log.logging(text=f"List(length: {len(translate_names)}) to translate: {translate_names}.", log_type='info')
debug_log.logging(text=f"Start translate from '{settings.START_LANG} to '{settings.END_LANG}'", log_type='info')


for names_dict in translate_names:
    count += 1
    debug_log.logging(text=f'DICTIONARY #{count}: "{names_dict}".', log_type='info')

    names_selector = [names_dict, settings.START_LANG]
    names_labels = db.get_data(settings.GET_NAMES, names_selector)

    for label in names_labels:
        label_name = translate.translate_word(google_translator, label['name'], settings.END_LANG)
        label_title = translate.translate_word(google_translator, label['title'], settings.END_LANG)
        label_comment = translate.translate_word(google_translator, label['comment'], settings.END_LANG)
        label_index = translate.translate_word(google_translator, label['index'], settings.END_LANG)

        label_selector = [label['key'], names_dict, label_name, label_title, label_comment, label_index, settings.USER_ID, settings.END_LANG]
        update_translate = db.get_data(settings.UPDATE_NAMES, label_selector)
    debug_log.logging(text=f'Dict "{names_dict}" was translated to "{settings.END_LANG}".', log_type='success')

    names_selector = [names_dict, settings.END_LANG]
    names_labels = db.get_data(settings.GET_NAMES, names_selector)

    for label in names_labels:
        for language in settings.END_LANGS:
            label_name = translate.translate_word(google_translator, label['name'], language)
            label_title = translate.translate_word(google_translator, label['title'], language)
            label_comment = translate.translate_word(google_translator, label['comment'], language)
            label_index = translate.translate_word(google_translator, label['index'], language)
            language = 'ge' if language == 'ka' else language

            label_selector = [label['key'], names_dict, label_name, label_title, label_comment, label_index, settings.USER_ID, language]
            update_translate = db.get_data(settings.UPDATE_NAMES, label_selector)

    debug_log.logging(text=f'Dict "{names_dict}" was translated to "{settings.END_LANGS}".', log_type='success')

debug_log.logging(text=f'All dictionaries were translated to {settings.END_LANGS}', log_type='success')
