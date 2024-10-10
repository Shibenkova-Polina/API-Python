from pydantic import ValidationError
from utils import SStudent
from datetime import date


def test_valid_student(data: dict) -> None:
    try:
        student = SStudent(**data)      # Распаковывает содержимое словаря в вызов функции.
        print(student)
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")

student_data = {
    "student_id": 1,
    "phone_number": "+1234567890",
    "first_name": "Иван",
    "last_name": "Иванов",
    "date_of_birth": date(2000, 1, 1),
    "email": "ivan.ivanov@example.com",
    "address": "Москва, ул. Пушкина, д. Колотушкина",
    #"enrollment_year": 1022,
    "enrollment_year": 2022,
    #"major": "Программирование",
    "major": "Информатика",
    #"course": 6,
    "course": 3,
    #"special_notes": "Увлекается программированием"   # можно передавать или нет, ошибок не будет
}

test_valid_student(student_data)