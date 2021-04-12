import logging
import os
import configparser
from logging.handlers import RotatingFileHandler


ROOT_DIR = os.path.dirname(os.path.abspath("settings.py"))
settings_file = open(os.path.join(ROOT_DIR, "settings.ini"), "r")
config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, "settings.ini"))


def __get_db_path() -> str:
    path = config.get('DB', 'sqlite')
    if path == '':
        path = 'sfms.db'
    elif '.db' not in path:
        path = path + '.db'
    return path


def __get_files_dir() -> str:
    path = config.get('SECRETS', 'files_dir')
    dir_not_exists = False
    if path == '':
        path = os.path.join(ROOT_DIR, "files_storage")
        dir_not_exists = True
    elif not os.path.exists(path):
        dir_not_exists = True

    elif not os.path.isdir(path):
        raise Exception("Files storage path provided is not a directory, check settings.ini")

    if dir_not_exists:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

    return path


SECRET_KEY = config.get('SECRETS', 'flask_key')
DB_PATH = __get_db_path()

FILES_DIR = __get_files_dir()

CSRF = True
FILES_PER_PAGE = 8

# Flask user config
USER_APP_NAME = "Simple File Management System"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False
USER_ENABLE_USERNAME = True
USER_CORPORATION_NAME = "Gerardo"
USER_COPYRIGHT_YEAR = 2021

# LOGGING CONFIG

logger = logging.getLogger('smfs')
logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#to log debug messages
debug_logger = logging.StreamHandler()
debug_logger.setLevel(logging.DEBUG)
debug_logger.setFormatter(formatter)

#to log general messages
# x2 files of 2mb
info_logger = RotatingFileHandler(filename='smfs.log', maxBytes=2097152, backupCount=2)
info_logger.setLevel(logging.INFO)
info_logger.setFormatter(formatter)

#to log errors messages
error_logger = RotatingFileHandler(filename='smfs_errors.log', maxBytes=2097152, backupCount=2)
error_logger.setLevel(logging.ERROR)
error_logger.setFormatter(formatter)

logger.addHandler(debug_logger)
logger.addHandler(info_logger)
logger.addHandler(error_logger)
