import pytest

from app.controller import Controller
from app.exceptions import EmptyTitleValue, EmptyAuthorValue, DateException, CanNotDetected, IdValueException, \
    StatusException


@pytest.mark.parametrize("kwargs, error, value", [({"title": ".", "author": "Лев Толстой", "year": 1869},
                                                   EmptyTitleValue,
                                                   "Название книги должно содержать хотя бы один символ, не считая знаков пунктуации. Введённое название - '.'"),
                                                  ({"title": "Война и мир", "author": "", "year": 1869},
                                                   EmptyAuthorValue,
                                                   "Имя автора книги должно содержать хотя бы один символ, не считая знаков пунктуации. Введённое имя - ''"),
                                                  ({"title": "Война и мир", "author": "", "year": -67},
                                                   DateException,
                                                   "Год издания должно быть натуральное число от 0 до 2024. Введённый год издания - '-67'"),
                                                  ({"title": "Война и мир", "author": "",
                                                    "year": 'тысяча весемьсот шестьдесят девятый'},
                                                   DateException,
                                                   "Год издания должно быть натуральное число от 0 до 2024. Введённый год издания - 'тысяча весемьсот шестьдесят девятый'"),
                                                  ]
                         )
def test_add_item_error(kwargs, error, value):
    with pytest.raises(error) as e:
        Controller.add_item(**kwargs)
    assert str(e.value) == value


@pytest.mark.parametrize("id, error, value", [
    (100, CanNotDetected, "Не возможно найти книгу с id равным 100"),
    ('qwerty', IdValueException, "id книги должно быть натуральное число. Введённое id - 'qwerty'"),
    (-3, IdValueException, "id книги должно быть натуральное число. Введённое id - '-3'"),
]
                         )
def test_del_item_error(id, error, value):
    with pytest.raises(error) as e:
        Controller.del_item(id=id)
    print(e.value)
    assert str(e.value) == value


def test_get_items():
    assert len(Controller.get_items()) == 6


test_item_1 = {"title": "1984", "author": "Джордж Оруэлл", "year": 1949}
test_item_2 = {"title": "Убежище", "author": "Альбер Камю", "year": 1949}
test_item_3 = {"title": "Бель-Ами", "author": "Ги де Мопассан", "year": 1949}
test_item_4 = {"title": "Чума", "author": "Альбер Камю", "year": 1949}
test_item_5 = {"title": "Долгая застава", "author": "Андре Жид", "year": 1949}
test_item_6 = {"title": "Зов предков", "author": "Жак Фрези", "year": 1949}

list_test_item = [test_item_1, test_item_2, test_item_3, test_item_4, test_item_5, test_item_6]


@pytest.mark.parametrize("item, new_id", [(item, i + 6) for i, item in enumerate(list_test_item, start=1)])
def test_add_item(item, new_id):
    assert Controller.add_item(**item) == new_id
    assert len(Controller.get_items()) == new_id


def test_update_item_error():
    with pytest.raises(StatusException) as e:
        Controller.update_item(id=7, status='Потеряна')
    assert str(e.value) == "Статус книги может иметь значения 'в наличии', 'выдана'. Введённое значение - 'Потеряна'"


@pytest.mark.parametrize("id_update, status", [(7, 'выдана'), (8, 'выдана'), (9, 'выдана')])
def test_update_item(id_update, status):
    Controller.update_item(id=id_update, status=status)



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
def test_get_item_filter(kwargs, total):
    assert len(Controller.get_item_filter(**kwargs)) == total


@pytest.mark.parametrize("id_delete, total",
                         [(12 - id_delete, 12 - id_delete - 1) for id_delete in range(len(list_test_item))])
def test_del_item(id_delete, total):
    Controller.del_item(id=id_delete)
    assert len(Controller.get_items()) == total




