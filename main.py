"""Main module: starting app."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template
from loguru import logger

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
    # return render_template("courses_page")


@app.route("/landing")
def landing() -> str:
    """Render landing."""
    return render_template("landing.html")


if __name__ == "__main__":
    # Loading consts from .env
    load_dotenv()

    IS_DEBUG = os.getenv("DEBUG").lower() == "true"
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # Starting flask app
    app.run(debug=IS_DEBUG, host=HOST, port=PORT)
