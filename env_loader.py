"""Загружает константы из .env.

Создан, чтобы не импортировать лишние пакеты,
возможно является не самой лучшей практикикой.
"""

import os

from dotenv import load_dotenv

# Загружаем данные из .env
load_dotenv()

# Данные для flask-сервера
IS_DEBUG = os.getenv("DEBUG").lower() == "true"
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# Получаем названия файлов баз данных из .env
USERS_DB_FILE_NAME = os.getenv("USERS_DB_FILE_NAME")
COURSES_DB_FILE_NAME = os.getenv("COURSES_DB_FILE_NAME")
