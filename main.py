
import os

from fastapi import FastAPI
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

