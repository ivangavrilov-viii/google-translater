import configparser
import os


absolute_path = os.path.dirname(os.path.abspath(__file__))
config = configparser.RawConfigParser()
config.read(os.path.join(absolute_path, 'config.ini'), encoding='utf-8-sig')

# PROJECT = 'flatinn'
PROJECT = 'leocars'

BUILD = 'local'
# BUILD = 'prod'

if BUILD == 'local' and PROJECT == 'flatinn':
    CONFIG_DB = 'db_test_flatinn'
elif BUILD == 'prod' and PROJECT == 'flatinn':
    CONFIG_DB = 'db'
else:
    CONFIG_DB = 'db_leocars'

DB_NAME = config.get(CONFIG_DB, 'NAME')

DB_USER = config.get(CONFIG_DB, 'USER')

DB_HOST = config.get(CONFIG_DB, 'HOST')

DB_PORT = config.get(CONFIG_DB, 'PORT')

DB_PASSWORD = config.get(CONFIG_DB, 'PASSWORD')

if PROJECT == 'flatinn':
    NAME_URLS = [
        "https://auth.flatinn.ru/static/names.txt",
        "https://guests.flatinn.ru/static/general/names.txt"
    ]

    START_LANG = config.get('variables', 'START_LANG')

    END_LANG = config.get('variables', 'END_LANG')

    END_LANGS = [
        'fr',
        'sr',
        'ar',
        'az',
        'ka'
    ]

    GET_NAMES = config.get('variables', 'GET_NAMES_FUNC')

    UPDATE_NAMES = config.get('variables', 'UPDATE_NAMES_FUNC')

    USER_ID = int(config.get('variables', 'DB_USER_ID'))

else:
    START_LANG = config.get('variables', 'START_LANG')

    END_LANG = config.get('variables', 'END_LANG')

    END_LANGS = [
        'ar',
        'de',
        'zh-CN'
    ]
