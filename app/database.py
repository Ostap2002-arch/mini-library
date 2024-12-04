import json
import os
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(__file__)))

from app.settings import settings

if settings.MODE == 'TEST':
    path = settings.TEST_PATH
else:
    path = settings.BASE_PATH


def get_path():
    return path
