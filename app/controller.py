import sys
from os.path import dirname
from typing import List

from app.exceptions import DateException, EmptyAuthorValue, EmptyTitleValue, IdValueException, StatusException
import string

sys.path.insert(0, dirname(__file__))

from app.models import Model

punctuation = set(string.punctuation + ' ')


def check_id(func):
    """Функция-декоратор проверяющая id.

    Эта функция выполняет валидацию переменной id. id должно быть натуральное числом.

    Args:
        func (callable): Декорируемая функция.

    Returns:
        callable: Возвращает результат func при корректном id

    Raises:
        IdValueException: Возникает при некорректным  значении id.
    """
    def wrapper(cls, **kwargs):
        if 'id' in kwargs.keys():
            id = kwargs.get('id')
            try:
                id = int(id)
            except Exception:
                raise IdValueException(id)
            if id < 0:
                raise IdValueException(id)
            kwargs['id'] = id
        return func(cls, **kwargs)

    return wrapper


def check_data(ignore=False):
    """Функция-декоратор, проверяющая корректность данных, передаваемых в функцию.

    Args:
        ignore (bool): Параметр отвечающий, нужно ли вызывать исключение, если ничего не дано в параметре. По умолчанию нужно.

    Returns:
        callable: Возвращает результат func при корректных данных

    Raises:
        DateException: Некорректная дата. Год издания должно быть натуральное число от 0 до 2024.
        EmptyTitleValue: Некорректное название. Название книги должно содержать хотя бы один символ, не считая знаков пунктуации.
        EmptyAuthorValue: Некорректное имя автора. Имя автора книги должно содержать хотя бы один символ, не считая знаков пунктуации.
    """
    def decorator(func):
        def wrapper(cls, **kwargs):
            if year := kwargs.get('year'):
                try:
                    year = int(year)
                except Exception:
                    raise DateException(year)
                if year > 2024 or year < 0:
                    raise DateException(year)
                kwargs['year'] = year
            if 'title' in kwargs.keys():
                title = kwargs.get('title')
                if (not title or set(title).issubset(punctuation)) and not ignore:
                    raise EmptyTitleValue(title)
            if 'author' in kwargs.keys():
                author = kwargs.get('author')
                if (not author or set(author).issubset(punctuation)) and not ignore:
                    raise EmptyAuthorValue(author)
            return func(cls, **kwargs)

        return wrapper

    return decorator


class Controller:
    model = Model()

    @classmethod
    @check_data()
    def add_item(cls, **kwargs) -> int:
        """Метод проверки данных при создании записи

        Этот метод проверяет содержимое новой записи перед её внесением в базу данных

        Args:
            **kwargs (dict): Новая записи в формате словаря {'title': str, 'auther': str, 'date': int}

        Returns:
            int: id новой записи
        """
        return cls.model.add_item(item=kwargs)

    @classmethod
    @check_id
    def del_item(cls, id: int) -> None:
        """Метод проверки данных при удалении записи

        Этот метод проверяет корректность id записи, которую нужно удалить

        Args:
            id (int): id удаляемой записи

        Returns:
            None
        """
        cls.model.del_item(id)

    @classmethod
    @check_data(ignore=True)
    def get_item_filter(cls, **kwargs) -> List[dict]:
        """Метод проверки данных при поиске записи

        Этот метод проверяет корректность параметров поиска, перед обращением к базе данных

        Args:
            **kwargs (dict): Новая записи в формате словаря {'title': str, 'auther': str, 'date': int}

        Returns:
            List[dict]
        """
        return cls.model.find_item(kwargs)

    @classmethod
    @check_id
    def update_item(cls, id: int, status: str) -> None:
        """Метод обновления статуса записи.

        Этот метод принимает id и новый статус для записи, и при проверке последних на корректность,
        обращается к базе данных для изменения статуса записи.

        Args:
            id (int): id записи.
            status (str): Новый статус.

        Returns:
            None

        Raises:
            StatusException: Ошибка при не корректном указании статуса. Статус книги может иметь значения 'в наличии', 'выдана'.
        """
        if status != 'в наличии' and status != 'выдана':
            raise StatusException(status)
        cls.model.change_status(id=id, status=status)

    @classmethod
    def get_items(cls) -> List[dict]:
        """Метод получения всех записей из базы данных

        Returns:
            List[dict]
        """
        return cls.model.get_data()
