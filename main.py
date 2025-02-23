"""Main module: starting app."""

from __future__ import annotations

from flask import Flask, redirect, render_template
from loguru import logger

from env_loader import HOST, IS_DEBUG, PORT
from utils.db import check_db

app = Flask(__name__, template_folder="pages")


@app.route("/")
@app.route("/?<refer>")
def main_page(refer: str | None=None) -> str:
    """Redirect to landing or to user courses page."""
    # TODO(@iamlostshe): Добавить `refer` (реферальную информацию) в базу данных
    logger.debug("refer: {}", refer)

    # TODO(@iamlostshe): Сделать проверку зарегистрирован ли пользователь
    # Если он не зарегистрирован переводим на landing
    return redirect("landing")

    # А если зарегистрирован переводить на страницу курсов
    # return render_template("courses_page")  # noqa: ERA001


@app.route("/landing")
def landing() -> str:
    """Render landing."""
    return render_template("landing.html")


if __name__ == "__main__":
    # Загружаем файл для записи логов
    logger.add("edu_project.log")

    # Проверяем наличие файлов баз данных
    check_db()

    # Starting flask app
    app.run(debug=IS_DEBUG, host=HOST, port=PORT)
