"""Модуль для работы с базой данных."""  # noqa: INP001

from __future__ import annotations

import json
from pathlib import Path

from loguru import logger

from env_loader import COURSES_DB_FILE_NAME, USERS_DB_FILE_NAME


async def check_db() -> None:
    """Проверяет наличае файлов баз данных."""
    for db_name in (USERS_DB_FILE_NAME, COURSES_DB_FILE_NAME):
        if not Path(db_name).exists():
            with Path.open(db_name, "a", encoding="UTF-8") as f:
                f.write("{}\n")
            logger.info("Файл базы данных {} создан", db_name)


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
            with Path.open(USERS_DB_FILE_NAME, "w", encoding="UTF-8") as f:
                data = json.load(f)

                # Проверяем не занят ли этот логин
                for user in data:
                    if not user.get(login):
                        logger.debug("Этот логин занят, используйте другой.")
                        await {
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

            logger.debug("Новый пользователь, {}", login)
            await {"ok": True, "message": ""}

        except Exception as e:  # noqa: BLE001
            logger.error("Неизвестная ошибка: {}.", e)
            await {"ok": False, "message": f"Неизвестная ошибка: {e}."}

class Courses:
    """Класс для взаимодействия с курсами."""
