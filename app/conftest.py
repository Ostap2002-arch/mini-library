
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(__file__)))

from app.settings import settings


settings.MODE = 'TEST'
print(1)
