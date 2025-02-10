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
language_id = db.db_language(settings.START_LANG)
translate_names = db.get_names(language_id)

debug_log.logging(text=f"List(length: {len(translate_names)}) to translate.", log_type='info')
debug_log.logging(text=f"Start translate from '{settings.START_LANG} to '{settings.END_LANG}'", log_type='info')

en_language_id = db.db_language(settings.END_LANG)

if language_id:
    for name in translate_names:
        label_name = translate.translate_word(google_translator, name['translation'], settings.END_LANG)
        label_title = translate.translate_word(google_translator, name['title'], settings.END_LANG)
        label_comment = translate.translate_word(google_translator, name['comment'], settings.END_LANG)
        label_index = name['index'] if name.get('index', None) else None
        result = db.save_name(name['set'], name['key'], label_name, label_comment, label_title, en_language_id, name['verified'])
    debug_log.logging(text=f'Names were translated to "{settings.END_LANG}".', log_type='success')

for lang in settings.END_LANGS:
    language_id = db.db_language(lang)

    if language_id:
        translate_names = db.get_names(en_language_id)

        for name in translate_names:
            label_name = translate.translate_word(google_translator, name['translation'], lang)
            label_title = translate.translate_word(google_translator, name['title'], lang)
            label_comment = translate.translate_word(google_translator, name['comment'], lang)
            label_index = name['index'] if name.get('index', None) else None
            result = db.save_name(name['set'], name['key'], label_name, label_comment, label_title, language_id, name['verified'])
    debug_log.logging(text=f'Names were translated to "{lang}".', log_type='success')

debug_log.logging(text=f'All names were translated to {settings.END_LANGS}', log_type='success')
