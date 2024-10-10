from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from app.config import get_db_url

from datetime import datetime
from typing import Annotated


# DB_HOST = 'localhost'
# DB_PORT = '5433'
# DB_NAME = 'fast_api'
# DB_USER = 'user'
# DB_PASSWORD = 'password'
#
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# аннотации, функционирующие аналогично псевдонимам (алиасам), позволяют создавать кастомные шаблоны для описания колонок в SQLAlchemy
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]    # установка значения по умолчанию
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):    # абстрактный класс, от которого наследуются все модели
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:          # определяет имя таблицы для модели на основе имени класса
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]          # части SQLAlchemy, использующиеся для объявления сопоставления между классами Python и структурами таблиц в базе данных
    updated_at: Mapped[updated_at]