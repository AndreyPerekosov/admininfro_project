import os
import secrets

from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Базовый сервис")


@app.get("/")
def root():
    logger.info("Вызван эндпоинт /")
    return {"message": "Сервис работает"}


@app.get("/health")
def health():
    logger.info("Проверка состояния сервиса")
    return {"status": "ok"}


@app.get("/hello")
def hello(name: str = "студент"):
    logger.info("Вызван эндпоинт /hello, name=%s", name)
    return {"message": f"Привет, {name}!"}


@app.get("/info")
def info():
    app_name = os.getenv("APP_NAME", "Не указано")
    app_author = os.getenv("APP_AUTHOR", "Не указан")

    logger.info("Получена информация о приложении")

    return {
        "app_name": app_name,
        "author": app_author,
    }


@app.get("/config")
def get_config():
    app_name = os.getenv("APP_NAME")
    app_author = os.getenv("APP_AUTHOR")

    logger.info("Запрошен статус конфигурации")

    return {
        "app_name_configured": bool(app_name),
        "app_author_configured": bool(app_author)
    }


@app.get("/convert-to-fahrenheit")
def convert_to_fahrenheit(celsius: float):
    fahrenheit = celsius * 9 / 5 + 32

    logger.info(
        "Перевод температуры: %s °C = %s °F",
        celsius,
        fahrenheit,
    )

    return {
        "celsius": celsius,
        "fahrenheit": round(fahrenheit, 2),
    }


@app.get("/password")
def generate_password(
    length: int = Query(default=16, ge=8, le=64),
):
    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()-_=+"
    )

    password = "".join(
        secrets.choice(alphabet) for _ in range(length)
    )

    logger.info("Сгенерирован пароль длиной %s символов", length)

    return {
        "length": length,
        "password": password,
    }


@app.get("/random")
def random_number(
    minimum: int = -100,
    maximum: int = 100,
):
    if minimum > maximum:
        raise HTTPException(
            status_code=400,
            detail="Минимум не может быть больше максимума",
        )

    result = secrets.randbelow(
        maximum - minimum + 1
    ) + minimum

    logger.info(
        "Сгенерировано случайное число в диапазоне [%s, %s]",
        minimum, maximum,
    )

    return {
        "minimum": minimum,
        "maximum": maximum,
        "number": result,
    }