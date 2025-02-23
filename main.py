"""Основной модуль для запуска."""

from __future__ import annotations

import asyncio

from flask import Flask, redirect, render_template
from loguru import logger

from env_loader import HOST, IS_DEBUG, PORT
from utils.db import check_db

# Создаём объект flask-приложения
app = Flask(__name__, template_folder="pages")


@app.route("/")
@app.route("/?<refer>")
async def main_page(refer: str | None=None) -> str:
    """Переводит на лендинг или на страницу курсов.

    В зависимости от того, зарегистрирован пользователь,
    или нет.
    """
    # Проверяем есть ли реферальная информация
    # Сохраняем реферальную информацию
    # TODO(@iamlostshe): Добавить `refer` (реферальную информацию) в базу данных

    # Выводим её в лог
    logger.debug("refer: {}", refer)

    # Если пользователь зарегистрирован

    # TODO(@iamlostshe): if <пользователь зарегистрирован>:
    # Переводим на страницу курсов
    # await redirect("courses_page")  # noqa: ERA001

    # else:  # noqa: ERA001
    # Переводим на landing
    return redirect("landing")


@app.route("/landing")
async def landing() -> str:
    """Render landing."""
    return render_template("landing.html")


async def main() -> None:
    """Асинхронная функция для запуска flask-сервер."""
    # Загружаем файл для записи логов
    logger.add("edu_project.log")

    # Проверяем наличие файлов баз данных
    await check_db()

    # Запускаем flask-сервер
    app.run(debug=IS_DEBUG, host=HOST, port=PORT)


if __name__ == "__main__":
    # Запускаем
    asyncio.run(main())
