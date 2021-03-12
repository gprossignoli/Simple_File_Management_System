import logging
import os
import configparser
from logging.handlers import RotatingFileHandler

ROOT_DIR = os.path.dirname(os.path.abspath("settings.py"))
settings_file = open(os.path.join(ROOT_DIR, "settings.ini"), "r")
config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, "settings.ini"))

SECRET_KEY = config.get('SECRETS', 'flask_key')
DB_NAME = config.get('DB', 'sqlite')
CSRF = True