"""Основной модуль для запуска."""

from __future__ import annotations

import asyncio

from flask import Flask, jsonify, redirect, render_template, request
from loguru import logger

from env_loader import HOST, IS_DEBUG, PORT
from utils import db

# Создаём объект flask-приложения
app = Flask(__name__, template_folder="pages")


@app.route("/api/reg", methods=["POST"])
async def reg_api() -> str:
    """Раздел API отвечает за регистрацию пользователя."""
    # Получаем переданную в json информацию
    data = request.get_json()

    logger.debug("data {}", data)

    # Логин
    login = data.get("login")
    if not login:
        return jsonify({"ok": False, "message": "Необходимо указать логин."})

    # Пароль
    password = data.get("password")
    if not password:
        return jsonify({"ok": False, "message": "Необходимо указать пароль."})

    # csrf-токен
    csrf_token = request.cookies.get("csrftoken")
    if not csrf_token:
        return jsonify({"ok": False, "message": "Необходимо указать csrf-токен."})

    # Регистрируем пользователя
    u = db.Users()
    add_user = await u.add(csrf_token, login, password, refer=None)
    return jsonify(add_user)


# TODO(@iamlostshe): Сделать вход:
# app.route("/api/auth", methods=["POST"])  # noqa: ERA001
# async def auth_api() -> str:


@app.route("/reg")
@app.route("/reg?")
async def reg_page() -> str:
    """Страница регистрации."""
    return render_template("reg.html")


@app.route("/landing")
async def landing_page() -> str:
    """Страница-лендинг.

    Даёт пользователю общее представление о проекте.
    """
    return render_template("landing.html")


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


async def main() -> None:
    """Асинхронная функция для запуска flask-сервер."""
    # Загружаем файл для записи логов
    logger.add("edu_project.log")

    # Проверяем наличие файлов баз данных
    db.check_db()

    # Запускаем flask-сервер
    app.run(debug=IS_DEBUG, host=HOST, port=PORT)


if __name__ == "__main__":
    # Запускаем
    asyncio.run(main())
