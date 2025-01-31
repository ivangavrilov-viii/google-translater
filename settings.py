import configparser
import os


absolute_path = os.path.dirname(os.path.abspath(__file__))
config = configparser.RawConfigParser()
config.read(os.path.join(absolute_path, 'config.ini'), encoding='utf-8-sig')

BUILD = 'local'
# BUILD = 'prod'

if BUILD == 'local':
    CONFIG_DB = 'db_test'
else:
    CONFIG_DB = 'db'

DB_NAME = config.get(CONFIG_DB, 'NAME')

DB_USER = config.get(CONFIG_DB, 'USER')

DB_HOST = config.get(CONFIG_DB, 'HOST')

DB_PORT = config.get(CONFIG_DB, 'PORT')

DB_PASSWORD = config.get(CONFIG_DB, 'PASSWORD')

NAME_URLS = [
    "https://auth.flatinn.ru/static/names.txt",

]

START_LANG = 'ru'

END_LANGS = [
    'en',
    'ru',
    'fr',
    'sr',
    'ar',
    'az',
    'ka'
]

GET_NAMES = 'names_arr_json'

UPDATE_NAMES = 'names_update_unverified_json'

USER_ID = 1
