"""Models Module Entry Point."""

from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import create_engine

DB_NAME = getenv("POSTGRES_DB") or "py_coin_db"
DB_USER = getenv("POSTGRES_USER") or "py_user"
DB_PASSWORD = getenv("POSTGRES_PASSWORD") or "py_user_password"
DB_HOST = getenv("POSTGRES_HOST") or "localhost"
DB_PORT = getenv("POSTGRES_PORT") or "5432"

ENGINE = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
Base = declarative_base()

Base.metadata.create_all(ENGINE)
