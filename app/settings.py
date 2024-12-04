import json
import os


def load_env(file_path):
    with open(file_path, 'r') as file:
        for string in file.readlines():
            if string := string.strip('\n'):
                key, value = string.split('=')
                os.environ[str(key)] = value
                os.getenv(key)


load_env('.env_non_dev')


class Settings:
    def __init__(self, BASE_PATH, TEST_PATH, MODE):
        self.BASE_PATH = BASE_PATH
        self.TEST_PATH = TEST_PATH
        self.MODE = MODE


settings = Settings(os.getenv('PATH_BASE'), os.getenv('PATH_TEST'), os.getenv('MODE'))
