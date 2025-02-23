"""Модуль для работы с базой данных."""  # noqa: INP001

# import json  # noqa: ERA001
from pathlib import Path

from loguru import logger

from env_loader import COURSES_DB_FILE_NAME, USERS_DB_FILE_NAME


def check_db() -> None:
    """Проверяет наличае файлов баз данных."""
    for db_name in (USERS_DB_FILE_NAME, COURSES_DB_FILE_NAME):
        if not Path(db_name).exists():
            with Path.open(db_name, "a", encoding="UTF-8") as f:
                f.write("{}\n")
            logger.info("Файл базы данных {} создан", db_name)


class Users:
    """Класс для взаимодействия с пользователями."""

class Courses:
    """Класс для взаимодействия с курсами."""
