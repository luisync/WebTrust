import os

from pathlib import Path
from dotenv import load_dotenv

# Laod .env settings.
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

class Settings:
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

    API_HOST = os.getenv("API_HOST")
    API_PORT = int(os.getenv("API_PORT"))

settings = Settings()

