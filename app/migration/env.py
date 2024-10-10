import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

import sys
from os.path import dirname, abspath

from alembic import context

from app.database import DATABASE_URL, Base
from app.students.models import Student, Major

sys.path.insert(0, dirname(dirname(abspath(__file__))))
# sys.path — это встроенная переменная в модуле sys, которая возвращает список каталогов, в которых интерпретатор Python будет искать требуемый модуль

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)
# объект конфигурации Alembic (alembic.config.Config), который используется для управления параметрами и настройками миграций
# указаниt URL, по которому Alembic будет подключаться к базе данных SQLAlchemy


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata   # информация о структуре БД, для сравнения текущей с тем, как она должна выглядеть после применения миграций


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
