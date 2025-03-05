"""Модуль для работы с базой данных."""  # noqa: INP001

from __future__ import annotations

import json
from pathlib import Path

from loguru import logger

from env_loader import COURSES_DB_FILE_NAME, USERS_DB_FILE_NAME


def check_db() -> None:
    """Проверяет наличае файлов баз данных."""
    # Словари
    for file_name in (USERS_DB_FILE_NAME,):
        path_file_object = Path(file_name)
        if not path_file_object.parent.exists():
            path_file_object.parent.mkdir(parents=True, exist_ok=True)
        if not path_file_object.exists():
            with path_file_object.open("a", encoding="UTF-8") as f:
                f.write("{}\n")

    # Списки
    for file_name in (COURSES_DB_FILE_NAME,):
        path_file_object = Path(file_name)
        if not path_file_object.parent.exists():
            path_file_object.parent.mkdir(parents=True, exist_ok=True)
        if not path_file_object.exists():
            with path_file_object.open("a", encoding="UTF-8") as f:
                f.write("[]\n")


class Users:
    """Класс для взаимодействия с пользователями."""

    async def add(
        self,
        csrf_token: str,
        login: str,
        password: str,
        refer: str | None = None,
    ) -> dict[str: bool, str: str]:
        """Добавляет пользователя в базу данных."""
        try:
            with Path.open(USERS_DB_FILE_NAME, "r+", encoding="UTF-8") as f:
                data = json.load(f)

                # Проверяем не занят ли этот логин
                for csrf in data:
                    if data[csrf].get("login") == login:
                        logger.debug("Этот логин занят, используйте другой.")
                        return {
                            "ok": False,
                            "message": "Этот логин занят, используйте другой.",
                        }
                        break

                data[csrf_token] = {
                    "login": login,
                    "password": password,
                    "refer": refer,
                }

                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4, ensure_ascii=True)

        except Exception as e:  # noqa: BLE001
            logger.error("Неизвестная ошибка: {}.", e)
            return {"ok": False, "message": f"Неизвестная ошибка: {e}."}

        else:
            logger.debug("Новый пользователь, {}", login)
            return {"ok": True, "message": ""}


    def is_auth(self, csrf: str) -> bool:
        """Проверяет зарегистрирован ли пользователь по csrf-токену."""
        with Path.open(USERS_DB_FILE_NAME, "r+", encoding="UTF-8") as f:
            return json.load(f).get(csrf)


class Courses:
    """Класс для взаимодействия с курсами."""
