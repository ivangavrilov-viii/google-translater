from googletrans import Translator
import translate
import debug_log
import settings
import db


google_translator = Translator()

debug_log.logging(text=f"Response to {settings.DB_NAME}.", log_type='info')
language_id = db.db_language(settings.START_LANG)
translate_names = db.get_names(language_id)

debug_log.logging(text=f"List(length: {len(translate_names)}) to translate.", log_type='info')
debug_log.logging(text=f"Start translate from '{settings.START_LANG} to '{settings.END_LANG}'", log_type='info')

en_language_id = db.db_language(settings.END_LANG)

if language_id:
    for name in translate_names:
        new_name = translate.translate_word(google_translator, name['translation'], settings.END_LANG)
        new_title = translate.translate_word(google_translator, name['title'], settings.END_LANG)
        new_comment = translate.translate_word(google_translator, name['comment'], settings.END_LANG)
        db.save_name(name['set'], name['key'], new_name, new_comment, new_title, en_language_id)
    debug_log.logging(text=f'Names were translated to "{settings.END_LANG}".', log_type='success')

for lang in settings.END_LANGS:
    language_id = db.db_language(lang)

    if language_id:
        translate_names = db.get_names(en_language_id)

        for name in translate_names:
            new_name = translate.translate_word(google_translator, name['translation'], lang)
            new_title = translate.translate_word(google_translator, name['title'], lang)
            new_comment = translate.translate_word(google_translator, name['comment'], lang)
            db.save_name(name['set'], name['key'], new_name, new_comment, new_title, language_id)
    debug_log.logging(text=f'Names were translated to "{lang}".', log_type='success')

debug_log.logging(text=f'All names were translated to {settings.END_LANGS}', log_type='success')
