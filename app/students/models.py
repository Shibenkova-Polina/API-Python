# Alembic — это инструмент для управления миграциями баз данных
from sqlalchemy import ForeignKey, text, Text    # SQLAlchemy — это мощная и гибкая библиотека для работы с базами данных в языке программирования Python
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date


# создаем модель таблицы студентов
class Student(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    enrollment_year: Mapped[int]
    course: Mapped[int]
    special_notes: Mapped[str_null_true]
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=False) # таблица majors, столбец id

    major: Mapped["Major"] = relationship("Major", back_populates="students")  # зависимость с таблицей Major по столбцу students

    def __str__(self):              # определение строкового представления объекта, предназначен для создания «приятного» для чтения представления объекта
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    def __repr__(self):             # предназначен для создания «официального» представления, которое может быть использовано для воссоздания объекта
        return str(self)


# создаем модель таблицы факультетов (majors)
class Major(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"

    def __repr__(self):
        return str(self)

# cd app
# python -m alembic init -t async migration   (или alembic init -t async migration)
# python -m alembic revision --autogenerate -m "Initial revision"     для автоматической генерации миграции базы данных с помощью Alembic
# Сгенерированный миграционный скрипт можно применить к БД с помощью команды alembic upgrade head,
# а при необходимости выполнить откат изменений с помощью alembic downgrade.
# Для отмены последнего изменения достаточно выполнить команду: alembic downgrade -1