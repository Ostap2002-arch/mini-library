import sys
from os.path import dirname
from pathlib import Path

import pytest
import os
import json

from app.settings import settings

sys.path.insert(0, dirname(dirname(dirname(__file__))))

from app.database import get_path


@pytest.fixture(scope='module', autouse=True)
def prepare_database():
    def get_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as file_read:
            return json.load(file_read)

    assert settings.MODE == 'TEST'

    path_test = get_path()

    # Очищаем хранилище каждый раз перед тестированием и заполняем данными
    with open(path_test, 'w', encoding='utf-8') as file:
        json.dump(get_data('app/tests/mock_data.json'), file, indent=4)
    yield
    # Очищаем хранилище каждый раз перед тестированием и заполняем данными
    with open(path_test, 'w', encoding='utf-8') as file:
        json.dump(get_data('app/tests/mock_data.json'), file, indent=4)
