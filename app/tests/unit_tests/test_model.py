import json
import sys
from os.path import dirname

import pytest

from app.exceptions import CanNotDetected
from app.models import model

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))))


def test_get_data():
    assert len(model.get_data()) == 6


test_item_1 = {"title": "1984", "author": "Джордж Оруэлл", "year": 1949}
test_item_2 = {"title": "Убежище", "author": "Альбер Камю", "year": 1949}
test_item_3 = {"title": "Бель-Ами", "author": "Ги де Мопассан", "year": 1949}
test_item_4 = {"title": "Чума", "author": "Альбер Камю", "year": 1949}
test_item_5 = {"title": "Долгая застава", "author": "Андре Жид", "year": 1949}
test_item_6 = {"title": "Зов предков", "author": "Жак Фрези", "year": 1949}

list_test_item = [test_item_1, test_item_2, test_item_3, test_item_4, test_item_5, test_item_6]


@pytest.mark.parametrize("item, new_id", [(item, i + 6) for i, item in enumerate(list_test_item, start=1)])
def test_add_item(item, new_id):
    assert model.add_item(item) == new_id


@pytest.mark.parametrize("id_update, status", [(7, 'выдана'), (8, 'выдана'), (9, 'выдана')])
def test_change_status(id_update, status):
    model.change_status(id_update, status)
    assert model.find_item({'id': id_update})[0]['status'] == status


@pytest.mark.parametrize("kwargs, total", [({'author': 'Альбер Камю'}, 2),
                                            ({'author': 'Альбер Камю', 'status': 'выдана'}, 1),
                                            ({'author': 'Альбер Камю', 'status': 'в наличии'}, 1),
                                            ({'year': 1949}, 7),
                                            ({'year': 1949}, 7),
                                            ({'author': 'Джордж Оруэлл'}, 2),
                                            ({'author': 'Джордж Оруэлл', 'status': 'выдана'}, 1),
                                            ({'author': 'Джордж Оруэлл', 'status': 'в наличии'}, 1),
                                            ({'author': 'Неизвестный'}, 0),
                                           ])
def test_find_item(kwargs, total):
    assert len(model.find_item(kwargs)) == total


@pytest.mark.parametrize("id_delete, total",
                         [(12 - id_delete, 12 - id_delete - 1) for id_delete in range(len(list_test_item))])
def test_del_item(id_delete, total):
    model.del_item(id=id_delete)
    assert len(model.get_data()) == total


def test_error_delete_by_id():
    with pytest.raises(CanNotDetected) as error:
        model.del_item(id=100)
    assert str(error.value) == "Не возможно найти книгу с id равным 100"

