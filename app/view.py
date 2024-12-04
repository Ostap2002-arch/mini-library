import json
import sys
from os.path import dirname

sys.path.insert(0, dirname(__file__))

from app.controller import Controller
from app.utils import print_table


class View:
    @classmethod
    def add_item_form_templates(cls) -> None:
        """Метод выводящий интерфейс консольного приложения для добавления новой книги \n
            title - не пустая строка \n
            auther - не пустая строка \n
            year - натуральное число от 0 до 2024 \n
        """
        title = input('Введите название книги: ')
        author = input('Введите имя и автора книги: ')
        year = input('Введите год публикации книги: ')
        new_id = Controller.add_item(title=title, author=author, year=year)
        print(f'Успешно добавлена книга с id = {new_id}')


    @classmethod
    def del_item_form_templates(cls) -> None:
        """Метод выводящий интерфейс консольного приложения для удаления книги по её id \n
            id - натуральное число соответствующему id существующей записи в базе данных
        """
        id = input('Введите id книги, которую необходимо удалить: ')
        Controller.del_item(id=id)
        print(f'Успешно удалена книга с id = {id}')


    @classmethod
    def get_items_form_templates(cls) -> None:
        """Метод выводящий интерфейс консольного приложения для получения всех записей из базы данных
        """
        result = Controller.get_items()
        print_table(result)

    @classmethod
    def get_item_filter_form_templates(cls) -> None:
        """Метод выводящий интерфейс консольного приложения для поиска нужной книги и выбора параметров поиска \n
            title - не пустая строка (опционально) \n
            author - не пустая строка (опционально) \n
            year - натуральное число от 0 до 2024 (опционально)
        """
        print('''Поиск нужной вам книги можно осуществить по названию книги, имени автора или года издания.  
Можно осуществлять поиск сразу по нескольким параметрам, тем самым сужая круг поиска. 
Для игнорирования фильтра просто нажимайте Enter.''')
        title = input('Введите название книги (при необходимости): ')
        author = input('Введите имя и автора книги (при необходимости): ')
        year = input('Введите год публикации книги (при необходимости): ')
        result = Controller.get_item_filter(title=title if title else None,
                                    author=author if author else None,
                                    year=year if year else None,
                                    )
        print_table(result)


    @classmethod
    def update_item_form_templates(cls) -> None:
        """Метод выводящий интерфейс консольного приложения для обновления статуса книги по её id \n
            id - натуральное число соответствующему id существующей записи в базе данных
            status - непустая строка, может иметь значения только 'в наличии' или 'выдана'
        """
        id = input('Введите id книги, статус которой необходимо обновить: ')
        status = input('Новый статус: ')
        Controller.update_item(id=id, status=status)
        print(f'Успешно обновлён статус на {status} у книги с id = {id}')


