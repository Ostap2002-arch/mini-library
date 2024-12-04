class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class StatusException(CustomException):
    def __init__(self, message):
        super().__init__(f"Статус книги может иметь значения 'в наличии', 'выдана'. Введённое значение - '{message}'")


class StatusRepeatException(CustomException):
    def __init__(self, message):
        super().__init__(f"Статус книги нельзя изменить на тоже самое. Книга уже {message}")


class CanNotDetected(CustomException):
    def __init__(self, id):
        super().__init__(f"Не возможно найти книгу с id равным {id}")


class DateException(CustomException):
    def __init__(self, date):
        super().__init__(f"Год издания должно быть натуральное число от 0 до 2024. Введённый год издания - '{date}'")


class EmptyTitleValue(CustomException):
    def __init__(self, title):
        super().__init__(
            f"Название книги должно содержать хотя бы один символ, не считая знаков пунктуации. Введённое название - '{title}'")


class EmptyAuthorValue(CustomException):
    def __init__(self, author):
        super().__init__(
            f"Имя автора книги должно содержать хотя бы один символ, не считая знаков пунктуации. Введённое имя - '{author}'")


class IdValueException(CustomException):
    def __init__(self, id):
        super().__init__(f"id книги должно быть натуральное число. Введённое id - '{id}'")
