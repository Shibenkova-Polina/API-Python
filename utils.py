import json

from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
# Pydantic: Обеспечивает валидацию и автоматическую сериализацию данных.
from datetime import date, datetime
from typing import Optional, Any
import re

from json_db_lite import JSONDatabase


def dict_list_to_json(dict_list, filename):
    """
    Преобразует список словарей в JSON-строку и сохраняет её в файл.

    :param dict_list: Список словарей
    :param filename: Имя файла для сохранения JSON-строки
    :return: JSON-строка или None в случае ошибки
    """
    try:
        json_str = json.dumps(dict_list, ensure_ascii=False)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_str)
        return json_str
    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при преобразовании списка словарей в JSON или записи в файл: {e}")
        return None


# def json_to_dict_list(filename):
#     """
#     Преобразует JSON-строку из файла в список словарей.
#
#     :param filename: Имя файла с JSON-строкой
#     :return: Список словарей или None в случае ошибки
#     """
#     try:
#         with open(filename, 'r', encoding='utf-8') as file:
#             json_str = file.read()
#             dict_list = json.loads(json_str)
#         return dict_list
#     except (TypeError, ValueError, IOError) as e:
#         print(f"Ошибка при чтении JSON из файла или преобразовании в список словарей: {e}")
#         return None

########################################################################################################################

class Major(str, Enum):
    # наследуется от str и Enum для обеспечения определенных функциональных возможностей
    # перечисление, где каждый член является строкой

    informatics = "Информатика"
    economics = "Экономика"
    law = "Право"
    medicine = "Медицина"
    engineering = "Инженерия"
    languages = "Языки"


class SStudent(BaseModel):
    # класс Field для описания поля в библиотеке Pydantic используется для добавления дополнительных метаданных
    # к полям моделей, которые наследуются от BaseModel
    # default=... значит, что данное значение обязательно
    # gt, ge, lt, le: ограничения для числовых значений (больше, больше или равно, меньше, меньше или равно)
    # max_digits, decimal_places: ограничения для чисел с плавающей точкой (максимальное количество цифр, количество десятичных знаков)

    student_id: int
    phone_number: str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(default=..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
    last_name: str = Field(default=..., min_length=1, max_length=50,
                           description="Фамилия студента, от 1 до 50 символов")
    date_of_birth: date = Field(default=..., description="Дата рождения студента в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(default=..., description="Электронная почта студента")
    address: str = Field(default=..., min_length=10, max_length=200,
                         description="Адрес студента, не более 200 символов")
    enrollment_year: int = Field(default=..., ge=2002, description="Год поступления должен быть не меньше 2002")
    major: Major = Field(default=..., description="Специальность студента")
    course: int = Field(default=..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
    special_notes: Optional[str] = Field(default=None, max_length=500,
                                         description="Дополнительные заметки, не более 500 символов")

    # Validators: Пользовательские проверки данных
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:   # класс, значение, валидность которого проверяется
        if not re.match(r'^\+\d{11}$', values):
            # принудительный вызов ошибки
            raise ValidationError('Номер телефона должен начинаться с "+" и содержать 11 цифр')
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValidationError('Дата рождения должна быть в прошлом')
        return values

class RBStudent:  # request body
    def __init__(self, course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
        self.course: int = course
        self.major: Optional[str] = major
        self.enrollment_year: Optional[int] = enrollment_year

########################################################################################################################

# инициализация объекта
small_db = JSONDatabase(file_path='students.json')


# получаем все записи
def json_to_dict_list():
    return small_db.get_all_records()


# добавляем студента
def add_student(student: dict):
    student['date_of_birth'] = student['date_of_birth'].strftime('%Y-%m-%d')  # strftime() преобразует объект типа datetime в строку
    small_db.add_records(student)
    return True


# обновляем данные по студенту
def upd_student(upd_filter: dict, new_data: dict):
    small_db.update_record_by_key(upd_filter, new_data)
    return True


# удаляем студента
def dell_student(key: str, value: str):
    small_db.delete_record_by_key(key, value)
    return True


# Модель для фильтрации
class SUpdateFilter(BaseModel):
    student_id: int


# Определение модели для новых данных студента
class SStudentUpdate(BaseModel):
    course: int = Field(..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
    major: Optional[Major] = Field(..., description="Специальность студента")


class SDeleteFilter(BaseModel):
    key: str
    value: Any
