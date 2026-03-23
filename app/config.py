import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _as_bool(value: str, default: bool = False) -> bool:
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
	API_TITLE = os.getenv("API_TITLE", "Task Management API")
	API_VERSION = os.getenv("API_VERSION", "v1")
	OPENAPI_VERSION = os.getenv("OPENAPI_VERSION", "3.0.3")
	OPENAPI_URL_PREFIX = os.getenv("OPENAPI_URL_PREFIX", "/")
	OPENAPI_SWAGGER_UI_PATH = os.getenv("OPENAPI_SWAGGER_UI_PATH", "/swagger-ui")
	OPENAPI_SWAGGER_UI_URL = os.getenv(
		"OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
	)

	APP_SQLALCHEMY_DATABASE_URI = os.getenv(
		"APP_SQLALCHEMY_DATABASE_URI",
		"mysql+pymysql://root:Ghy%401234@localhost:3036/task_manager",
	)
	SQLALCHEMY_TRACK_MODIFICATIONS = _as_bool(
		os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"),
		False,
	)
	SECRET_KEY = os.getenv("SECRET_KEY", "abcd")
	JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "abcd")
	FLASK_DEBUG = _as_bool(os.getenv("FLASK_DEBUG"), True)
	APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
	APP_PORT = int(os.getenv("APP_PORT", "5000"))

	DB_SERVER_URI = os.getenv("DB_SERVER_URI", "mysql+pymysql://root:Adi12345@localhost:3306")
	DB_NAME = os.getenv("DB_NAME", "task_management")
	DATABASE_URL = os.getenv("DATABASE_URL", "")
	DB_ENGINE_ECHO = _as_bool(os.getenv("DB_ENGINE_ECHO"), True)


settings = Settings()
