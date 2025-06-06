import configparser
import argparse
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

    BIG_DICTS = [
        # "reviews",
        "rentals-headline",
    ]

    mode_choices = [
        'full',
        'auth',
        'short',
        'guests',
        'owners',
        'flatinn',
        'standart',
        'dashboard',
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=mode_choices)
    args = parser.parse_args()
    MODE = args.mode

    if MODE == 'guests':
        NAME_URLS = [
            "https://guests.flatinn.ru/static/general/names.txt",
        ]
    elif MODE == 'owners':
        NAME_URLS = [
            "https://owners.flatinn.ru/static/names.txt",
        ]
    elif MODE == 'auth':
        NAME_URLS = [
            "https://auth.flatinn.ru/static/names.txt",
        ]
    elif MODE == 'flatinn':
        NAME_URLS = [
             "https://flatinn.ru/static/names.txt"
        ]
    elif MODE == 'short':
        NAME_URLS = [
            "https://flatinn.ru/static/names.txt"
        ]
        END_LANGS = []
    elif MODE == 'standart':
        NAME_URLS = [
            "https://auth.flatinn.ru/static/names.txt",
            "https://guests.flatinn.ru/static/general/names.txt",
            "https://flatinn.ru/static/names.txt"
        ]
    else:
        NAME_URLS = list()
else:
    START_LANG = config.get('variables', 'START_LANG')

    END_LANG = config.get('variables', 'END_LANG')

    END_LANGS = [
        'ar',
        'de',
        'zh-CN'
    ]
