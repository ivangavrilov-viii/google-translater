import asyncio
import logging
from telegram_bot import PyFlatinnBot
import db
import argparse
import sqlite3
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
# 01c222eb-05ce-48b2-a46a-2e21027ad0e0
# https://geocode-maps.yandex.ru/1.x/?apikey=ваш API-ключ&format=json&geocode=Тверская+6


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['run', 'status'])
    args = parser.parse_args()
    if args.action == 'status':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(dir_path + '/telegram.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select t.chat_id, checklist_id, step, c.checklist_line->>'key' as key from telegram t left join checklists c on t.chat_id = c.chat_id and t.step = c.checklist_step where checklist_id is not NULL;")
        data = cursor.fetchall()
        if len(data) > 0:
            connection_to_main_db = db.start_db_connection()
            print("{:<20} {:<15} {:<30} {:<15}".format('Chat id', 'Checklist id', 'Checklist name', 'Step'))
            for chat in data:
                connected_to_db, checklist_name = db.make_query(connection_to_main_db, "select * from checklist_name(%s,'ru');", chat[1])
                print("{:<20} {:<15} {:<30} {:<15}".format(str(chat[0]), str(chat[1]), checklist_name[0][0], str(chat[3])))
            db.stop_db_connection(connection_to_main_db)
        else:
            print("No active checklists!")
    elif args.action == 'run':
        connection_to_db = db.start_db_connection()
        bot = PyFlatinnBot("6547971783:AAFfyYdwVfs4j788RKv-YMBplwMcGli0uIg", "telegram-flatinn-bot", connection_to_db)
        bot.add_commands(["start", "add", "list"])    # bot.add_message_handler()
        bot.add_photo_handler()
        bot.add_location_handler()
        bot.add_video_handler()
        bot.add_message_handler()
        bot.add_document_handler()
        bot.run()
        db.stop_db_connection(connection_to_db)


if __name__ == "__main__":
    main()