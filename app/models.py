import json
import os
import sys
from os.path import dirname
from typing import List, Optional, Union

from app.database import get_path

sys.path.insert(0, dirname(dirname(__file__)))
from app.exceptions import CanNotDetected, StatusRepeatException


class Model:
    def __init__(self):
        self.path = get_path()
        self.data = self.get_data()

    def get_data(self) -> List[dict]:
        """Возвращает все данные из базы данных.

        Этот метод ничего не принимает и возвращает список словарей с данными.

        Returns:
            List[dict]: Список словарей.

        Raises:
            FileNotFoundError: Если база данных не найдена.
            JSONDecodeError: Ошибка данных внутри базы данных.
        """
        if os.path.getsize(self.path) > 0:
            with open(self.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return []

    def save_data(self) -> None:
        """Сохраняет изменения в базу данных.

        Этот метод ничего не принимает и ничего не возвращает и сохраняет изменения в базу данных


        Returns:
            None

        Raises:
            FileNotFoundError: Если база данных не найдена.
            TypeError: Сериализация неподдерживаемых типов данных.
        """

        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

    def add_item(self, item: dict) -> int:
        """Добавляет новую запись в базу данных.

        Этот метод принимает новую запись в формате словаря и добавляет её в базу данных.

        Args:
            item (dict): Новая запись.

        Returns:
            int: id созданного элемента

        Raises:
            FileNotFoundError: Если база данных не найдена.
            TypeError: Сериализация неподдерживаемых типов данных.
        """
        id = max(map(lambda x: x['id'], self.data), default=-1) + 1
        item = {'id': id} | item | {'status': 'в наличии'}
        self.data.append(item)
        self.save_data()
        return id

    def del_item(self, id: int) -> None:
        """Удаляет запись из базы данных

        Этот метод принимает id записи и удаляет её из базы данных.

        Args:
            id (int): id.

        Returns:
            None

        Raises:
            FileNotFoundError: Если база данных не найдена.
            CanNotDetected: Попытка удалить несуществующую запись.
        """
        item = self.find_item({'id': id})
        if not len(item):
            raise CanNotDetected(id)
        self.data.remove(item[0])
        self.save_data()

    def find_item(self, keys: dict) -> List[dict]:
        """Функция поиска записей по параметрам.

        Этот метод принимает параметры в виде dict и возвращает список записей в базе данных, удовлетворяющим
        заданными условиям.

        Args:
            keys (dict): Параметры в виде словаря. В качестве поиска используются id, title, auther, status.
                        Пример словаря с максимальным количеством переменных {"id": 1, "title": "1984", "author": "Джордж Оруэлл", "year": 1949, "status": "в наличии"}

        Returns:
            List[dict]: Список записей в базе данных.

        """
        result = self.data
        for key, values in keys.items():
            if values is None:
                continue
            else:
                result = list(filter(lambda x: x[key] == values, result))
        return result

    def change_status(self, id: int, status: str) -> None:
        """Изменяет статус записи.

        Этот метод принимает id и новый статус. Метод ничего не возвращает и только изменяет статус.

        Args:
            id (int): id записи.
            status (str): новый статус.

        Returns:
            None

        Raises:
            FileNotFoundError: Если база данных не найдена.
            CanNotDetected: Попытка обновить статус несуществующей записи.
            StatusRepeatException: Попытка изменить статус на тот же самый.
        """
        item = self.find_item({'id': id})
        if not len(item):
            raise CanNotDetected(id)
        if item[0]['status'] == status:
            raise StatusRepeatException(status)
        item[0]['status'] = status
        self.save_data()


model = Model()
